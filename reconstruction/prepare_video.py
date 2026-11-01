"""Extract ordered RGB frames from a phone video using FFmpeg."""
import argparse
import shutil
import subprocess
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--fps", type=float, default=2.0)
    args = parser.parse_args()
    if not args.video.is_file():
        parser.error(f"Video not found: {args.video}")
    if args.fps <= 0:
        parser.error("--fps must be positive")
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise SystemExit("FFmpeg was not found on PATH. Install it or use still images directly.")
    args.out.mkdir(parents=True, exist_ok=True)
    pattern = args.out / "frame_%06d.jpg"
    cmd = [ffmpeg, "-hide_banner", "-loglevel", "error", "-i", str(args.video),
           "-vf", f"fps={args.fps}", "-q:v", "2", str(pattern)]
    subprocess.run(cmd, check=True)
    count = len(list(args.out.glob("frame_*.jpg")))
    print(f"Extracted {count} frames into {args.out}")
    if count < 20:
        print("WARNING: fewer than 20 frames; coverage may be insufficient.")

if __name__ == "__main__":
    main()
