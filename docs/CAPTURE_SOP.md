# Indoor capture SOP — draft v0.1

## Before capture
1. Choose one floor and one connected room/corridor loop for the first dataset.
2. Record a rough hand sketch and measure at least two known distances (door width, room length, corridor width).
3. Remove avoidable moving objects; if people are present, capture during a quieter period.
4. Clean the camera lens; use consistent lighting and avoid changing exposure modes mid-scan.
5. Record device model, capture app/version, video resolution/FPS, and whether depth was recorded.

## Capture path
1. Start at a visually distinctive anchor point.
2. Walk slowly at approximately 0.3–0.5 m/s; avoid rapid pans and sudden rotations.
3. Keep the camera at a steady chest/eye height and aim slightly downward enough to retain floor-wall geometry without losing wall features.
4. Overlap adjacent views substantially; turn at corners slowly and pause briefly to capture each corner.
5. Capture each room doorway from both sides and include transitions between connected rooms.
6. Make a loop back toward the starting area to reduce drift and help loop closure.
7. Capture stairs/landings separately and record floor identity; do not assume vertical alignment.

## Data handling
- Preserve original video/photos.
- Extract video at 1–3 frames/second initially; inspect frames and remove blurred/near-duplicate images.
- Keep frames in chronological order.
- Save a `capture_manifest.json` using the provided example.
- Store any depth maps, intrinsics and timestamps alongside RGB frames without changing filenames or timestamp associations.

## Quality gate
Before running reconstruction, check for blur, severe exposure changes, insufficient overlap, missing corners, featureless walls, and people crossing most frames. Re-capture weak sections rather than trying to fix all capture problems in software.
