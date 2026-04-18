# -*- mode: python ; coding: utf-8 -*-
#
# PyInstaller spec for ForgeYT desktop app.
#
# Build with:
#     pyinstaller ForgeYT.spec --clean
#
# Output: dist/ForgeYT/ForgeYT.exe (Windows) / ForgeYT.app (macOS) / ForgeYT (Linux).

import sys
from pathlib import Path
from PyInstaller.utils.hooks import (
    collect_all,
    collect_data_files,
    collect_submodules,
    copy_metadata,
)

SPEC_DIR = Path(SPECPATH).resolve()

# ── Streamlit collection (runtime-discovered dist-info, data files, etc.) ──
streamlit_datas, streamlit_binaries, streamlit_hiddenimports = collect_all("streamlit")
streamlit_datas += copy_metadata("streamlit")

# imageio-ffmpeg bundles a platform-specific ffmpeg binary in its package
# data dir; collect_all pulls the binary into the bundle.
ffmpeg_datas, ffmpeg_binaries, ffmpeg_hiddenimports = collect_all("imageio_ffmpeg")

# yt-dlp has many dynamic imports for site extractors; collect_submodules.
ytdlp_hiddenimports = collect_submodules("yt_dlp")

# Other packages that use importlib.metadata at runtime
extra_metadata = []
for pkg in (
    "streamlit",
    "yt-dlp",
    "mutagen",
    "requests",
    "altair",
    "pyarrow",
    "numpy",
    "pandas",
    "tornado",
    "click",
    "rich",
    "imageio-ffmpeg",
):
    try:
        extra_metadata += copy_metadata(pkg)
    except Exception:
        pass

hidden_imports = list(streamlit_hiddenimports) + list(ffmpeg_hiddenimports) + list(ytdlp_hiddenimports) + [
    "streamlit.web.cli",
    "streamlit.runtime.scriptrunner.magic_funcs",
    "streamlit.runtime.caching",
    "streamlit.runtime.state",
    "streamlit.components.v1",
    "altair",
    "pyarrow",
    "pydeck",
    "watchdog",
    "importlib_metadata",
    "mutagen",
    "requests",
    "imageio_ffmpeg",
    "forgeyt_core",
    "forgeyt_core.about",
    "forgeyt_core.downloader",
]

# ── Data files ─────────────────────────────────────────────────────────
datas = list(streamlit_datas) + list(ffmpeg_datas) + list(extra_metadata)

# ForgeYT's own source package + ui.py
datas += [
    (str(SPEC_DIR / "forgeyt_core"), "forgeyt_core"),
    (str(SPEC_DIR / "ui.py"), "."),
    (str(SPEC_DIR / "media"), "media"),
    (str(SPEC_DIR / ".streamlit" / "config.toml"), ".streamlit"),
]

# License files — ship ours + the third-party list next to the exe
datas += [
    (str(SPEC_DIR / "LICENSE"), "."),
    (str(SPEC_DIR / "THIRD_PARTY_LICENSES.md"), "."),
    (str(SPEC_DIR / "README.md"), "."),
]

# Platform-specific app icon
if sys.platform == "win32":
    _icon = str(SPEC_DIR / "media" / "forgeyt.ico")
elif sys.platform == "darwin":
    _icns = SPEC_DIR / "media" / "forgeyt.icns"
    _icon = str(_icns) if _icns.exists() else None
else:
    _icon = None

binaries = list(streamlit_binaries) + list(ffmpeg_binaries)

block_cipher = None

a = Analysis(
    ["forgeyt.py"],
    pathex=[str(SPEC_DIR)],
    binaries=binaries,
    datas=datas,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        "tkinter",
        "PyQt5",
        "PyQt6",
        "PySide2",
        "PySide6",
        "notebook",
        "jupyter",
        "IPython",
        "pytest",
        "sphinx",
        "scipy",
        "sklearn",
        "tensorflow",
        "torch",
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="ForgeYT",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=_icon,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name="ForgeYT",
)

if sys.platform == "darwin":
    app = BUNDLE(
        coll,
        name="ForgeYT.app",
        icon=_icon,
        bundle_identifier="com.liquidreleasing.forgeyt",
    )
