# Namma Space — Round 1 Web Viewer Starter

A local-first Three.js viewer for reconstructed indoor scenes. It currently accepts binary glTF (`.glb`) outputs and provides a browser-based first-person walkthrough (WASD + mouse).

## Important scope boundary

This is the **viewer component only**. It does not reconstruct a 3D scene from photos, video, depth, or LiDAR. The reconstruction engine must generate a valid GLB/GLTF asset that can be loaded here. No reconstruction result or sample venue is fabricated.

## Requirements

- Node.js 20.19+ or 22.12+
- npm
- A modern desktop browser with WebGL

## Run locally

```bash
npm install
npm run dev
```

Open the local URL printed by Vite. Click **Load 3D model** and select a `.glb` file. For `.gltf`, keep all referenced `.bin` and texture files in their original relative paths; `.glb` is preferred for sharing.

## Build

```bash
npm run build
npm run preview
```

## Controls

- `W A S D`: move
- Mouse: look around (click the scene to lock pointer)
- `Esc`: release pointer

## Current limitations / next engineering tasks

1. Integrate a tested local reconstruction pipeline and document its exact version, commands, and licence.
2. Add floor-aware coordinate conventions and collision geometry; current movement is intentionally a basic free-roam controller.
3. Add scene bounds and safe movement constraints after real model scale/orientation are established.
4. Add POI metadata and spatial search in the Round 2 milestone.
5. Add obstacle-aware path planning and WebXR only after the Round 1 pipeline is stable.

## Submission reproducibility

Keep the original capture inputs in a `sample-data/` directory (subject to size/privacy constraints), plus a manifest describing capture device, app, settings, route, and preprocessing. Do not commit private indoor footage without the owner's consent. The final repository should include the reconstruction script/configuration and instructions to regenerate the model from the submitted sample inputs.
