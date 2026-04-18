# ForgeYT

![ForgeYT](media/forgeyt-logo.png)

Paste a YouTube URL. Get the audio file on your disk.

A small, local desktop app — no account, no cloud, no telemetry. Runs on Windows, macOS, and Linux.

**Download:** [latest release](https://github.com/liquid-releasing/forgeyt-releases/releases/latest) · **Community:** [Discord](https://discord.gg/sZWCqgxY)

---

## What it does

1. Paste a YouTube URL into the form.
2. Pick an audio format (MP3, M4A, WAV, Opus) and quality.
3. Click **Forge**.
4. The audio lands in your chosen folder.

Title, artist, and cover art (where available) are embedded as ID3 tags automatically.

## What it doesn't do

- No playlists, no batch URL lists, no channel scraping. One URL at a time.
- No video — audio only.
- No account, no sign-in, no data sent anywhere except YouTube itself.

If your workflow needs those features, you're probably looking for [yt-dlp](https://github.com/yt-dlp/yt-dlp) directly on the command line.

---

## Terms of use

> **Liquid Releasing ships this as a tool for users downloading content they have permission to access.**

YouTube's Terms of Service restrict downloading content without explicit permission. You are responsible for ensuring you have the right to download any file you fetch with ForgeYT — whether that's your own uploads, content under a Creative Commons license, public-domain material, or something where the rightsholder has granted you permission.

ForgeYT does not check these rights. We do not distribute copyrighted content. We ship a tool.

---

## Building from source

```bash
git clone https://github.com/liquid-releasing/forgeyt
cd forgeyt
pip install -r requirements.txt
pip install -r requirements-desktop.txt
python forgeyt.py
```

You'll need `ffmpeg` on your `PATH` when running from source. The packaged release bundles it.

## License

ForgeYT's own source code is released under the [MIT License](LICENSE).

Packaged releases bundle third-party software (ffmpeg, Streamlit, PyWebView, yt-dlp, etc.) that retains its own license. See [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md) for the full list.

**ForgeYT™** and **Liquid Releasing™** are trademarks of Liquid Releasing.

---

*© 2026 [Liquid Releasing](https://github.com/liquid-releasing). Written by human and Claude AI.*
