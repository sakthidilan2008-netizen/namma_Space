# Reconstruction architecture — milestone 1

## Data flow

`iPhone RGB capture -> ordered frames -> COLMAP SfM -> COLMAP MVS -> fused point cloud -> Open3D mesh -> GLB -> Three.js viewer`

### Why this baseline

- The competition explicitly accepts ordinary photos/video/sensor data and asks teams to define their own SOP.
- Camera-only reconstruction provides a baseline independent of a specific iOS capture app.
- COLMAP is an established local SfM/MVS engine. It estimates camera poses and geometry from overlapping images.
- Open3D provides local point-cloud processing and mesh export.
- The pipeline preserves intermediate artefacts so failures can be diagnosed rather than hidden.

## Planned sensor extension

An optional capture adapter will accept:
- RGB frames (JPEG/HEIC converted to lossless or high-quality JPEG for processing)
- per-frame depth maps (16-bit PNG/EXR or documented binary format)
- camera intrinsics
- camera pose / timestamp metadata
- depth scale and invalid-depth convention

Do not assume two sensor streams are synchronized merely because they are recorded in one app. Validate timestamp alignment and dropped-frame behaviour. The Xcode capture app is a later adapter, not a dependency for the initial RGB baseline.

## AI component (later, only where it helps)

Round 1's supplied brief does not mandate a trained AI model. For Round 2, a locally run open-weight vision model can propose semantic labels for visible objects/areas, with human confirmation. POI names are provided on-site, and human labelling is explicitly allowed. The final system should keep a traceable distinction between model suggestions and human-approved labels. Model and weights licence must be checked before use.

## Known engineering risks

1. Textureless/white walls and repeated corridors weaken visual feature matching.
2. Motion blur, rolling shutter, exposure shifts and fast turns break camera tracking.
3. RGB-only scale is ambiguous; anchor the model using measured dimensions.
4. Moving people cause ghosting; capture during low-traffic periods or mask dynamic regions.
5. Separate floors/rooms may form disconnected components; align with measured dimensions and surveyed control points.
6. Poisson meshing can close openings or invent surfaces; inspect and compare against photographs and dimensions.

## Acceptance tests

- At least 80% of captured frames register (initial internal target; report actual value).
- No major room/corridor is missing in the walkthrough.
- Measured wall-to-wall dimensions are within a declared tolerance (target <= 10% initially; report actual error).
- Viewer loads the GLB and supports collision-aware first-person movement (viewer milestone).
- All raw sample inputs and exact commands are included in the submission package.
