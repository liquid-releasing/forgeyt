# Copyright (c) 2026 Liquid Releasing. Licensed under the MIT License.

"""ForgeYT Streamlit UI — one page, one URL, one audio file out."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import streamlit as st

from forgeyt_core import (
    ABOUT_MARKDOWN,
    APP_NAME,
    TAGLINE,
    VERSION,
    DownloadOptions,
    download_audio,
    probe_url,
)

# ── Page setup ────────────────────────────────────────────────────────
st.set_page_config(
    page_title=f"{APP_NAME} {VERSION}",
    page_icon="🔨",
    layout="centered",
)


def _default_output_dir() -> Path:
    """User Music folder / forgeyt subfolder."""
    home = Path.home()
    for candidate in (home / "Music", home / "Documents" / "Music"):
        if candidate.exists():
            return candidate / "forgeyt"
    return home / "forgeyt"


def _desktop_mode() -> bool:
    return os.environ.get("FORGEYT_DESKTOP") == "1"


def _bridge_port() -> int:
    return int(os.environ.get("FORGEYT_BRIDGE_PORT", "0"))


def _pick_folder(current: str) -> str | None:
    """Ask the PyWebView launcher for a folder picker via the HTTP bridge.
    Only works in desktop mode; returns None if picker is unavailable or
    the user cancels.
    """
    port = _bridge_port()
    if port == 0:
        return None
    import requests  # noqa: PLC0415 — only imported in desktop mode
    try:
        resp = requests.get(
            f"http://127.0.0.1:{port}/pick-folder",
            params={"initial": current},
            timeout=120,
        )
        if resp.ok and resp.text.strip():
            return resp.text.strip()
    except Exception:
        return None
    return None


def _open_folder(path: Path) -> None:
    """Reveal a folder in the OS file manager."""
    p = str(path)
    try:
        if sys.platform == "win32":
            os.startfile(p)  # type: ignore[attr-defined]
        elif sys.platform == "darwin":
            subprocess.Popen(["open", p])
        else:
            subprocess.Popen(["xdg-open", p])
    except Exception:
        pass


# ── Sidebar ───────────────────────────────────────────────────────────
with st.sidebar:
    st.image("media/forgeyt-logo.png", width=200)
    st.caption(f"{TAGLINE}")
    st.caption(f"Version {VERSION}")

    with st.expander(f"About {APP_NAME} {VERSION}"):
        st.markdown(ABOUT_MARKDOWN)

# ── First-run disclaimer ──────────────────────────────────────────────
if not st.session_state.get("_forgeyt_accepted_terms"):
    st.warning(
        "**Liquid Releasing ships ForgeYT as a tool for users downloading "
        "content they have permission to access.** You are responsible for "
        "ensuring you have the right to download any file you fetch. "
        "ForgeYT does not check these rights.",
        icon="⚠️",
    )
    if st.button("I understand — continue"):
        st.session_state["_forgeyt_accepted_terms"] = True
        st.rerun()
    st.stop()

# ── Main form ─────────────────────────────────────────────────────────
st.title(f"{APP_NAME}")
st.caption(TAGLINE)

url = st.text_input(
    "YouTube URL",
    placeholder="https://www.youtube.com/watch?v=...",
    key="url",
)

col_fmt, col_q = st.columns(2)
with col_fmt:
    audio_format = st.selectbox("Format", ["mp3", "m4a", "opus", "wav"], index=0)
with col_q:
    quality_options = {"Best available": "best", "192 kbps": "192", "128 kbps": "128", "96 kbps": "96"}
    quality_label = st.selectbox("Quality", list(quality_options.keys()), index=0)
    quality = quality_options[quality_label]

# Output folder
if "output_dir" not in st.session_state:
    st.session_state["output_dir"] = str(_default_output_dir())

out_col1, out_col2 = st.columns([4, 1])
with out_col1:
    st.session_state["output_dir"] = st.text_input(
        "Output folder",
        value=st.session_state["output_dir"],
    )
with out_col2:
    st.write("")  # spacer to align with text input
    st.write("")
    if _desktop_mode() and st.button("Browse…", use_container_width=True):
        picked = _pick_folder(st.session_state["output_dir"])
        if picked:
            st.session_state["output_dir"] = picked
            st.rerun()

embed_tags = st.checkbox("Embed title / artist / cover art", value=True)

# ── Forge! ────────────────────────────────────────────────────────────
if st.button("🔨 Forge", type="primary", use_container_width=True, disabled=not url):
    output_dir = Path(st.session_state["output_dir"]).expanduser()

    status = st.status("Forging…", expanded=True)
    progress_bar = status.progress(0.0, text="Starting…")

    def _progress(d: dict) -> None:
        phase = d.get("status", "")
        if phase == "downloading":
            total = d.get("total_bytes") or d.get("total_bytes_estimate") or 0
            done = d.get("downloaded_bytes") or 0
            if total > 0:
                pct = min(done / total, 1.0)
                progress_bar.progress(pct, text=f"Downloading… {pct * 100:.0f}%")
            else:
                progress_bar.progress(0.5, text="Downloading…")
        elif phase == "finished":
            progress_bar.progress(0.95, text="Transcoding audio…")

    opts = DownloadOptions(
        url=url,
        output_dir=output_dir,
        audio_format=audio_format,  # type: ignore[arg-type]
        quality=quality,  # type: ignore[arg-type]
        embed_metadata=embed_tags,
        embed_thumbnail=embed_tags,
    )

    result = download_audio(opts, progress_cb=_progress)

    if result.success and result.output_path:
        progress_bar.progress(1.0, text="Done")
        status.update(label="Forged!", state="complete", expanded=True)
        status.write(f"**{result.title}**")
        if result.uploader:
            status.write(f"by *{result.uploader}*")
        status.write(f"Saved to: `{result.output_path}`")
        if st.button("Open folder"):
            _open_folder(result.output_path.parent)
    else:
        status.update(label="Failed", state="error", expanded=True)
        status.write(f"**Error:** {result.error or 'Unknown failure.'}")
