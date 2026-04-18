"""ForgeYT core — yt-dlp wrapper and metadata helpers."""

from .about import ABOUT_MARKDOWN, APP_NAME, TAGLINE, VERSION, about_title
from .downloader import DownloadOptions, DownloadResult, download_audio, probe_url

__all__ = [
    "ABOUT_MARKDOWN",
    "APP_NAME",
    "DownloadOptions",
    "DownloadResult",
    "TAGLINE",
    "VERSION",
    "about_title",
    "download_audio",
    "probe_url",
]
