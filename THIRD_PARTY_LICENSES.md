# Third-Party Licenses

ForgeYT's own source code is released under the [MIT License](LICENSE).

Packaged releases of ForgeYT bundle third-party software that retains its own license. This file lists each dependency, its license, and where to find the full license text.

---

## Bundled binaries

### FFmpeg

- **License:** LGPL 2.1 (or GPL 2 if built with GPL-licensed codecs)
- **Project:** [ffmpeg.org](https://ffmpeg.org)
- **License text:** [ffmpeg.org/legal.html](https://www.ffmpeg.org/legal.html)
- **Used for:** audio decoding and transcoding of downloaded media.
- **Packaged releases** include a copy of the applicable ffmpeg license alongside the `ffmpeg` executable in the distribution.

## Python dependencies

### yt-dlp

- **License:** The Unlicense (public domain)
- **Project:** [github.com/yt-dlp/yt-dlp](https://github.com/yt-dlp/yt-dlp)
- **Used for:** extracting media URLs and downloading content.

### Streamlit

- **License:** Apache License 2.0
- **Project:** [streamlit.io](https://streamlit.io)
- **License text:** [github.com/streamlit/streamlit/blob/develop/LICENSE](https://github.com/streamlit/streamlit/blob/develop/LICENSE)
- **Used for:** the application UI framework.

### pywebview

- **License:** BSD 3-Clause
- **Project:** [pywebview.flowrl.com](https://pywebview.flowrl.com)
- **License text:** [github.com/r0x0r/pywebview/blob/master/LICENSE](https://github.com/r0x0r/pywebview/blob/master/LICENSE)
- **Used for:** the native desktop window wrapper around the Streamlit UI.

### mutagen

- **License:** GPL 2
- **Project:** [mutagen.readthedocs.io](https://mutagen.readthedocs.io)
- **Used for:** reading and writing ID3 tags on the downloaded audio files.

### requests

- **License:** Apache License 2.0
- **Project:** [requests.readthedocs.io](https://requests.readthedocs.io)
- **Used for:** fetching cover-art thumbnails for ID3 embedding.

### psutil

- **License:** BSD 3-Clause
- **Project:** [github.com/giampaolo/psutil](https://github.com/giampaolo/psutil)
- **Used for:** process lifecycle management in the desktop launcher.

### PyInstaller

- **License:** GPL 2 with runtime exception (the exception permits bundled binaries to use any license)
- **Project:** [pyinstaller.org](https://www.pyinstaller.org)
- **Used for:** building the packaged desktop release. Runtime exception means the packaged app is not restricted to GPL.

---

Full license texts for each dependency are included in the packaged release under `LICENSES/`.
