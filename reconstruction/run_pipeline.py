"""Local RGB indoor reconstruction: COLMAP SfM/MVS -> Open3D mesh -> GLB."""
import argparse
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".tif", ".tiff"}

def run(cmd, log_path):
    with log_path.open("a", encoding="utf-8") as log:
        log.write("\n$ " + " ".join(map(str, cmd)) + "\n")
        log.flush()
        subprocess.run(list(map(str, cmd)), check=True, stdout=log, stderr=subprocess.STDOUT)

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--images", type=Path, required=True)
    p.add_argument("--work", type=Path, required=True)
    p.add_argument("--colmap", default="colmap")
    p.add_argument("--camera-model", default="OPENCV", choices=["SIMPLE_RADIAL","RADIAL","OPENCV","FULL_OPENCV"])
    p.add_argument("--quality", default="high", choices=["low","medium","high","extreme"])
    args = p.parse_args()

    images = args.images.resolve()
    work = args.work.resolve()
    if not images.is_dir():
        p.error(f"Image directory does not exist: {images}")
    image_files = [f for f in images.iterdir() if f.is_file() and f.suffix.lower() in IMAGE_EXTS]
    if len(image_files) < 20:
        p.error(f"Need at least 20 usable images for a meaningful first attempt; found {len(image_files)}.")
    colmap = shutil.which(args.colmap)
    if not colmap:
        p.error("COLMAP executable not found. Install COLMAP and add its CLI to PATH.")
    work.mkdir(parents=True, exist_ok=True)
    database = work / "database.db"
    sparse = work / "sparse"
    dense = work / "dense"
    sparse.mkdir(exist_ok=True)
    log_path = work / "pipeline.log"
    report = {
        "status":"running", "input_image_count":len(image_files),
        "input_directory":str(images), "started_unix":time.time(),
        "pipeline":"COLMAP SfM + PatchMatch MVS + Open3D Poisson mesh",
        "scale":"unknown_without_metric_reference", "lidar_used":False
    }
    (work/"run_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    try:
        run([colmap,"feature_extractor","--database_path",database,"--image_path",images,
             "--ImageReader.camera_model",args.camera_model], log_path)
        run([colmap,"exhaustive_matcher","--database_path",database], log_path)
        run([colmap,"mapper","--database_path",database,"--image_path",images,
             "--output_path",sparse], log_path)
        models = sorted([d for d in sparse.iterdir() if d.is_dir() and (d/"images.bin").exists()])
        if not models:
            raise RuntimeError("COLMAP registered no sparse model. Inspect pipeline.log and improve capture coverage.")
        model = models[0]
        run([colmap,"image_undistorter","--image_path",images,"--input_path",model,
             "--output_path",dense,"--output_type","COLMAP"], log_path)
        run([colmap,"patch_match_stereo","--workspace_path",dense,"--workspace_format","COLMAP",
             "--PatchMatchStereo.geom_consistency","true"], log_path)
        fused = dense/"fused.ply"
        run([colmap,"stereo_fusion","--workspace_path",dense,"--workspace_format","COLMAP",
             "--input_type","geometric","--output_path",fused], log_path)

        try:
            import open3d as o3d
        except ImportError as exc:
            raise RuntimeError("Open3D missing. Run: pip install -r requirements.txt") from exc

        cloud = o3d.io.read_point_cloud(str(fused))
        if cloud.is_empty() or len(cloud.points) < 1000:
            raise RuntimeError("Dense point cloud is empty/too small. Inspect capture and COLMAP logs.")
        cloud = cloud.voxel_down_sample(voxel_size=0.015)
        cloud.estimate_normals()
        cloud.orient_normals_consistent_tangent_plane(30)
        mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(cloud, depth=10)
        density_threshold = sorted(densities)[int(len(densities)*0.02)]
        import numpy as np
        mesh.remove_vertices_by_mask(np.asarray(densities) < density_threshold)
        mesh.compute_vertex_normals()
        mesh_path = work/"scene_mesh.ply"
        glb_path = work/"scene.glb"
        if not o3d.io.write_triangle_mesh(str(mesh_path), mesh):
            raise RuntimeError("Failed to write PLY mesh.")
        if not o3d.io.write_triangle_mesh(str(glb_path), mesh, write_vertex_normals=True):
            raise RuntimeError("Failed to write GLB. Check Open3D GLTF support.")
        report.update({
            "status":"completed", "finished_unix":time.time(),
            "registered_sparse_model":str(model), "dense_point_cloud":str(fused),
            "mesh_ply":str(mesh_path), "mesh_glb":str(glb_path),
            "point_count_after_downsample":len(cloud.points),
            "mesh_vertices":len(mesh.vertices), "mesh_triangles":len(mesh.triangles)
        })
    except Exception as exc:
        report.update({"status":"failed","error":str(exc),"finished_unix":time.time()})
        raise
    finally:
        (work/"run_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Reconstruction complete: {work/'scene.glb'}")

if __name__ == "__main__":
    main()
