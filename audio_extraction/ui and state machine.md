Bruce, absolutely — you can pair your CLI with a **clean, industrial‑grade UI** that mirrors the simplicity of your workflow:  
**paste URL → download audio → store metadata → optionally process playlists**.

Below is a **full UI proposal** that fits your engineering style: modular, deterministic, and automation‑friendly. It’s intentionally minimal so it doesn’t compete with your Forge UI aesthetic, but it still feels like a proper tool.

---

# 🔥 **YOUTUBE PREMIUM AUDIO DOWNLOADER — UI PROPOSAL**  
### *A compact desktop UI that wraps your CLI pipeline.*

This UI is designed to sit on top of your CLI logic without replacing it.  
Think of it as a **thin orchestration layer**: the UI triggers the CLI, displays progress, and stores metadata.

---

# 🧱 **1. Layout Overview**

### **Main Window (600×420)**  
Clean, single‑column layout:

```
┌──────────────────────────────────────────────┐
│  YouTube Premium Audio Downloader            │
├──────────────────────────────────────────────┤

│  VIDEO URL                                   │
│  [ https://www.youtube.com/watch?v=...    ]  │

│  OUTPUT FORMAT                               │
│  (•) MP3   ( ) WAV   ( ) Original M4A        │

│  METADATA                                    │
│  Title:        [ auto-filled ]               │
│  Channel:      [ auto-filled ]               │
│  Duration:     [ auto-filled ]               │
│  Playlist:     [ auto-filled if applicable ] │

│  DOWNLOAD LOCATION                            │
│  [ ./sounds/ ]   (Browse)                    │

│  ACTIONS                                      │
│  [ Download Audio ]                           │
│  [ Download Playlist ]                        │

│  STATUS                                        │
│  ✔ Ready                                       │
└──────────────────────────────────────────────┘
```

---

# 🔵 **2. Core UI Sections**

## **A. URL Input**
A single text field:

- Paste a YouTube URL  
- Auto‑detects:
  - video ID  
  - playlist ID  
  - channel URL  
  - shorts URL  
  - music.youtube.com URLs  

When the user pastes a URL:

- UI calls CLI: `yt-audio get-metadata <url>`
- Fills metadata fields automatically

---

## **B. Output Format Selector**
Radio buttons:

- MP3 (default)
- WAV
- Original M4A/WebM

This maps directly to CLI flags:

```
--mp3
--wav
--no-convert
```

---

## **C. Metadata Panel**
Auto‑filled fields:

- Title  
- Channel  
- Duration  
- Playlist name (if applicable)  

Stored in:

```
./sounds/<video-id>.json
```

Metadata includes:

```
{
  "video_id": "...",
  "title": "...",
  "channel": "...",
  "duration": "...",
  "source_url": "...",
  "downloaded_at": "...",
  "format": "mp3"
}
```

---

## **D. Download Location**
Defaults to:

```
./sounds/
```

User can override.

Maps to CLI:

```
--output-dir <path>
```

---

## **E. Actions**
Two buttons:

### **1. Download Audio**
Triggers:

```
yt-audio get <url> --mp3
```

UI shows:

- Progress bar  
- Status messages  
- Final success indicator  

### **2. Download Playlist**
Triggers:

```
yt-audio playlist <playlist-url> --mp3
```

UI iterates through each video:

- Fetch metadata  
- Download audio  
- Save metadata  
- Update progress  

---

## **F. Status Bar**
Shows:

- ✔ Ready  
- ⏳ Downloading…  
- 🔄 Converting…  
- 🔥 Fallback capture active  
- ❌ Error (with message)  

---

# 🟧 **3. Optional Advanced Panel (Collapsible)**

```
[ Advanced ▼ ]

OAuth Status:  Logged in as <email>
Token Expires:  2026-04-12 14:22
Fallback Mode:  Auto
Bitrate:        320 kbps
Normalize:      Off
```

This maps directly to your config file.

---

# 🔥 **4. Playlist Mode UI**

When a playlist URL is detected:

```
Playlist:  “My Favorite Tracks”
Videos:    42

[ Download Entire Playlist ]
```

Progress view:

```
Downloading 3 / 42
[███████---------]
Current: Song Title
```

Metadata stored as:

```
./sounds/playlist-<id>.json
```

---

# 🟦 **5. UI → CLI Mapping**

| UI Action | CLI Command |
|----------|-------------|
| Paste URL | `yt-audio get-metadata <url>` |
| Download Audio | `yt-audio get <url> --mp3` |
| Download Playlist | `yt-audio playlist <playlist-url>` |
| Change output folder | `--output-dir <path>` |
| Change format | `--mp3`, `--wav`, `--no-convert` |
| Fallback mode | `--fallback` |
| Refresh OAuth | `yt-audio login` |

---

# 🧨 **6. Stretch Goal: Playlist Extraction Logic**

UI detects playlist URLs:

- `youtube.com/playlist?list=...`
- `music.youtube.com/playlist?list=...`

CLI runs:

```
yt-audio playlist <playlist-id>
```

UI shows:

- Total videos  
- Progress  
- Per‑video metadata  
- Errors (skipped videos)  

---

# 🏁 **7. Why this UI works**

- Minimal cognitive load  
- Mirrors your CLI architecture  
- Easy to automate  
- Easy to extend  
- Perfect for a small desktop app  
- Works with your Premium OAuth flow  
- Supports playlist extraction cleanly  

---

If you want, I can now generate:

### ✔ A **pixel‑perfect UI mockup**  
### ✔ A **component library for this UI**  
### ✔ A **state machine for the UI itself**  
### ✔ A **UX flow diagram**  
### ✔ A **folder structure for the UI project**  

Just tell me where you want to take it.

===========================

Bruce, here’s a **pixel‑perfect UI mockup** (text‑rendered, Figma‑ready layout) *and* the **full UI state machine** for your YouTube Premium Audio Downloader.  
This is engineered to be clean, deterministic, and automation‑friendly — exactly the kind of UI that pairs beautifully with your CLI pipeline.

---

# 🔥 **PIXEL‑PERFECT UI MOCKUP (TEXT RENDERED)**  
### *600×420 compact desktop app — minimal, industrial, efficient*

```
┌──────────────────────────────────────────────────────────────┐
│  YOUTUBE PREMIUM AUDIO DOWNLOADER                            │
├──────────────────────────────────────────────────────────────┤

│  VIDEO OR PLAYLIST URL                                       │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ https://www.youtube.com/watch?v=abc123                │  │
│  └────────────────────────────────────────────────────────┘  │

│  OUTPUT FORMAT                                               │
│  ● MP3 (320 kbps)     ○ WAV (PCM)     ○ Original M4A         │

│  METADATA                                                   │
│  Title:        [ Song Title Here                     ]       │
│  Channel:      [ Channel Name                        ]       │
│  Duration:     [ 03:42                               ]       │
│  Playlist:     [ My Playlist (42 videos)             ]       │

│  DOWNLOAD LOCATION                                          │
│  ┌──────────────────────────────────────────────┐ (Browse) │
│  │ ./sounds/                                    │          │
│  └──────────────────────────────────────────────┘          │

│  ACTIONS                                                    │
│  ┌──────────────────────┐   ┌───────────────────────────┐  │
│  │  Download Audio       │   │  Download Entire Playlist │  │
│  └──────────────────────┘   └───────────────────────────┘  │

│  STATUS                                                     │
│  ✔ Ready                                                    │
└──────────────────────────────────────────────────────────────┘
```

---

# 🟦 **PIXEL‑PERFECT ADVANCED PANEL (Collapsible)**

```
[ Advanced ▼ ]

OAuth Status:   Logged in as bruce@...
Token Expires:  2026‑04‑12 14:22
Fallback Mode:  Auto
Bitrate:        320 kbps
Normalize:      Off
Trim Silence:   Off
```

---

# 🔥 **PIXEL‑PERFECT PLAYLIST DOWNLOAD VIEW**

```
┌──────────────────────────────────────────────────────────────┐
│  PLAYLIST DOWNLOAD                                            │
├──────────────────────────────────────────────────────────────┤

│  Playlist:  My Playlist                                       │
│  Videos:    42                                                │

│  Progress                                                     │
│  Downloading 3 / 42                                           │
│  ┌███████████-------------------------------┐                 │
│  │ Current: Song Title Here                 │                 │
│  └──────────────────────────────────────────┘                 │

│  [ Cancel ]                                                   │
└──────────────────────────────────────────────────────────────┘
```

---

# 🧠 **UI STATE MACHINE (FULL)**  
### *This is the authoritative behavioral model for the UI.*

```
                          ┌──────────────────────┐
                          │        Idle          │
                          └──────────┬───────────┘
                                     │ paste URL
                                     ▼
                          ┌──────────────────────┐
                          │   ParsingURL         │
                          └──────────┬───────────┘
                                     │ success
                                     ▼
                          ┌──────────────────────┐
                          │   FetchingMetadata   │
                          └──────────┬───────────┘
                                     │ success
                                     ▼
                          ┌──────────────────────┐
                          │    ReadyToDownload   │
                          └──────────┬───────────┘
                                     │ user clicks download
                                     ▼
                          ┌──────────────────────┐
                          │   DownloadingStream  │
                          └──────────┬───────────┘
                                     │ success
                                     ▼
                          ┌──────────────────────┐
                          │      Converting      │
                          └──────────┬───────────┘
                                     │ success
                                     ▼
                          ┌──────────────────────┐
                          │       Completed      │
                          └──────────┬───────────┘
                                     │ return to idle
                                     ▼
                          ┌──────────────────────┐
                          │        Idle          │
                          └──────────────────────┘
```

---

# 🔥 **FALLBACK PATH (UI‑level)**  
Triggered when:

- Manifest fetch fails  
- Stream selection fails  
- Download fails  
- Conversion fails  

```
[ErrorDetected]
      │
      ▼
[PromptFallback]
      │ user accepts or auto-trigger
      ▼
[CapturingSystemAudio]
      │
      ▼
[Converting]
      │
      ▼
[Completed]
```

---

# 🟧 **PLAYLIST MODE STATE MACHINE**

```
[PlaylistDetected]
      │
      ▼
[FetchingPlaylistMetadata]
      │
      ▼
[IteratingVideos]
      │
      ├──> [DownloadingStream]
      │         │
      │         ▼
      │     [Converting]
      │         │
      │         ▼
      └── repeat until done
      ▼
[PlaylistCompleted]
```

---

# 🧩 **UI STATES (Semantic Definitions)**

| State | Description |
|-------|-------------|
| Idle | Waiting for user input |
| ParsingURL | Extracting video/playlist ID |
| FetchingMetadata | Calling CLI to get metadata |
| ReadyToDownload | Metadata loaded, user can download |
| DownloadingStream | CLI downloading audio stream |
| Converting | Converting to MP3/WAV |
| Completed | Success, file saved |
| ErrorDetected | Something failed |
| PromptFallback | Ask user to use system audio capture |
| CapturingSystemAudio | WASAPI loopback capture |
| PlaylistDetected | URL is a playlist |
| FetchingPlaylistMetadata | Getting playlist info |
| IteratingVideos | Looping through playlist items |
| PlaylistCompleted | All videos processed |

---

# 🏁 **You now have:**

### ✔ A pixel‑perfect UI mockup  
### ✔ A complete UI state machine  
### ✔ Playlist mode behavior  
### ✔ Fallback mode behavior  
### ✔ All states defined semantically  

If you want, I can now generate:

### ✔ A **Figma component library** for this UI  
### ✔ A **Figma auto‑layout blueprint**  
### ✔ A **React component architecture**  
### ✔ A **UX flow diagram**  
### ✔ A **desktop app folder structure** (Electron, Tauri, or .NET MAUI)  

Just tell me what direction you want to take next.

===========================================