Bruce, absolutely — here is a **Figma‑ready specification**, written exactly in the format designers and engineers expect when building a real component library and auto‑layout system.  
This is not a conceptual description — this is a **production‑grade spec** you can paste directly into a Figma project description, hand to a designer, or use as the authoritative blueprint for building the UI.

I’ll structure it the same way professional design systems do:

- Component taxonomy  
- Component anatomy  
- Variants  
- Auto‑layout rules  
- Constraints  
- Tokens  
- Templates  
- Interaction notes  

Everything is deterministic, modular, and ready for implementation.

---

# 🔥 **FIGMA‑READY SPEC — YOUTUBE PREMIUM AUDIO DOWNLOADER UI**

---

# 1. **DESIGN TOKENS**

### **Color Tokens**
```
Surface/Background: #F7F7F9
Surface/Panel: #FFFFFF
Surface/Input: #FAFAFC

Border/Default: #D0D3D9
Border/Focus: #4A90E2

Text/Primary: #1A1A1C
Text/Secondary: #4A4A4F
Text/Muted: #8A8A90

Accent/Blue: #4A90E2
Accent/Green: #2ECC71
Accent/Red: #E74C3C
```

### **Spacing Tokens**
```
Space/XS: 4
Space/S: 8
Space/M: 12
Space/L: 16
Space/XL: 24
```

### **Radius Tokens**
```
Radius/Small: 4
Radius/Medium: 6
Radius/Large: 8
```

### **Typography**
```
Title: Inter 20 / Semibold
Section: Inter 14 / Semibold
Label: Inter 12 / Medium
Body: Inter 13 / Regular
Small: Inter 11 / Regular
```

---

# 2. **COMPONENT LIBRARY**

Below is the exact structure to create in Figma’s Assets panel.

```
Components/
  Input/
    TextField
    Radio
    RadioGroup
    FolderPicker
  Button/
    Primary
    Secondary
  Metadata/
    Row
  Panels/
    MetadataPanel
    DownloadLocation
    Actions
    PlaylistProgress
  Progress/
    Bar
  Status/
    Bar
  Panel/
    Collapsible
Templates/
  MainScreen
  PlaylistScreen
```

---

# 3. **COMPONENT SPECS**

---

## **3.1 TextField**

### **Anatomy**
- Container  
- Label (optional)  
- Input text  
- Border  
- Focus ring (variant)  

### **Variants**
```
Default
Focused
Error
Disabled
```

### **Auto‑layout**
```
Direction: Vertical
Gap: 4
Padding: 8/12
Width: Fill container
Height: Hug contents
```

### **Constraints**
- Input text: Fill container  
- Container: Fill container  

---

## **3.2 Radio Button**

### **Anatomy**
- Outer circle  
- Inner dot (selected only)  
- Label  

### **Variants**
```
Selected
Unselected
Disabled
```

### **Auto‑layout**
```
Direction: Horizontal
Gap: 8
Alignment: Center-left
```

---

## **3.3 RadioGroup**

### **Anatomy**
- Multiple Radio components  
- Optional section label  

### **Auto‑layout**
```
Direction: Horizontal
Gap: 24
Alignment: Center-left
```

---

## **3.4 FolderPicker**

### **Anatomy**
- Input field  
- Browse button  

### **Auto‑layout**
```
Direction: Horizontal
Gap: 8
Width: Fill container
```

---

## **3.5 Button (Primary / Secondary)**

### **Anatomy**
- Container  
- Label  

### **Variants**
```
Default
Hover
Pressed
Disabled
```

### **Auto‑layout**
```
Padding: 12/16
Corner radius: 6
Alignment: Center
Min width: 140
```

---

## **3.6 Metadata Row**

### **Anatomy**
- Label (left)  
- Value (right)  

### **Auto‑layout**
```
Direction: Horizontal
Alignment: Space-between
Height: Hug contents
```

---

## **3.7 Metadata Panel**

### **Anatomy**
- Title row  
- Channel row  
- Duration row  
- Playlist row  

### **Auto‑layout**
```
Direction: Vertical
Padding: 12
Gap: 8
Background: Surface/Panel
Corner radius: 8
Width: Fill container
```

---

## **3.8 Download Location Panel**

### **Anatomy**
- FolderPicker  
- Browse button  

### **Auto‑layout**
```
Direction: Horizontal
Gap: 8
Width: Fill container
```

---

## **3.9 Actions Panel**

### **Anatomy**
- Download Audio button  
- Download Playlist button  

### **Auto‑layout**
```
Direction: Horizontal
Gap: 16
Width: Fill container
```

---

## **3.10 Progress Bar**

### **Variants**
```
Idle
InProgress
Complete
```

### **Auto‑layout**
```
Width: Fill container
Height: 8
Corner radius: 4
```

---

## **3.11 Status Bar**

### **Variants**
```
Ready
Loading
Error
Success
```

### **Auto‑layout**
```
Direction: Horizontal
Padding: 8
Alignment: Center-left
Background: Surface/Input
Corner radius: 6
Height: 32
Width: Fill container
```

---

## **3.12 Collapsible Panel**

### **Variants**
```
Collapsed
Expanded
```

### **Auto‑layout**
```
Direction: Vertical
Gap: 8
Padding: 12
Width: Fill container
```

---

# 4. **TEMPLATES**

---

## **4.1 MainScreen Template**

### **Structure**
```
MainScreen
  URL Input
  Output Format RadioGroup
  MetadataPanel
  DownloadLocationPanel
  ActionsPanel
  StatusBar
```

### **Auto‑layout**
```
Direction: Vertical
Padding: 24
Gap: 16
Width: 600
Height: Hug contents
Alignment: Left
```

---

## **4.2 PlaylistScreen Template**

### **Structure**
```
PlaylistScreen
  Playlist Title
  Video Count
  PlaylistProgressPanel
  StatusBar
```

### **Auto‑layout**
```
Direction: Vertical
Padding: 24
Gap: 16
Width: 600
Height: Hug contents
```

---

# 5. **INTERACTION NOTES (Figma Prototype)**

### **TextField**
- On click → Focused variant  
- On error → Error variant  

### **RadioGroup**
- On click → Selected variant  

### **Buttons**
- Hover → Hover variant  
- Press → Pressed variant  
- Disabled → Disabled variant  

### **Collapsible Panel**
- On click header → Toggle collapsed/expanded  

### **Playlist Mode**
- Detect playlist URL → Switch to PlaylistScreen template  

---

# 🏁 **This is a complete, Figma‑ready specification.**

It includes:

- Tokens  
- Component anatomy  
- Variants  
- Auto‑layout rules  
- Constraints  
- Templates  
- Interaction notes  

If you want, I can now generate:

### ✔ A **Figma page structure** (exact pages + sections)  
### ✔ A **component property schema** (Figma’s new properties system)  
### ✔ A **React component mapping**  
### ✔ A **design tokens JSON export**  

Just tell me what you want to forge next.

=============================

Bruce, here is a **clean, production‑ready design tokens JSON export** — exactly the format you’d drop into a Figma Tokens plugin, a design‑system repo, or a cross‑platform UI toolkit.

This JSON mirrors the tokens we defined earlier, but normalized into a **real token schema** with:

- `color`
- `spacing`
- `radius`
- `typography`
- `effects`
- `component` defaults (optional but useful)

Everything is namespaced, deterministic, and ready for automation.

---

# 🔥 **DESIGN TOKENS — JSON EXPORT (Figma‑Ready)**

```json
{
  "version": 1,
  "tokens": {
    "color": {
      "surface": {
        "background": { "value": "#F7F7F9" },
        "panel": { "value": "#FFFFFF" },
        "input": { "value": "#FAFAFC" }
      },
      "border": {
        "default": { "value": "#D0D3D9" },
        "focus": { "value": "#4A90E2" }
      },
      "text": {
        "primary": { "value": "#1A1A1C" },
        "secondary": { "value": "#4A4A4F" },
        "muted": { "value": "#8A8A90" }
      },
      "accent": {
        "blue": { "value": "#4A90E2" },
        "green": { "value": "#2ECC71" },
        "red": { "value": "#E74C3C" }
      }
    },

    "spacing": {
      "xs": { "value": 4 },
      "s": { "value": 8 },
      "m": { "value": 12 },
      "l": { "value": 16 },
      "xl": { "value": 24 }
    },

    "radius": {
      "small": { "value": 4 },
      "medium": { "value": 6 },
      "large": { "value": 8 }
    },

    "typography": {
      "title": {
        "fontFamily": "Inter",
        "fontSize": 20,
        "fontWeight": 600,
        "lineHeight": 28
      },
      "section": {
        "fontFamily": "Inter",
        "fontSize": 14,
        "fontWeight": 600,
        "lineHeight": 20
      },
      "label": {
        "fontFamily": "Inter",
        "fontSize": 12,
        "fontWeight": 500,
        "lineHeight": 16
      },
      "body": {
        "fontFamily": "Inter",
        "fontSize": 13,
        "fontWeight": 400,
        "lineHeight": 18
      },
      "small": {
        "fontFamily": "Inter",
        "fontSize": 11,
        "fontWeight": 400,
        "lineHeight": 14
      }
    },

    "effects": {
      "focusRing": {
        "type": "shadow",
        "value": "0 0 0 2px #4A90E2"
      },
      "inputShadow": {
        "type": "shadow",
        "value": "0 1px 2px rgba(0,0,0,0.06)"
      },
      "panelShadow": {
        "type": "shadow",
        "value": "0 2px 4px rgba(0,0,0,0.08)"
      }
    },

    "component": {
      "button": {
        "padding": { "value": "12 16" },
        "radius": { "value": "{radius.medium}" },
        "minWidth": { "value": 140 }
      },
      "input": {
        "padding": { "value": "8 12" },
        "radius": { "value": "{radius.medium}" }
      },
      "panel": {
        "padding": { "value": 12 },
        "radius": { "value": "{radius.large}" }
      }
    }
  }
}
```

---

# 🧩 **NOTES FOR FIGMA TOKENS / DESIGN SYSTEMS**

### ✔ Namespaced keys  
Everything is grouped under `color`, `spacing`, `radius`, `typography`, `effects`, and `component`.

### ✔ Figma Tokens compatibility  
This JSON is directly compatible with:

- Figma Tokens plugin  
- Tokens Studio  
- Style Dictionary  
- Tailwind config generators  
- Design‑system pipelines  

### ✔ Component tokens  
The `component` section is optional but extremely useful for:

- Auto‑layout defaults  
- Padding consistency  
- Radius inheritance  
- Cross‑platform UI generation  

### ✔ Token references  
You can replace literal values with references like:

```
"value": "{color.accent.blue}"
```

if you want full token chaining.

---

# 🏁 **You now have a complete, production‑ready design tokens JSON export.**

If you want, I can also generate:

### ✔ A **Style Dictionary build config**  
### ✔ A **Tailwind preset** based on these tokens  
### ✔ A **React theme object** (MUI, Chakra, Radix, or custom)  
### ✔ A **CSS variables export**  
### ✔ A **Figma Tokens import guide**  

Just tell me which direction you want to take next.

