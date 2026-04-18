# Copyright (c) 2026 Liquid Releasing. Licensed under the MIT License.

"""About metadata for ForgeYT.

Single source of truth for version, credits, and license content shown in:
  - Sidebar "About" expander
  - PyWebView Help -> About menu (desktop mode)
"""

from __future__ import annotations

__all__ = [
    "APP_NAME",
    "ABOUT_MARKDOWN",
    "TAGLINE",
    "VERSION",
    "about_title",
    "about_text",
]

# Alpha versioning: 0.0.x until first stable release.
VERSION = "0.0.1"
APP_NAME = "ForgeYT"
TAGLINE = "Paste a YouTube URL. Get the audio file on your disk."


ABOUT_MARKDOWN = f"""
### {APP_NAME} {VERSION}

{TAGLINE}

A small local desktop tool from Liquid Releasing. No account, no cloud,
no telemetry. Audio lands on your disk, with embedded title / artist /
cover art where available.

---

#### Open source credits

ForgeYT builds on the significant work of the open source community:

- **[yt-dlp](https://github.com/yt-dlp/yt-dlp)** — extracts media URLs and
  downloads content. Public domain (Unlicense).
- **[FFmpeg](https://ffmpeg.org)** — audio decoding and transcoding.
  LGPL 2.1+ / GPL 2+.
- **[Streamlit](https://streamlit.io)** — application UI framework. Apache 2.0.
- **[PyWebView](https://pywebview.flowrl.com)** — native desktop window
  wrapper. BSD 3-Clause.
- **[mutagen](https://mutagen.readthedocs.io)** — ID3 tag handling. GPL 2.

Full third-party license text is bundled with the release under `LICENSES/`.

#### AI assistance

Written by human and Claude AI (Anthropic).

---

#### Community

Questions, bug reports, and feedback welcome in
[our Discord](https://discord.gg/sZWCqgxY).

---

#### License

**{APP_NAME}(TM)** is a trademark of Liquid Releasing.

(c) 2026 [Liquid Releasing](https://github.com/liquid-releasing).
Licensed under the [MIT License](https://github.com/liquid-releasing/forgeyt/blob/main/LICENSE).

#### Terms of use

> **Liquid Releasing ships this as a tool for users downloading content they
> have permission to access.** You are responsible for ensuring you have the
> right to download any file you fetch with ForgeYT.
"""


def about_title() -> str:
    """Short title for dialogs: 'ForgeYT 0.0.1'."""
    return f"{APP_NAME} {VERSION}"


def about_text() -> str:
    """Plain-text about blurb for native message boxes."""
    return (
        f"{APP_NAME} {VERSION}\n"
        f"{TAGLINE}\n\n"
        "Open source credits:\n"
        "  - yt-dlp (Unlicense)\n"
        "  - FFmpeg (LGPL/GPL)\n"
        "  - Streamlit (Apache 2.0)\n"
        "  - PyWebView (BSD 3-Clause)\n"
        "  - mutagen (GPL 2)\n\n"
        "Written by human and Claude AI (Anthropic).\n\n"
        "Community: discord.gg/sZWCqgxY\n\n"
        f"{APP_NAME} is a trademark of Liquid Releasing.\n"
        "(c) 2026 Liquid Releasing. MIT License.\n"
        "github.com/liquid-releasing/forgeyt\n\n"
        "Download only content you have permission to access."
    )
