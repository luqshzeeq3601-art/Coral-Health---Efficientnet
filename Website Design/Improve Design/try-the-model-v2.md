# Try the Model — Warm Scientific Journal Edition

> **File:** `try-the-model-v2.html`
> **Aesthetic:** Warm cream + editorial serif · coral & teal accents

---

## Concept

A complete departure from corporate "AI tool" UI. Designed to feel like a **scientific field journal** — warm paper tones, italicised serif headings, monospace data labels, decorative numbered steps. The coral reef subject inspired the colour palette: cream backgrounds for sand, deep teal for ocean depth, dusty coral for the reef itself.

**What makes it memorable:** the italic serif "Model" word, the multi-coloured dots orbiting the upload icon, and the numbered step badges in coral.

---

## Colour Palette

| Token | Hex | Role |
|---|---|---|
| `--paper` | `#FAF6F0` | Page background (warm cream) |
| `--paper-warm` | `#FBF8F3` | Card interiors (warmer cream) |
| `--card` / `--white` | `#FFFFFF` | Main panel |
| `--teal-700` | `#0D5C5C` | Primary · explainability |
| `--coral-700` | `#C95A3F` | Accent · italics · active states |
| `--coral-500` | `#E8856B` | Hover · gradients |
| `--healthy` | `#2D7D4F` | Healthy class |
| `--bleached` | `#B47B0B` | Bleached class |
| `--dead` | `#B53B2C` | Dead class |
| `--ink-900` | `#1A1714` | Primary text (warm black) |
| `--ink-500` | `#5C544D` | Body text |

Background uses **two radial gradient washes** (coral top-left, teal bottom-right) for atmosphere.

---

## Typography

| Role | Font | Notes |
|---|---|---|
| Display / titles | **Fraunces** | Variable serif · uses `opsz 144` + `SOFT 50–100` axes for distinctive italics |
| Body / UI | **Manrope** | Modern humanist sans · 300–700 weights |
| Data / labels / chips | **JetBrains Mono** | All numeric values, file metadata, technical labels |

**Italic Fraunces** is used for emphasis (`Model`, `coral`, "Analyse another image") — a signature touch.

---

## Layout & Structure

```
┌─ STAMP ROW ─────────────────────────────────┐
│ N° 01 / DEMO ─────── ● LIVE INFERENCE      │
└──────────────────────────────────────────────┘

╔══ HEADING ═══════════════════════════════════╗
║ Try the Model (italic serif)                ║
║ Description in warm sans                    ║
╚══════════════════════════════════════════════╝

╔══ PANEL (rounded 40px, soft shadow) ═════════╗
║                                              ║
║ ① Choose model                              ║
║    [Ensemble *] [Base]                      ║
║    ─ ─ ─ ─ ─ ─ ─ (dashed divider)          ║
║                                              ║
║ ② Explainability                            ║
║    [🔬 Grad-CAM ──── ●○]                    ║
║    ⚠ ACTIVE · ~2–4 ms                       ║
║    ─ ─ ─ ─ ─ ─ ─                           ║
║                                              ║
║ ③ Upload image                              ║
║    [────── DROP ZONE ──────]                ║
║                                              ║
║ [ Analyse Coral Health ]                    ║
║                                              ║
╚══════════════════════════════════════════════╝
```

---

## Key Design Details

### Numbered step badges
- Circular `01`, `02`, `03` in **Fraunces** serif
- Coral-tinted background with subtle border
- Pairs each step with a title + helper description

### Stamp row
- Top decorative element resembling a journal page header
- `N° 01 / DEMO` in monospace + horizontal rule + animated `● LIVE INFERENCE` chip

### Model cards
- **Active state:** coral-tinted background + 4px coral bar slides in from the left edge
- White icon container with `0 0 0 4px` glow halo when active
- Custom checkmark animates in with spring easing
- Chip system: SWA (teal), TTA (coral), 98.11% (green), Faster (gray)

### Grad-CAM toggle row
- Full-width clickable card, turns teal-tinted when ON
- Notice banner uses **left-border accent** style (amber stripe) in monospace caps
- Toggle thumb uses spring easing for a satisfying snap

### Upload zone
- **Grid pattern overlay** for blueprint/scientific feel
- Three coloured dots (coral, teal, amber) orbit the icon — represent the three classes
- Rotating dashed ring at 14s slow rotation
- Hover/drag state floods the zone with coral tint
- Dark "Browse files" button inverts to coral on hover

### Run button
- Solid `--ink-900` (warm black) base
- Light **sweep animation** runs across on hover (`::before` pseudo)
- Background shifts to coral on hover with bigger shadow

### Loading state
- Concentric coral ripple rings expand outward
- Solid coral core pulses (scale animation)
- Step text in serif, detail line in monospace
- Thin progress bar with coral gradient fill

### Results state
- **Verdict card** with decorative offset circle in corner (overflow-hidden creates partial bleed)
- Healthy/Bleached/Dead each have distinct cream-tinted backgrounds
- Confidence percentage shown LARGE in Fraunces serif
- Three confidence bars with gradient fills
- Three metric boxes with serif values + monospace mini-labels
- Grad-CAM panel: original vs heatmap, with peach/coral gradient placeholder
- Reset link in **italic Fraunces coral** — feels like an editorial footnote

---

## Animations

| Name | Element | Behaviour |
|---|---|---|
| `rise` | Stamp · heading · panel | Staggered 0.55–0.6s entrance |
| `blink` | Live dot in stamp | 1.8s opacity loop |
| `spin` | Upload zone dashed ring | 14s linear, slow & subtle |
| `ripple` | Loading state | 1.8s scale + fade × 2 (offset by 0.9s) |
| `pulseScale` | Loading core | 1.4s breathing |
| `progress` | Load bar fill | 2.6s ease-out |
| `bar-fill` width | Confidence bars | 0.9s with 0.3s stagger delay |
| Run button sweep | `::before` on hover | Light gradient slides left → right |

All easings: `cubic-bezier(0.22, 1, 0.36, 1)` (smooth out) or `cubic-bezier(0.34, 1.56, 0.64, 1)` (spring).

---

## Comparison vs Previous Versions

| Aspect | v1 (Google Material) | v2 (Ocean Editorial) | **v3 (Scientific Journal)** |
|---|---|---|---|
| Mood | Corporate / product | Refined / techy | **Editorial / warm / artisanal** |
| Background | Cool blue-grey | Light blue-grey | **Warm cream + radial gradients** |
| Primary | Google Blue `#1A73E8` | Ocean blue `#1565A8` | **Coral `#C95A3F` + Teal `#0D5C5C`** |
| Display font | Google Sans | Bricolage Grotesque | **Fraunces (with italics)** |
| Body font | Roboto | DM Sans | **Manrope** |
| Data font | — | — | **JetBrains Mono** |
| Steps | Numbered circle badge | Field labels with line | **Coral serif badge with description** |
| Run button | Blue gradient | Dark ocean gradient | **Warm black with coral hover + sweep** |

---

## Files Delivered

```
try-the-model-v2.html   ← standalone HTML (open directly in browser)
try-the-model-v2.md     ← this design documentation
```

---

*All inference numbers (98.11%, 10.38 ms, confidence bars) are bound to your canonical FYP benchmarks. Replace the placeholder Grad-CAM gradient with real overlay output in production via Flask.*
