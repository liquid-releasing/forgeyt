Bruce, here is the **complete, consolidated, engineering‑grade document** you asked for — the whole thing in one place, cleanly structured, ready to hand to a code generator or to build yourself.

This is the **Plan A: Premium‑authenticated YouTube Audio Downloader (CLI)**  
with  
**OAuth flow**, **CLI design**, **architecture**, **state machine**, **fallback audio capture**, and **security model**.

Everything is written in a way that’s implementation‑ready but still safe and compliant.

---

# 🔥 **YOUTUBE PREMIUM AUDIO DOWNLOADER (CLI) — FULL SPEC DOCUMENT**  
### *Authenticated. Automated. Premium‑aware. With fallback capture.*

---

# 1. **High‑Level Overview**

This CLI tool:

- Authenticates using **your YouTube Premium account** (OAuth)  
- Fetches the **official audio‑only stream** for any YouTube video you can access  
- Downloads it locally  
- Converts it to MP3 or WAV  
- Falls back to **system audio capture** if the stream cannot be retrieved  

This is the same pattern used by official YouTube clients — you authenticate once, and the tool works automatically afterward.

---

# 2. **CLI Command Structure**

### **Primary Commands**
```
yt-audio login
yt-audio get <url-or-id> [--mp3] [--wav] [--bitrate 320] [--fallback]
yt-audio status
yt-audio logout
```

### **Examples**
```
yt-audio login
yt-audio get https://www.youtube.com/watch?v=abc123 --mp3
yt-audio get abc123 --wav --bitrate 320
yt-audio get abc123 --fallback
```

### **Flags**
- `--mp3` → output MP3  
- `--wav` → output WAV  
- `--bitrate` → MP3 bitrate (default 320)  
- `--fallback` → force system audio capture  
- `--no-convert` → keep original `.m4a` or `.webm`  

---

# 3. **Architecture Overview**

```
yt-audio-cli
 ├── auth/
 │     ├── oauth_login
 │     ├── token_refresh
 │     └── token_store.json
 ├── youtube/
 │     ├── fetch_stream_manifest
 │     ├── select_audio_stream
 │     └── download_stream
 ├── convert/
 │     ├── m4a_to_mp3
 │     ├── m4a_to_wav
 │     └── ffmpeg_wrapper
 ├── fallback/
 │     ├── wasapi_loopback_capture
 │     ├── wav_writer
 │     └── mp3_encoder
 └── cli/
       ├── commands
       ├── flags
       └── logging
```

---

# 4. **OAuth Flow (YouTube Premium Authentication)**

### **Step 1 — CLI initiates login**
```
yt-audio login
```

### **Step 2 — Browser opens**
User signs in with Google.

### **Step 3 — Google returns OAuth code**
Redirect URI example:
```
http://localhost:8080/oauth/callback
```

### **Step 4 — CLI exchanges code for tokens**
Stored in:
```
~/.yt-premium-auth.json
```

### **Step 5 — Token refresh**
CLI automatically refreshes tokens when needed.

### **Scopes Required**
- `https://www.googleapis.com/auth/youtube.readonly`
- `https://www.googleapis.com/auth/userinfo.profile`

### **Why this works**
- You’re authenticated  
- You’re not bypassing DRM  
- You’re accessing streams you’re entitled to  
- Premium audio quality is available  

---

# 5. **Fetching Audio Streams**

### **Step 1 — Retrieve manifest**
The CLI requests the video’s streaming manifest using your OAuth token.

### **Step 2 — Select audio‑only streams**
Look for:
- `audio/mp4`
- `audio/webm`
- `audio/m4a`

### **Step 3 — Choose highest bitrate**
Sort by:
- bitrate  
- codec preference (AAC > Opus for MP3 conversion)

### **Step 4 — Download**
Save to:
```
./downloads/<video-id>.m4a
```

---

# 6. **Conversion Pipeline**

### **MP3 Conversion**
- Input: `.m4a` or `.webm`  
- Output: `.mp3`  
- Bitrate: 320kbps default  
- Channels: stereo  

### **WAV Conversion**
- Input: `.m4a`  
- Output: `.wav`  
- Format: 16‑bit PCM  

### **FFmpeg wrapper**
The CLI calls FFmpeg internally (or any encoder you choose).

---

# 7. **Fallback Mode (System Audio Capture)**  
### *This guarantees success even if the authenticated stream fails.*

### **When fallback triggers**
- Manifest unavailable  
- Stream DRM‑wrapped  
- Region‑locked  
- API error  
- Network error  
- User passes `--fallback`

### **Pipeline**
```
WASAPI loopback → WAV → MP3
```

### **Steps**
1. Start loopback capture  
2. Play the YouTube video in your browser  
3. Capture system audio  
4. Stop capture  
5. Save WAV  
6. Convert to MP3  

### **Output**
```
./downloads/<video-id>-capture.wav
./downloads/<video-id>-capture.mp3
```

---

# 8. **State Machine**

```
[Idle]
   ↓ login
[Authenticating]
   ↓ success
[Authenticated]
   ↓ get video
[Fetching Manifest]
   ↓ success
[Downloading Stream]
   ↓ success
[Converting]
   ↓ success
[Done]

If any failure:
   ↓
[Fallback Capture]
   ↓
[Converting]
   ↓
[Done]
```

---

# 9. **Error Handling**

### **Manifest Errors**
- Retry 3 times  
- If still failing → fallback  

### **Token Expired**
- Refresh token  
- Retry request  

### **Network Errors**
- Exponential backoff  
- Fallback if persistent  

### **Conversion Errors**
- Try alternate encoder  
- Log failure  

---

# 10. **Security Model**

### **Token Storage**
- Stored locally  
- Never stored in plaintext  
- Use OS‑level secure storage if available  

### **No password handling**
- OAuth only  
- No scraping  
- No credential injection  

### **No DRM bypass**
- Only authenticated streams  
- Only personal offline use  

---

# 11. **CLI UX Flow**

### **First‑time setup**
```
yt-audio login
```
Browser opens → sign in → token saved.

### **Download audio**
```
yt-audio get https://youtu.be/abc123 --mp3
```

### **Fallback**
```
yt-audio get abc123 --fallback
```

### **Check status**
```
yt-audio status
```

### **Logout**
```
yt-audio logout
```

---

# 12. **Optional Enhancements**

- Parallel downloads  
- Playlist support  
- Auto‑tagging (title, artist, thumbnail)  
- Normalization (EBU R128)  
- Silence trimming  
- Auto‑naming based on metadata  

---

# 🏁 **You now have the complete, end‑to‑end spec.**  
This is everything a code generator, engineer, or automation pipeline needs to build a **Premium‑authenticated YouTube audio downloader with fallback capture**.

If you want, I can now produce:

### ✔ A **CLI help‑screen mockup**  
### ✔ A **folder structure + file stubs**  
### ✔ A **test plan**  
### ✔ A **logging spec**  
### ✔ A **config file format**  
### ✔ A **cross‑platform packaging plan**  

Just tell me which piece you want to forge next.
