# Page-by-Page UI Spec — Updated Design

> **Design language:** Dark-first, neon-aqua accent (`#00F5D4`), bold metrics, rounded card-based layouts. Inspired by modern fitness/health tracker apps. All colours reference `THEME.md`.

---

## Navigation Structure

Bottom NavigationBar with 4 tabs. Active tab icon wrapped in `#00F5D4` filled circle.

```
[Home]  [Analyze]  [History]  [Info]
```

Settings is accessible via the Home screen top-right gear icon (next to notification bell).

---

## 1. Onboarding Screen (`onboarding_screen.dart`)

**Purpose:** First-launch hero screen. Skipped if user has previous session.

**Layout (top → bottom):**
- Full-bleed coral reef hero photo with deep dark gradient overlay (bottom 60%)
- Centred motivational headline at lower portion:
  > **"Coral health made simple:**  
  > **your dive to** `Conservation` **and** `Discovery`**"**  
  Highlighted words use `#00F5D4`. Other words white.
- Single pill CTA button: **"Get Started"** → navigates to Home Screen
  - Background `#00F5D4`, text `#0E0E0E`, with right-side circular play icon

---

## 2. Home Screen / Dashboard (`home_screen.dart`)

**Purpose:** Landing dashboard. Shows user identity, last assessment, and quick stats.

**Layout (top → bottom):**

1. **Top Bar**
   - Left: circular avatar + "Welcome Back! 👋" (caption) + "Coral Scanner" (title) underneath
   - Right: notification bell icon + gear (Settings) icon

2. **Hero "Last Assessment" Card** (`#1A1A1A`, radius 24)
   - Icon (running figure replaced with coral icon) in `#00F5D4` circle on left
   - Title: "Last Scan · 3 days ago"
   - Caption: "Bleached coral · 87% confidence"
   - Right side: arrow icon in small dark circle

3. **Section Header**: "Health Metrics" + "See All" link on right (in `#00F5D4`)

4. **2 × 2 Metric Grid** (small cards, radius 20)
   | Card | Content |
   |---|---|
   | Top-left | "Test Accuracy" — `98.11%` — mini bar chart |
   | Top-right | "Inference" — `10 ms` — sparkline |
   | Bottom-left | "Scans Today" — `7` — bar icon |
   | Bottom-right | "Avg Confidence" — `92.4%` — mini gauge |

5. **Section Header**: "Coral Classes" + "See All"

6. **Filter Pills Row**: `All` | `Healthy` | `Bleached` | `Dead`
   - Active pill: `#00F5D4` background, `#0E0E0E` text
   - Inactive: transparent with white text

7. **Featured Card** (image-based card showing 3 coral examples or hero coral photo)
   - Title overlay: "Reef Assessment"
   - Caption: "159 test samples"

---

## 3. Analysis Screen (`analysis_screen.dart`)

**Purpose:** Image input + model selection before inference.

**Layout (top → bottom):**

1. **Top Bar**: Back arrow + "Analyze Coral" title + calendar icon (date stamp)

2. **Date Pills Row**: optional horizontal scroll of `11 12 13 14 [Today, 20 May] 21 22 23` (style match to reference fitness app's date strip)

3. **Image Source Section** ("Select Image" caption header)
   - Two large elevated cards side by side:
     - **Camera** card — camera icon in `#00F5D4` circle, "Take Photo" label
     - **Gallery** card — folder icon, "From Gallery" label

4. **Image Preview Pane** (radius 24, takes ~60% width centred)
   - Placeholder: dark `#2B2B2B` with coral icon and "No image selected" text
   - After pick: thumbnail filling the pane

5. **Model Selector** (`model_selector.dart`) — two pill toggle buttons:
   - `Ensemble · High Accuracy` (default active when online)
   - `Base · Fast & Offline`
   - Active pill: `#00F5D4` background

6. **Analyze CTA** (full-width pill button) — disabled (`#2B2B2B`) until image selected
   - Active state: `#00F5D4`, text "Analyze Coral" with right arrow

7. **Error Snackbar** if non-image / connection fails: red tint `#F8717133` background, dismissible

---

## 4. Result Screen (`result_screen.dart`) — KEY SCREEN

**Purpose:** Display full prediction with confidence, Grad-CAM, and probabilities.

**Layout (top → bottom):**

1. **Top Bar**: Back arrow + "Assessment Result" + date pill (matches reference Daily Report)

2. **Hero "Health Grade" Card** (`#1A1A1A`, radius 24, full width)
   - Left side:
     - Title: "Coral Status"
     - Caption: status-coloured pill badge (Healthy / Bleached / Dead)
     - Description: 1-line recommendation
   - Right side: **Confidence Ring** — large circular gauge showing confidence % (e.g., "92")
     - Ring colour: `#00F5D4`
     - Inner text: large 40 sp number, "%" below

3. **Section Header**: "Visual Analysis" + "Grad-CAM" caption

4. **Grad-CAM Viewer Card** (`gradcam_viewer.dart`)
   - Large image at top (radius 20)
   - 3-pill toggle below image:
     - `Original` | `Overlay` | `Heatmap`
     - Active pill: `#00F5D4` background, dark text

5. **Section Header**: "Class Probabilities"

6. **Probability Cards** — 3 horizontal cards stacked vertically (each radius 20):
   - Each card shows:
     - Left: class label + small status colour dot
     - Middle: large probability number
     - Right: sparkline-style mini bar in `#00F5D4`
   - Example layout:
     ```
     Healthy  💚    2.0%    [▁▁▁]
     Bleached 🟡   93.5%    [█████]
     Dead     🔴    4.5%    [▁▁]
     ```

7. **Uncertainty Banner** (only if confidence < 75%)
   - Amber tint background `#FBBF2433`, text `#FBBF24`
   - "Low confidence — consider re-capturing in better lighting"

8. **Recommendation Card** (`coral_status_card.dart`)
   - Severity label + recommendation text from backend
   - 4 px left border in class colour

9. **Model Info Row** (caption text, `#A1A1AA`)
   - "EfficientNetB0 SWA · seed42" (Base) or "5-seed Ensemble + TTA" (Ensemble)

10. **Action Buttons Row** (3 pill icon buttons):
    - **Save** (heart icon)
    - **Share** (share icon)
    - **Re-analyze** (refresh icon)

---

## 5. History Screen (`history_screen.dart`)

**Purpose:** Browse past assessments saved locally (sqflite).

**Layout (top → bottom):**

1. **Top Bar**: "History" title + filter icon

2. **Weekly Trend Card** (radius 24, big card at top)
   - Title: "Workout" → renamed to **"Assessment Activity"**
   - Toggle pills: `Week` | `Day` | `Month` (active = `#00F5D4`)
   - Line chart in `#00F5D4` showing scan count over time
   - X-axis: Mon Tue Wed Thu Fri Sat Sun

3. **Filter Pills Row**: `All` | `Healthy` | `Bleached` | `Dead`

4. **List of Session Cards** (radius 20, `#1A1A1A`)
   - Each card row:
     - Thumbnail (60×60 rounded square)
     - Middle column: class badge + confidence % + date/time + model used
     - Right: arrow icon
   - Tap → opens Result Screen (read-only mode)
   - Long-press → delete confirmation dialog

5. **Empty State** (when no history): coral illustration + "No assessments yet. Start by analyzing your first coral image."

---

## 6. Info Screen (`info_screen.dart`)

**Purpose:** Educate users on the 3 coral health categories.

**Layout (top → bottom):**

1. **Top Bar**: "Coral Health Guide" title

2. **Three Expandable Cards** (radius 24, `#1A1A1A`):

   **Healthy Coral**
   - Top: representative photo (rounded top corners)
   - Status pill: green `#4ADE80`
   - Title: "Healthy Coral"
   - Tap to expand: signs, characteristics, importance

   **Bleached Coral**
   - Same structure, amber `#FBBF24` pill
   - Description: zooxanthellae loss, white/pale tissue
   - Causes: thermal stress, pollution, disease

   **Dead Coral**
   - Same structure, red `#F87171` pill
   - Description: skeleton exposed, algae overgrowth
   - Action: document for conservation

---

## 7. Settings Screen (`settings_screen.dart`)

**Purpose:** User configuration.

**Layout (top → bottom):**

1. **Top Bar**: Back + "Settings"

2. **Connection Section**
   - "Backend API URL" — text field (`#2B2B2B` BG, radius 16)
   - Default: `http://10.0.2.2:8000`
   - "Test Connection" pill button — shows loading → green check or red X

3. **Preferences Section** (list of toggle rows, dividers `#27272A`)
   - **Default Model**: pill toggle Ensemble | Base
   - **Dark Mode**: switch (default ON, accent `#00F5D4`)
   - **Confidence Threshold**: slider (default 75 %)

4. **About Section**
   - Model: EfficientNetB0 SWA Ensemble (5-seed)
   - Test Accuracy: 98.11 %
   - Macro F1: 0.98
   - Classes: Healthy, Bleached, Dead
   - App version: 1.0.0
   - Developer: Muhammad Luqman Haziq · UniMAP FYP 2025

---

## Component Mapping (Reference → CoralScan)

| Reference Fitness App Element | CoralScan Implementation |
|---|---|
| "Welcome Back! Rupak Chakraborty" header | "Welcome Back! Coral Scanner" with avatar |
| "Running 7 days" hero card | "Last Scan · 3 days ago" hero card |
| Health Metrics 2×2 grid (Blood Pressure / Heart beat) | Test Accuracy / Inference / Scans / Avg Confidence |
| "Workout Programs" filter pills | "Coral Classes" filter pills |
| "Full Body workout" image card | "Reef Assessment" featured card |
| "Daily Report" with date strip | "Assessment Result" with date strip |
| "Health Grade 80" ring | "Confidence 92%" ring |
| 2×2 metrics with mini charts | 3 probability cards with sparklines |
| "Workout" weekly line chart | "Assessment Activity" weekly chart |
| Bottom nav 5 icons (home/compass/bar/heart/profile) | Bottom nav 4 icons (home/scan/history/info) |

---

## Visual Consistency Rules

1. **Every screen uses the dark background** `#0E0E0E` — no exceptions.
2. **Only one accent colour visible per card** — `#00F5D4` for the primary metric; status colours only on badges/pills.
3. **All cards have radius 20+** — no sharp rectangles.
4. **All CTA buttons are full-pill** (radius 999) — never sharp-cornered.
5. **Large numbers use Inter 40 sp Bold** with small unit labels below (e.g., "92" + "%").
6. **Section headers use 16 sp Bold white** with optional "See All" link in `#00F5D4` on the right.
7. **Active bottom nav icon** is always wrapped in `#00F5D4` filled circle.

---

*This spec must be read alongside `THEME.md` for colour and typography tokens. Reference Flutter implementation patterns live in `ARCHITECTURE.md`.*
