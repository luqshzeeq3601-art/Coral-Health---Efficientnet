# Page-by-Page UI Spec

## Navigation Structure

Bottom NavigationBar with 4 tabs:

```
[Home]  [Analyze]  [History]  [Info]
```

Settings is accessible via the Home screen top-right icon.

---

## 1. Home Screen (`home_screen.dart`)

**Purpose:** Landing page. Motivates the user and gives quick access to analysis.

**UI Elements:**
- App logo + title "Coral Health AI"
- Hero banner with tagline
- **"Analyze Coral"** CTA button → navigates to Analysis Screen
- Last result preview card (thumbnail + class badge + confidence) — hidden if no history
- Stats row: Model accuracy 98.11% | Inference ~10 ms | 3 classes
- Top-right gear icon → Settings Screen

---

## 2. Analysis Screen (`analysis_screen.dart`)

**Purpose:** Image input and model selection before running inference.

**UI Elements:**
- Section heading "Select Image"
- Two buttons side by side:
  - **Camera** — opens device camera via `camera` plugin
  - **Gallery** — opens photo picker via `image_picker`
- Image preview pane (square, rounded corners) — shows "No image selected" placeholder by default
- **Model Selector** (`model_selector.dart`) — two radio options:
  - `Ensemble (High Accuracy)` — requires backend connection
  - `Base (Fast, Offline)` — runs on device
- **Analyze** button (disabled until image selected) — shows loading spinner during inference
- Error snackbar if non-image file selected or connection fails

---

## 3. Result Screen (`result_screen.dart`)

**Purpose:** Display the full prediction output.

**UI Elements (top to bottom):**

1. **Status Badge** — color-coded pill
   - Healthy → green
   - Bleached → yellow/amber
   - Dead → red

2. **Confidence Ring** (`confidence_ring.dart`) — circular gauge showing confidence %

3. **Grad-CAM Viewer** (`gradcam_viewer.dart`) — image with 3-way toggle:
   - `Original` — unmodified input image
   - `Overlay` — Grad-CAM heatmap blended on original
   - `Heatmap` — heatmap only (JET colormap)

4. **Probability Bars** (`probability_bars.dart`) — horizontal bar chart:
   - Healthy | Bleached | Dead (all 3 classes, color-coded)

5. **Uncertainty Banner** — amber warning card shown when confidence < 75%:
   > "Low confidence prediction. Consider re-capturing with better lighting."

6. **Recommendation Card** (`coral_status_card.dart`) — severity label + recommendation text from backend

7. **Model Info Row** — "EfficientNetB0 SWA · seed42" (Base) or "5-seed Ensemble" (Ensemble)

8. **Action Buttons** row:
   - **Save** — stores to sqflite history
   - **Share** — system share sheet (image + text summary)
   - **Re-analyze** — goes back to Analysis Screen with same image

---

## 4. History Screen (`history_screen.dart`)

**Purpose:** Browse all past coral assessments saved locally.

**UI Elements:**
- Filter chips row: All | Healthy | Bleached | Dead
- ListView of `HistoryEntry` cards:
  - Thumbnail (60×60)
  - Class badge
  - Confidence %
  - Date + time
  - Model used (Base / Ensemble)
- Tap card → opens Result Screen (read-only, no re-analyze)
- Long-press card → delete confirmation dialog
- Empty state illustration when no history

---

## 5. Info Screen (`info_screen.dart`)

**Purpose:** Educate users on coral health categories.

**UI Elements:**
- Three expandable info cards:

  **Healthy Coral**
  - Description: Normal pigmentation, tissue intact
  - Signs: Vibrant color, full polyp extension
  - Causes: N/A (positive indicator)

  **Bleached Coral**
  - Description: Loss of zooxanthellae, white/pale appearance
  - Causes: Elevated water temperature, pollution, disease
  - Action: Monitor closely; reversible if stressors removed

  **Dead Coral**
  - Description: Bare skeleton, algae overgrowth
  - Causes: Prolonged bleaching, physical damage, disease
  - Action: Document and report for conservation records

- Each card has a representative example image and colored top border

---

## 6. Settings Screen (`settings_screen.dart`)

**Purpose:** User configuration for backend and app behavior.

**UI Elements:**
- **Backend API URL** text field (default: `http://10.0.2.2:8000`)
  - "Test Connection" button → pings `/api/health`
- **Default Model** toggle: Ensemble / Base
- **Dark Mode** switch
- **About** section:
  - Model: EfficientNetB0 SWA Ensemble
  - Accuracy: 98.11%
  - Classes: Healthy, Bleached, Dead
  - App version: 1.0.0
