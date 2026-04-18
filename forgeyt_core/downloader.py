# Copyright (c) 2026 Liquid Releasing. Licensed under the MIT License.

"""yt-dlp wrapper — one URL in, one audio file out."""

from __future__ import annotations

import os
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Literal, Optional

AudioFormat = Literal["mp3", "m4a", "opus", "wav"]
Quality = Literal["best", "192", "128", "96"]


@dataclass
class DownloadOptions:
    url: str
    output_dir: Path
    audio_format: AudioFormat = "mp3"
    quality: Quality = "best"
    embed_metadata: bool = True
    embed_thumbnail: bool = True


@dataclass
class DownloadResult:
    success: bool
    output_path: Optional[Path] = None
    title: Optional[str] = None
    uploader: Optional[str] = None
    duration_s: Optional[float] = None
    error: Optional[str] = None
    info: dict = field(default_factory=dict)


def _locate_ffmpeg() -> Optional[str]:
    """Find ffmpeg — prefer the imageio-ffmpeg bundled binary, fall back to PATH."""
    try:
        import imageio_ffmpeg  # noqa: PLC0415
        path = imageio_ffmpeg.get_ffmpeg_exe()
        if path and Path(path).exists():
            return path
    except Exception:
        pass
    return shutil.which("ffmpeg")


def probe_url(url: str, timeout_s: int = 8) -> dict:
    """Fetch metadata without downloading. Raises on failure."""
    import yt_dlp

    opts = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
        "socket_timeout": timeout_s,
        "noplaylist": True,
        "playlist_items": "1",
        "extractor_retries": 1,
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        return ydl.extract_info(url, download=False)


def download_audio(
    opts: DownloadOptions,
    progress_cb: Optional[Callable[[dict], None]] = None,
) -> DownloadResult:
    """Download one URL as audio.

    progress_cb receives yt-dlp's progress dict: status, downloaded_bytes,
    total_bytes, speed, eta. Runs synchronously on the caller's thread.
    """
    import yt_dlp

    opts.output_dir.mkdir(parents=True, exist_ok=True)

    ffmpeg_path = _locate_ffmpeg()
    if ffmpeg_path is None:
        return DownloadResult(
            success=False,
            error="FFmpeg not found. Install ffmpeg and ensure it is on PATH.",
        )

    postprocessors = [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": opts.audio_format,
            "preferredquality": "0" if opts.quality == "best" else opts.quality,
        }
    ]
    if opts.embed_metadata:
        postprocessors.append({"key": "FFmpegMetadata"})
    if opts.embed_thumbnail and opts.audio_format in ("mp3", "m4a", "opus"):
        postprocessors.append({"key": "EmbedThumbnail"})

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": str(opts.output_dir / "%(title)s.%(ext)s"),
        "postprocessors": postprocessors,
        "writethumbnail": opts.embed_thumbnail,
        "ffmpeg_location": ffmpeg_path,
        "noplaylist": True,   # URLs like ?v=X&list=Y should only grab the single video
        "playlist_items": "1",
        "noprogress": True,   # we route through progress_hooks instead
        "quiet": True,
        "no_warnings": True,
    }
    if progress_cb is not None:
        ydl_opts["progress_hooks"] = [progress_cb]

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(opts.url, download=True)
    except Exception as exc:  # noqa: BLE001 — surface the user-facing error
        return DownloadResult(success=False, error=str(exc))

    title = info.get("title", "audio")
    final_filename = _find_output_file(opts.output_dir, title, opts.audio_format)

    return DownloadResult(
        success=True,
        output_path=final_filename,
        title=title,
        uploader=info.get("uploader"),
        duration_s=info.get("duration"),
        info=info,
    )


def _find_output_file(output_dir: Path, title: str, ext: str) -> Optional[Path]:
    """Best-effort locate the final file after post-processing.

    yt-dlp sanitizes the title for the filename; we search for matching
    extension newest-first rather than trying to replicate its sanitizer.
    """
    matches = sorted(output_dir.glob(f"*.{ext}"), key=os.path.getmtime, reverse=True)
    return matches[0] if matches else None
