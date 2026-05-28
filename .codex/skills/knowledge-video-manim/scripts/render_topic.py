from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def srt_time(seconds: float) -> str:
    millis = round(seconds * 1000)
    hours, millis = divmod(millis, 3_600_000)
    minutes, millis = divmod(millis, 60_000)
    secs, millis = divmod(millis, 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"


def make_assets(topic_path: Path, run_dir: Path, voice: str, rate: str) -> None:
    topic = json.loads(topic_path.read_text(encoding="utf-8"))
    audio_dir = run_dir / "audio"
    audio_dir.mkdir(parents=True, exist_ok=True)
    cursor = 0.0
    blocks = []
    for idx, segment in enumerate(topic["segments"], start=1):
        wav = audio_dir / f"seg_{idx:02d}.wav"
        if not wav.exists():
            aiff = audio_dir / f"seg_{idx:02d}.aiff"
            subprocess.run(["say", "-v", voice, "-r", rate, "-o", str(aiff), segment["subtitle"]], check=True)
            subprocess.run(["ffmpeg", "-y", "-i", str(aiff), "-ar", "44100", "-ac", "1", str(wav)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        transition = 0.35 if idx < len(topic["segments"]) else 0.0
        end = cursor + float(segment["duration"]) + transition
        blocks.append(f"{idx}\n{srt_time(cursor)} --> {srt_time(end)}\n{segment['subtitle']}\n")
        cursor = end
    (run_dir / f"{topic['slug']}.srt").write_text("\n".join(blocks), encoding="utf-8")


def render(topic_path: Path, quality: str, run_dir: Path) -> None:
    env = {
        **__import__("os").environ,
        "TOPIC_JSON": str(topic_path.resolve()),
        "RUN_DIR": str(run_dir.resolve()),
    }
    subprocess.run(
        [
            "manim",
            quality,
            str(ROOT / "generic_video.py"),
            "GenericKnowledgeVideo",
            "--media_dir",
            str(run_dir / "media"),
        ],
        check=True,
        env=env,
    )


def copy_final(topic_path: Path, run_dir: Path, quality_dir: str) -> Path:
    topic = json.loads(topic_path.read_text(encoding="utf-8"))
    src = run_dir / "media" / "videos" / "generic_video" / quality_dir / "GenericKnowledgeVideo.mp4"
    dst = run_dir / f"{topic['slug']}_{quality_dir}.mp4"
    dst.write_bytes(src.read_bytes())
    return dst


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("topic")
    parser.add_argument("--quality", default="-qm")
    parser.add_argument("--quality-dir", default="720p30")
    parser.add_argument("--voice", default="Tingting")
    parser.add_argument("--rate", default="175")
    args = parser.parse_args()

    topic_path = Path(args.topic).resolve()
    topic = json.loads(topic_path.read_text(encoding="utf-8"))
    run_dir = ROOT / "outputs" / topic["slug"]
    run_dir.mkdir(parents=True, exist_ok=True)
    make_assets(topic_path, run_dir, args.voice, args.rate)
    render(topic_path, args.quality, run_dir)
    final = copy_final(topic_path, run_dir, args.quality_dir)
    print(final)


if __name__ == "__main__":
    main()
