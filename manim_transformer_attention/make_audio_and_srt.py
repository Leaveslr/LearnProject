from __future__ import annotations

import subprocess
from pathlib import Path

from content import SEGMENTS


ROOT = Path(__file__).resolve().parent
AUDIO_DIR = ROOT / "assets" / "audio"
OUTPUT_DIR = ROOT / "outputs"


def srt_time(seconds: float) -> str:
    millis = round(seconds * 1000)
    hours = millis // 3_600_000
    millis %= 3_600_000
    minutes = millis // 60_000
    millis %= 60_000
    secs = millis // 1000
    millis %= 1000
    return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"


def make_srt() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    cursor = 0.0
    blocks = []
    for index, segment in enumerate(SEGMENTS, start=1):
        start = cursor
        transition = 0.35 if index < len(SEGMENTS) else 0.0
        end = cursor + float(segment["duration"]) + transition
        blocks.append(
            f"{index}\n{srt_time(start)} --> {srt_time(end)}\n{segment['subtitle']}\n"
        )
        cursor = end
    (OUTPUT_DIR / "transformer_attention.srt").write_text("\n".join(blocks), encoding="utf-8")


def make_audio() -> None:
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    for segment in SEGMENTS:
        target = AUDIO_DIR / f"seg_{segment['id']}.wav"
        if target.exists():
            continue
        temp_aiff = AUDIO_DIR / f"seg_{segment['id']}.aiff"
        subprocess.run(
            [
                "say",
                "-v",
                "Tingting",
                "-r",
                "175",
                "-o",
                str(temp_aiff),
                segment["subtitle"],
            ],
            check=True,
        )
        subprocess.run(
            ["ffmpeg", "-y", "-i", str(temp_aiff), "-ar", "44100", "-ac", "1", str(target)],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )


if __name__ == "__main__":
    make_srt()
    make_audio()
    print(f"Wrote subtitles to {OUTPUT_DIR / 'transformer_attention.srt'}")
    print(f"Wrote wav audio clips to {AUDIO_DIR}")
