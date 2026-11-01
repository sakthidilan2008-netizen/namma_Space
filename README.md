# Namma Space

Open-source, local-first pipeline for reconstructing an indoor space from smartphone imagery and serving it as a navigable 3D digital twin.

## Current milestone: camera-only baseline

This repository starts with a reproducible RGB pipeline:

1. Extract frames from phone video (or use still images).
2. COLMAP estimates camera poses and sparse geometry (SfM).
3. COLMAP PatchMatch + stereo fusion creates a dense point cloud (MVS).
4. Open3D estimates normals and creates a Poisson mesh.
5. Export a GLB for the Three.js web viewer.

**LiDAR is optional and is not silently assumed.** The iPhone Pro capture adapter is deliberately format-agnostic until the team confirms which capture app and export formats the organizers accept. A future synchronized RGB/depth adapter can add metric scale and depth constraints without replacing the RGB baseline.

## Requirements

- Python 3.10+
- COLMAP CLI available on PATH (tested against your installed version before a full run)
- FFmpeg available on PATH (only needed for video input)
- Python dependencies: `pip install -r requirements.txt`

COLMAP and Open3D are open-source. Check the exact versions and licence notices of every dependency before submission; include the notices in the technical abstract.

## Quick start

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt

# If your capture is a video:
python -m reconstruction.prepare_video --video data/room_walkthrough.mov --out data/images --fps 2

# Run reconstruction from extracted frames or manually copied images:
python -m reconstruction.run_pipeline --images data/images --work outputs/room01 --colmap colmap

# Optional scale calibration (known measured distance in metres between two reconstructed camera centres
# is not yet automated; use a measured scene reference during validation).
```

The first successful run is a **baseline**, not a promise of photorealistic quality. Results depend on coverage, texture, motion blur, exposure, repeated patterns, reflective surfaces, and COLMAP's ability to register images.

## Input contract

- `data/images/`: JPEG/PNG frames, named in capture order.
- Avoid mixing frames from different floors or disconnected rooms in one reconstruction until the individual room models are stable.
- Preserve original source captures separately; never overwrite raw data.
- Record device model, app/version, capture date, frame extraction rate, and any LiDAR/depth export details in `capture_manifest.json`.

## Output

`outputs/<scene>/` contains COLMAP workspaces, sparse/dense point clouds, `scene_mesh.ply`, `scene.glb`, and `run_report.json`. The GLB is the intended input to the web viewer.

## Current limitations

- No LiDAR/depth fusion yet: RGB-only geometry is generally scale-ambiguous and can drift.
- Multi-floor alignment is not automatic in this first milestone. Process each floor/connected region separately, then align using measured dimensions and stair/landing control points.
- POI detection, semantic search, collision navigation, and WebXR are later milestones.
- A reconstruction must be evaluated against measured dimensions and visual references; a successful command exit is not proof of fidelity.

## Competition alignment

Round 1: document the SOP, pipeline, input sample data, code repository, and browser free-roaming viewer. The official walkthrough PDF says Round 1 judges SOP/pipeline soundness, visual quality/model fidelity, web viewer performance, and documentation/video clarity (page 9). Round 2 adds POI labelling/search and obstacle-aware desktop navigation; WebXR AR is a finale bonus (page 7).

## Licence

Project code: MIT. Third-party tools retain their own licences; see `THIRD_PARTY_NOTICES.md`.
