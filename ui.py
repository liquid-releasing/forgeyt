# Copyright (c) 2026 Liquid Releasing. Licensed under the MIT License.

"""ForgeYT Streamlit UI — queue-based single-worker download manager."""

from __future__ import annotations

import os
import subprocess
import sys
import uuid
from pathlib import Path

import streamlit as st

# Resolve bundled media paths absolutely. Works in both dev (script CWD
# may be wrong) and PyInstaller bundle (streamlit runs from a temp dir).
_APP_DIR = Path(__file__).parent.resolve()
_MEDIA = _APP_DIR / "media"

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


# ── Helpers ───────────────────────────────────────────────────────────
def _default_output_dir() -> Path:
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
    port = _bridge_port()
    if port == 0:
        return None
    import requests  # noqa: PLC0415
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


STATUS_ICON = {
    "pending": "⏸",
    "downloading": "⏳",
    "done": "✅",
    "failed": "❌",
}


def _job_summary(job: dict) -> str:
    title = job.get("title")
    if title:
        label = title if len(title) <= 60 else title[:57] + "…"
    else:
        label = job["url"]
        if len(label) > 60:
            label = label[:57] + "…"
    return f"{STATUS_ICON[job['status']]} **{label}**  ·  {job['audio_format']} / {job['quality']}"


# ── Sidebar ───────────────────────────────────────────────────────────
with st.sidebar:
    # 60% width, centered via [1, 3, 1] column spacers
    _sl, _sc, _sr = st.columns([1, 3, 1])
    with _sc:
        st.image(str(_MEDIA / "forgeyt_icon.png"), width="stretch")
    st.caption(TAGLINE)
    st.caption(f"Version {VERSION}")

    with st.expander(f"About {APP_NAME} {VERSION}"):
        st.markdown(ABOUT_MARKDOWN)

    # ── Footer ────────────────────────────────────────────────────────
    st.divider()
    _fl, _fc, _fr = st.columns([1, 3, 1])
    with _fc:
        st.image(str(_MEDIA / "liquid-releasing-logo.svg"), width="stretch")
    st.markdown(
        """
        <center style="font-size:0.85em; line-height:1.6;">
        © 2026 <a href="https://github.com/liquid-releasing" target="_blank">Liquid Releasing</a><br>
        <a href="https://github.com/liquid-releasing/forgeyt" target="_blank">ForgeYT</a>
        &nbsp;·&nbsp;
        <a href="https://github.com/liquid-releasing/forgeyt/blob/main/LICENSE" target="_blank">MIT License</a>
        &nbsp;·&nbsp;
        <a href="https://discord.gg/sZWCqgxY" target="_blank">Discord</a>
        </center>
        """,
        unsafe_allow_html=True,
    )

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

# ── Session state ─────────────────────────────────────────────────────
if "queue" not in st.session_state:
    st.session_state["queue"] = []  # list[dict]
if "output_dir" not in st.session_state:
    st.session_state["output_dir"] = str(_default_output_dir())
if "_url_input_nonce" not in st.session_state:
    # Used to force-clear the URL field after adding to queue
    st.session_state["_url_input_nonce"] = 0
if "processing" not in st.session_state:
    st.session_state["processing"] = False

# Recover from a run that was interrupted mid-download: a widget interaction
# during the loop raises RerunException and leaves one item stuck with
# status="downloading". If we see that on a run with processing=True, the
# previous run was interrupted — reset the stuck item and clear the flag.
# If processing=True but nothing is stuck, we just armed processing on the
# previous run and this run should execute the download loop — leave it set.
_interrupted_titles: list[str] = []
if st.session_state["processing"]:
    _stuck = [j for j in st.session_state["queue"] if j["status"] == "downloading"]
    if _stuck:
        for _j in _stuck:
            _j["status"] = "pending"
            _j["error"] = None
            _interrupted_titles.append(_j.get("title") or _j["url"])
        st.session_state["processing"] = False

if _interrupted_titles:
    names = ", ".join(f"**{t}**" for t in _interrupted_titles)
    st.warning(
        f"The previous batch was interrupted while downloading {names}. "
        f"Reset to pending — click **Start downloads** again to retry. "
        f"Tip: don't interact with the form while a batch is running.",
        icon="⚠️",
    )

# ── Add to queue form ─────────────────────────────────────────────────
_locked = st.session_state["processing"]
_lock_help = (
    "A batch is currently downloading. Finish the batch, or cancel it by "
    "closing the window and relaunching, before adding more items."
) if _locked else None

url_key = f"url_{st.session_state['_url_input_nonce']}"

url = st.text_input(
    "YouTube URL",
    placeholder="https://www.youtube.com/watch?v=...",
    key=url_key,
    disabled=_locked,
    help=_lock_help,
)

col_fmt, col_q = st.columns(2)
with col_fmt:
    audio_format = st.selectbox("Format", ["mp3", "m4a", "opus", "wav"], index=0, disabled=_locked)
with col_q:
    quality_options = {"Best available": "best", "192 kbps": "192", "128 kbps": "128", "96 kbps": "96"}
    quality_label = st.selectbox("Quality", list(quality_options.keys()), index=0, disabled=_locked)
    quality = quality_options[quality_label]

# Output folder
out_col1, out_col2 = st.columns([4, 1])
with out_col1:
    st.session_state["output_dir"] = st.text_input(
        "Output folder",
        value=st.session_state["output_dir"],
        disabled=_locked,
    )
with out_col2:
    st.write("")
    st.write("")
    if _desktop_mode() and st.button("Browse…", use_container_width=True, disabled=_locked):
        picked = _pick_folder(st.session_state["output_dir"])
        if picked:
            st.session_state["output_dir"] = picked
            st.rerun()

embed_tags = st.checkbox("Embed title / artist / cover art", value=True, disabled=_locked)

if st.button(
    "🔨 Forge",
    type="primary",
    use_container_width=True,
    disabled=_locked or not url,
    help=_lock_help,
):
    url_clean = url.strip()
    title = None
    uploader = None
    duration = None
    with st.spinner("Looking up title…"):
        try:
            info = probe_url(url_clean)
            title = info.get("title")
            uploader = info.get("uploader")
            duration = info.get("duration")
        except Exception:
            # Couldn't fetch metadata now — fall back to the URL; we'll retry
            # during download. Keeps transient network hiccups from blocking queueing.
            pass

    st.session_state["queue"].append(
        {
            "id": str(uuid.uuid4()),
            "url": url_clean,
            "title": title,
            "uploader": uploader,
            "duration": duration,
            "audio_format": audio_format,
            "quality": quality,
            "output_dir": st.session_state["output_dir"],
            "embed_tags": embed_tags,
            "status": "pending",
            "result": None,
            "error": None,
        }
    )
    st.session_state["_url_input_nonce"] += 1
    st.rerun()

# ── Queue panel ───────────────────────────────────────────────────────
queue = st.session_state["queue"]
pending = [j for j in queue if j["status"] == "pending"]
running = [j for j in queue if j["status"] == "downloading"]
done = [j for j in queue if j["status"] in ("done", "failed")]

if queue:
    st.divider()
    parts = [f"{len(pending)} pending"]
    if running:
        parts.append(f"{len(running)} running")
    parts.append(f"{len(done)} complete")
    st.subheader(f"Queue ({', '.join(parts)})")

    for i, job in enumerate(queue):
        cols = st.columns([10, 1])
        with cols[0]:
            st.write(_job_summary(job))
            parts = []
            if job.get("uploader"):
                parts.append(job["uploader"])
            if job.get("duration"):
                mins, secs = divmod(int(job["duration"]), 60)
                parts.append(f"{mins}:{secs:02d}")
            if parts:
                st.caption(" · ".join(parts))
            if job["status"] == "done" and job["result"]:
                r = job["result"]
                st.caption(f"→ `{r.output_path}`")
            elif job["status"] == "failed":
                st.caption(f"Error: {job['error']}")
        with cols[1]:
            if job["status"] == "pending":
                if st.button(
                    "✕",
                    key=f"rm_{job['id']}",
                    help=_lock_help or "Remove from queue",
                    disabled=_locked,
                ):
                    st.session_state["queue"] = [j for j in queue if j["id"] != job["id"]]
                    st.rerun()

    col_a, col_b = st.columns(2)
    with col_a:
        start_clicked = st.button(
            f"▶ Start downloads ({len(pending)})",
            type="primary",
            use_container_width=True,
            disabled=_locked or not pending,
            help=_lock_help,
        )
    with col_b:
        if st.button(
            "Clear completed",
            use_container_width=True,
            disabled=_locked or not done,
            help=_lock_help,
        ):
            st.session_state["queue"] = [j for j in queue if j["status"] == "pending"]
            st.rerun()
else:
    start_clicked = False

# ── Arm the processing flag and rerun — ensures every widget is rendered
#    disabled on the run that actually executes downloads ────────────────
if start_clicked and pending and not _locked:
    st.session_state["processing"] = True
    st.rerun()

# ── Download worker (synchronous, runs only when locked) ──────────────
if _locked and pending:
    st.divider()
    st.subheader("Forging…")
    st.info(
        "Downloads are running. The form is disabled until this batch "
        "finishes. Click **Cancel downloads** to stop now — the in-progress "
        "item resets to pending and the rest stay queued.",
        icon="⏳",
    )
    if st.button(
        "✕ Cancel downloads",
        key="cancel_downloads",
        help="Interrupt the current download. Pending items stay queued.",
    ):
        # Click triggers a rerun; on re-entry the interrupt-recovery code
        # resets the in-flight item to pending and clears the processing flag.
        st.rerun()

    for job in pending:
        output_dir = Path(job["output_dir"]).expanduser()
        job["status"] = "downloading"

        item = st.status(f"⏳ {job['url']}", expanded=True)
        progress_bar = item.progress(0.0, text="Starting…")

        def _progress(d: dict, bar=progress_bar) -> None:
            phase = d.get("status", "")
            if phase == "downloading":
                total = d.get("total_bytes") or d.get("total_bytes_estimate") or 0
                downloaded = d.get("downloaded_bytes") or 0
                if total > 0:
                    pct = min(downloaded / total, 1.0)
                    bar.progress(pct, text=f"Downloading… {pct * 100:.0f}%")
                else:
                    bar.progress(0.5, text="Downloading…")
            elif phase == "finished":
                bar.progress(0.95, text="Transcoding audio…")

        opts = DownloadOptions(
            url=job["url"],
            output_dir=output_dir,
            audio_format=job["audio_format"],  # type: ignore[arg-type]
            quality=job["quality"],  # type: ignore[arg-type]
            embed_metadata=job["embed_tags"],
            embed_thumbnail=job["embed_tags"],
        )

        result = download_audio(opts, progress_cb=_progress)

        if result.success and result.output_path:
            job["status"] = "done"
            job["result"] = result
            progress_bar.progress(1.0, text="Done")
            item.update(label=f"✅ {result.title}", state="complete", expanded=False)
            item.write(f"**{result.title}**")
            if result.uploader:
                item.write(f"by *{result.uploader}*")
            item.write(f"Saved to: `{result.output_path}`")
        else:
            job["status"] = "failed"
            job["error"] = result.error or "Unknown failure."
            item.update(label=f"❌ Failed: {job['url']}", state="error", expanded=True)
            item.write(f"**Error:** {job['error']}")

    st.session_state["processing"] = False
    st.success(f"Done — processed {len(pending)} item(s).")
    if st.button("Open output folder"):
        _open_folder(Path(st.session_state["output_dir"]).expanduser())
    st.rerun()
