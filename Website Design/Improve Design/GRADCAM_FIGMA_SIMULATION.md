# GradCAM Simulation — Figma Design Specification
## For Claude Code with Figma MCP Plugin

> **Tool:** Figma (via Claude Code Figma MCP — `use_figma` tool)
> **Output:** Figma file with 5 frames (Idle + 4 steps) + Prototype interactions
> **Mode:** Design + Prototype (Smart Animate transitions between step frames)
> **Theme:** Light — white background, ocean-blue and teal accents
> **Canvas size per frame:** 1440 × 900 px (Desktop Web)

---

## Claude Code Must Do This First

```
1. Call Figma MCP: use_figma → create_new_file → name "GradCAM Simulation — Coral Reef CNN"
2. Create 1 Figma Page named "GradCAM Steps"
3. Create 5 frames on that page (see §3 for layout)
4. Build all components as reusable Figma components (see §4)
5. Place component instances in each frame (see §5–§9)
6. Set up prototype interactions (see §10)
7. Export shareable Figma link
```

---

## 1. Design Tokens

### 1.1 Colour Palette

| Token Name | Hex | Usage |
|---|---|---|
| `bg-canvas` | `#F0F9FF` | Frame background (sky-50) |
| `bg-panel` | `#FFFFFF` | Card / panel surfaces |
| `bg-panel-dim` | `#F8FAFC` | Dimmed panel (slate-50) |
| `border-default` | `#E2E8F0` | Default borders (slate-200) |
| `border-active` | `#14B8A6` | Active/highlighted borders (teal-500) |
| `text-primary` | `#0F172A` | Main headings (slate-900) |
| `text-secondary` | `#475569` | Body text (slate-600) |
| `text-muted` | `#94A3B8` | Labels, captions (slate-400) |
| `accent-sky` | `#0EA5E9` | Step 1 colour (sky-500) |
| `accent-orange` | `#F97316` | Step 2 colour (orange-500) |
| `accent-violet` | `#7C3AED` | Step 3 colour (violet-700) |
| `accent-teal` | `#0D9488` | Step 4 colour (teal-700) |
| `class-healthy` | `#22C55E` | Healthy class (green-500) |
| `class-bleached` | `#F59E0B` | Bleached class (amber-500) |
| `class-dead` | `#EF4444` | Dead class (red-500) |
| `gradient-arrow` | `#EF4444` | Backprop gradient arrows |
| `heatmap-cold` | `#3B82F6` | Jet colormap cold end |
| `heatmap-hot` | `#EF4444` | Jet colormap hot end |

### 1.2 Typography

| Style | Font | Size | Weight | Usage |
|---|---|---|---|---|
| `heading-xl` | Inter | 48px | 800 | Section title |
| `heading-md` | Inter | 20px | 700 | Card titles |
| `heading-sm` | Inter | 14px | 700 | Step labels |
| `body` | Inter | 14px | 400 | Descriptions |
| `caption` | Inter | 11px | 500 | Map labels, formulas |
| `mono` | JetBrains Mono | 13px | 400 | Code/formula text |

### 1.3 Spacing

```
Frame padding:  80px top/bottom, 120px left/right
Card padding:   24px
Gap between panels: 32px
Component gap:  16px
```

---

## 2. Figma Component Library

Create these as Figma Components (⌘K → Create Component) before placing in frames.

### Component 1 — `FeatureMapTile`

```
Size: 90 × 90 px
Shape: Rectangle, corner radius 8px
Fill: Gradient mesh simulating activation pattern
  - Background: #0F172A (dark slate)
  - Overlay: 6×6 grid of small rectangles (each ~13×13 px)
    Colors from teal palette: #0D9488, #14B8A6, #2DD4BF, #99F6E4
    Arrange in organic non-uniform pattern (not a uniform grid)
    Some cells darker (#064E3B), some lighter (#5EEAD4)
    Simulate: neural activation — brighter = more activated
Border: 1px #1E293B
Label (Auto Layout, bottom): "Aᵏ" — JetBrains Mono 10px #94A3B8

Variants:
  State=Idle       → fill opacity 40%, label color #475569
  State=Active     → fill opacity 100%, border 1.5px #14B8A6, glow effect (shadow 0 0 12px #14B8A6 40%)
  State=Gradient   → red-orange tint overlay rgba(249,115,22,0.35) on top of base fill
  State=Faded      → fill opacity 20%, label opacity 30%
  State=Weighted   → fill opacity 100%, + class colour corner badge showing α value
```

### Component 2 — `AlphaBar`

```
Size: 32 × variable height (max 120px)
Shape: Rectangle, corner radius 4px top only
Fill: class colour (Healthy/Bleached/Dead) — passed as property
Label above: "α₁" JetBrains Mono 10px text-muted
Value below: "0.82" JetBrains Mono 11px bold class colour

Variants:
  Height=Tall   → height 110px (α ≈ 0.91)
  Height=Medium → height 70px  (α ≈ 0.58)
  Height=Short  → height 40px  (α ≈ 0.33)
  State=Hidden  → height 2px, opacity 0 (for step 0,1,2 frames)
  State=Visible → full height (for step 3,4 frames)
```

### Component 3 — `GradientArrow`

```
Shape: Line + Arrow head
Stroke: 2.5px, color #EF4444 (red — represents gradient)
End arrowhead: filled triangle, #EF4444
Dash pattern: dashed (8, 4) — signals gradient flow direction
Length variants: Long (240px), Medium (180px), Short (120px)
Direction: right-to-left (from Class Node toward feature maps)
Label on arrow: "∂y^c/∂Aᵏ" JetBrains Mono 9px #EF4444, positioned above midpoint

Variants:
  State=Hidden  → opacity 0
  State=Visible → opacity 100%
  State=Pulse   → use Figma Smart Animate — opacity oscillates (achieved by 2 frames)
```

### Component 4 — `ClassNode`

```
Shape: Circle, diameter 72px
Fill: Radial gradient — class colour center → darker edge
  Healthy:  #22C55E → #15803D
  Bleached: #F59E0B → #B45309
  Dead:     #EF4444 → #B91C1C
Border: 2px white, shadow 0 0 20px class-colour 50%
Label inside: "yᶜ" Inter 16px 700 white
Label below:  "Class Score" Inter 11px text-muted

Variants (one per class): Healthy / Bleached / Dead
```

### Component 5 — `HeatmapOverlay`

```
Size: 220 × 220 px (matches input image frame size)
Shape: Rectangle with fill painted as jet colormap gradient
  Create using Figma's gradient fill editor:
  
  HEALTHY (tight center focus):
    Radial gradient, center bright red #EF4444
    25% radius → yellow #FDE047
    50% radius → cyan #06B6D4
    75% radius → dark blue #1E3A5F
    Center position: 50%, 50% of frame
  
  BLEACHED (3-hotspot patchy):
    Use 3 overlapping radial gradients (Figma supports multiple fills):
    Hotspot 1 center (30%, 35%): red→transparent 35% radius
    Hotspot 2 center (65%, 40%): orange→transparent 30% radius
    Hotspot 3 center (50%, 65%): yellow→transparent 28% radius
    Base fill: dark blue #1E3A5F opacity 60%
  
  DEAD (diffuse wide spread):
    Radial gradient, center warm yellow #FDE047 opacity 70%
    Wide spread: 75% radius → blue #3B82F6
    Edge: deep blue #1E3A5F
    Low contrast — peak much dimmer than Healthy

Opacity: 0% in frames 0–3, 80% in frame 4
Corner radius: 8px (match input image corner)

Variants: Healthy / Bleached / Dead × State=Hidden / State=Visible
```

### Component 6 — `InputCoralImage`

```
Size: 220 × 220 px
Background: Rectangle fill #0C2340 (deep ocean blue)
Corner radius: 8px
Border: 1.5px #E2E8F0

Coral drawing (all Figma vector paths):
  HEALTHY variant:
    6 branching coral shapes using Pen tool:
      Trunk: thick path, fill #C2410C (orange-brown), width tapers
      Branches: 3–4 per trunk, fill #F97316 orange or #A855F7 purple
      Tip dots: small ellipses r=4px, fill #22D3EE teal
    Seabed: arc path bottom 30px, fill #1A3A5C
    Water shimmer: 3 diagonal lines, stroke 1px #7DD3FC 20% opacity

  BLEACHED variant:
    Same structure as Healthy but:
    All fills: #F8FAFC (near-white), #E2E8F0 (pale grey)
    Tip dots: #94A3B8 grey (most pigment lost)
    2–3 tips still #FDE68A (partial bleach — yellowish)

  DEAD variant:
    Coral skeleton: #374151 grey paths
    Algae overlay: irregular polygons #166534 dark green
    Sediment dots: scattered #92400E brown circles
    Background: #0A1628 murky dark

Label below image: "Input: 224×224 RGB" Inter 11px text-muted

Variants: Healthy / Bleached / Dead
```

### Component 7 — `StepBadge`

```
Size: Auto (pill shape)
Padding: 6px 14px
Background: step colour at 15% opacity
Border: 1px step colour
Text: "Step N · Step Name" Inter 11px 700 step colour uppercase tracking wide

Colours per step:
  Step 1: accent-sky
  Step 2: accent-orange
  Step 3: accent-violet
  Step 4: accent-teal
```

### Component 8 — `FormulaBar`

```
Size: 680 × 64px
Background: #F8FAFC
Border: 1px #E2E8F0
Corner radius: 12px
Content (JetBrains Mono 14px, horizontal layout):

  Span 1 "L_GradCAM" — text-primary
  Span 2 " = " — text-muted
  Span 3 "ReLU(" — highlight on step 4 (bg accent-teal 20%, text accent-teal)
  Span 4 "Σ_k " — text-muted
  Span 5 "α_k" — highlight on step 3 (bg accent-violet 20%, text accent-violet)
  Span 6 " · " — text-muted
  Span 7 "A^k" — highlight on step 1 (bg accent-sky 20%, text accent-sky)
  Span 8 " )  where  " — text-muted
  Span 9 "α_k = (1/Z)Σ_ij ∂y^c/∂A^k_ij" — highlight on step 2 (bg accent-orange 20%, text accent-orange)

Each span is a separate Figma text layer so highlight can be toggled per frame.
"Highlight" = rectangle behind span with colour fill + text colour change.
```

---

## 3. Frame Structure — 5 Frames on Canvas

```
Place frames left-to-right on Figma canvas, 80px gap between them.

Frame 0 — "Idle / Overview"      X=0
Frame 1 — "Step 1 Forward Pass"  X=1520
Frame 2 — "Step 2 Backprop"      X=3040
Frame 3 — "Step 3 Pool αk"       X=4560
Frame 4 — "Step 4 Heatmap"       X=6080

All frames: 1440 × 900 px, Fill = bg-canvas (#F0F9FF)
```

---

## 4. Shared Layout — All 5 Frames

Every frame contains these shared layout zones:

```
TOP BAR (y=0, height=64px):
  Background: white, bottom border 1px #E2E8F0
  Left: "GradCAM Simulation" Inter 14px 700 text-primary
  Right: class selector mockup (3 pill tabs: Healthy / Bleached / Dead)
         Active class pill: filled class colour, white text
         Inactive: border only, text-muted

SECTION HEADER (y=100):
  StepBadge component (step-specific)
  Heading: "Step N — [Step Name]" heading-xl text-primary, centered

MAIN SCENE (y=200, height=480px):
  Three-column layout:
    Left column  (w=320px): Input Image panel
    Center column (w=560px): Feature Maps panel (main scene)
    Right column (w=320px): Computation panel (class node / alpha bars)

FORMULA BAR (y=710):
  FormulaBar component, centered, active span highlighted per step

STEP CARD ROW (y=790):
  4 StepCard boxes horizontal (see §10), active one highlighted
```

---

## 5. Frame 0 — Idle / Overview

**Purpose:** Show all elements in their resting state with labels explaining what each object represents.

```
TOP BAR: class = Healthy (active)
STEP BADGE: none — show "Grad-CAM Simulation Overview" plain text
HEADING: "How Grad-CAM Works in EfficientNetB0"

LEFT COLUMN — Input Panel:
  Card (320×400px, bg-panel, border-default, radius 16px):
    Title: "① Input Image" heading-sm text-primary, top-left
    InputCoralImage component (Healthy variant) centered
    Caption below: "224×224 RGB coral photograph\nFed into EfficientNetB0"
    body text-secondary, centered

CENTER COLUMN — Feature Maps Panel:
  Card (560×400px):
    Title: "② Final Conv Layer Feature Maps A^k" heading-sm
    2×3 grid of FeatureMapTile components (State=Idle)
      Labels: A¹ A² A³ A⁴ A⁵ A⁶
    Caption: "6 spatial feature maps from MBConv Block 7\nEach map detects different visual patterns"

RIGHT COLUMN — Output Panel:
  Card (320×400px):
    Title: "③ Grad-CAM Output" heading-sm
    HeatmapOverlay (Healthy, State=Hidden) stacked on InputCoralImage
    Caption: "Attention heatmap overlaid on input\nRed = high influence on prediction"

FORMULA BAR: no spans highlighted (all text-muted)

ANNOTATION ARROWS (Figma smart connector lines):
  Input Image → Feature Maps: curved arrow, text "Forward Pass"
  Feature Maps → Right panel: curved arrow, text "Backprop + Pool + ReLU"
```

---

## 6. Frame 1 — Step 1: Forward Pass

**Purpose:** Show coral image projecting into the feature maps. Maps become active.

```
TOP BAR: class = Healthy (active)
STEP BADGE: Step 1 · Forward Pass (accent-sky)
HEADING: "Step 1 — Forward Pass"
Sub: "The coral image flows through 7 MBConv blocks, producing feature maps at the final conv layer."

LEFT COLUMN:
  Card:
    InputCoralImage (Healthy variant)
    Overlay: right-pointing arrow icon on right edge of image, color accent-sky
    Animation label: "→ propagating" caption accent-sky italic
    Status badge: "Processing..." bg-sky-100 text-sky-700

CENTER COLUMN:
  Card with accent-sky border (border-active state):
    Title: "Feature Maps A^k — Activated" heading-sm accent-sky
    2×3 grid of FeatureMapTile (State=Active)
    Each tile has visible coloured activation pattern (teal grid texture)
    Glow shadow on each tile: 0 0 10px #14B8A6 30%
    Label "A^k" in accent-sky below each

    FORMULA highlight: Span 7 "A^k" highlighted sky-blue
    Caption: "MBConv Block 7 output\n7×7 spatial resolution, 1280 channels"

RIGHT COLUMN:
  Card:
    ClassNode component (Healthy) — full opacity but no arrows yet
    Label below: "Target class for gradient\ncomputation (next step)"
    Caption text-muted

FORMULA BAR: "A^k" span highlighted (accent-sky background, accent-sky text)

STEP ANNOTATION (right side of center card, vertical):
  "Each map detects different patterns:"
  • A¹: edges & contours
  • A²: colour gradients
  • A³: texture density
  • A⁴: structural shapes
  • A⁵: pigmentation zones
  • A⁶: branching patterns
  (Inter 11px text-muted, bullet list)
```

---

## 7. Frame 2 — Step 2: Backpropagation

**Purpose:** Show gradient arrows flowing back from class score node to each feature map.

```
TOP BAR: class = Healthy
STEP BADGE: Step 2 · Backpropagation (accent-orange)
HEADING: "Step 2 — Compute Gradients ∂y^c / ∂A^k"
Sub: "Gradients of the class score flow back to measure each feature map's influence."

LEFT COLUMN:
  Card:
    InputCoralImage (Healthy) — dimmed (opacity 60%)
    Caption: "Image held in memory\nfor final heatmap overlay"

CENTER COLUMN:
  Card with orange border:
    Title: "Gradient-Weighted Feature Maps" heading-sm accent-orange
    2×3 grid FeatureMapTile (State=Gradient)
      Each tile has orange-red tint overlay
      Red dot in top-right corner of each tile (gradient signal indicator)
    6 GradientArrow components (State=Visible) overlaid:
      Each arrow points FROM right side of frame (class node) TO each tile
      Arrows are dashed red (#EF4444), labeled "∂y^c/∂Aᵏ"
      Stagger arrow opacity: A¹=100%, A²=85%, A³=95%, A⁴=70%, A⁵=90%, A⁶=80%
      (simulates different gradient magnitudes)

RIGHT COLUMN:
  Card with orange border:
    ClassNode component (Healthy variant) — glowing
    Glow effect: outer shadow 0 0 24px #22C55E 60%
    Label: "yᶜ = Healthy" accent text
    Below node: confidence scores stack
      "Healthy:  99.3%" green bar (full)
      "Bleached:  0.3%" amber bar (tiny)
      "Dead:      0.4%" red bar (tiny)
      Each: label + thin progress bar (4px height) + percentage

FORMULA BAR: "∂y^c/∂A^k_ij" span highlighted (orange bg, orange text)

ANNOTATION BOX (below center card, full width):
  bg-orange-50, border-orange-200, radius 12px, padding 16px
  "Larger gradients = that feature map has more influence on predicting Healthy coral.
   The arrows' thickness represents gradient magnitude ∂y^c/∂A^k."
  Inter 12px text-secondary
```

---

## 8. Frame 3 — Step 3: Pool α_k

**Purpose:** Show gradients condensing into scalar α_k weights displayed as vertical bars.

```
TOP BAR: class = Healthy
STEP BADGE: Step 3 · Global Average Pool (accent-violet)
HEADING: "Step 3 — Compute Importance Weights α_k"
Sub: "Each gradient map is spatially averaged to a single scalar α_k weight."

LEFT COLUMN:
  Card:
    InputCoralImage (Healthy) — dimmed (opacity 50%)

CENTER COLUMN:
  Card:
    Title: "Feature Maps — Condensing to Weights" heading-sm
    2×3 grid FeatureMapTile (State=Faded — 20% opacity)
    CONDENSING ARROWS: 6 small downward arrows below each tile
      pointing toward the alpha bar row below
      color accent-violet, 1.5px stroke

    ALPHA BAR ROW (below feature map grid, inside same card):
      6 AlphaBar components (State=Visible, class colour = #22C55E Healthy)
      Heights (Healthy class values):
        α₁=0.82 → 98px
        α₂=0.41 → 49px
        α₃=0.65 → 78px
        α₄=0.91 → 109px  ← tallest
        α₅=0.33 → 40px   ← shortest
        α₆=0.77 → 92px
      Values shown as text above each bar
      Bars arranged horizontally with 8px gaps

RIGHT COLUMN:
  Card with violet border:
    Title: "α_k = (1/Z) Σ_ij ∂y^c/∂A^k_ij" mono 12px accent-violet
    Description: "Global Average Pooling reduces each\n112×112 gradient map to\none scalar importance score."
    Gap 16px
    Ranked list:
      "① A⁴ — α=0.91 (highest)" bold
      "② A¹ — α=0.82"
      "③ A⁶ — α=0.77"
      "④ A³ — α=0.65"
      "⑤ A² — α=0.41"
      "⑥ A⁵ — α=0.33 (lowest)"
    Inter 12px, rank numbers accent-violet, rest text-secondary

FORMULA BAR: "α_k" span highlighted (violet bg, violet text)
```

---

## 9. Frame 4 — Step 4: Weighted Sum + ReLU + Heatmap

**Purpose:** Show the final heatmap appearing over the coral image. This is the payoff.

```
TOP BAR: class = Healthy
STEP BADGE: Step 4 · ReLU + Heatmap (accent-teal)
HEADING: "Step 4 — Final Grad-CAM Attention Heatmap"
Sub: "Feature maps × α_k weights are summed and ReLU-filtered, then overlaid on the input."

LEFT COLUMN — MAIN FOCUS (enlarged for this frame: 380px wide):
  Card with teal border + glow shadow 0 8px 40px #14B8A6 20%:
    Title: "Grad-CAM Output" heading-sm accent-teal
    InputCoralImage (Healthy) + HeatmapOverlay (Healthy, State=Visible) stacked
      Heatmap at 80% opacity over coral image
      Colorbar legend (vertical, right side of image):
        Thin rectangle 12×160px
        Fill: linear gradient top=red → yellow → green → cyan → blue
        Labels: "High" top, "Low" bottom, Inter 9px text-muted
    Caption below: "Model attention concentrated on\ncoral polyp clusters — confirms healthy classification"
    accent-teal bold 12px

CENTER COLUMN — Formula Breakdown (560px):
  Card:
    Title: "How the Heatmap Was Built" heading-sm
    Step-by-step vertical breakdown (4 rows):

    Row 1 — Weighted Maps:
      6 tiny FeatureMapTile thumbnails (40×40px, State=Weighted)
      Each with α value overlaid: "×0.82", "×0.41" etc. (green text)
      Arrow: "+" between each tile → "Σ" symbol at end

    Row 2 — Summed Map:
      Single FeatureMapTile (80×80px) showing merged activation
      Label: "Σ_k α_k · A^k" mono accent-teal

    Row 3 — ReLU Applied:
      Same tile but dimmer cells removed (negative activations set to 0)
      Label: "ReLU( · ) — negatives removed" caption text-muted
      Comparison: before/after tiles side by side with "|" separator

    Row 4 — Upsampled + Overlaid:
      Small thumbnail showing coral + heatmap
      Arrow → "224×224 output" label

RIGHT COLUMN:
  Card:
    Title: "Attention Profile" heading-sm
    Class badge: "Healthy — F1 0.986" (green pill)
    Gap 12px
    "Pattern: Tight center focus" caption
    "Dominant activation on coral polyp clusters and branching tips"
    body text-secondary
    Gap 16px
    Comparison table (3 rows):
      Class    | Pattern   | Spread
      Healthy  | Focused   | ██░░░ Narrow
      Bleached | Patchy    | ████░ Medium
      Dead     | Diffuse   | █████ Wide
    (Simple Figma table component, Inter 11px)

FORMULA BAR: "ReLU(" and "L_GradCAM" spans highlighted (teal bg, teal text)
```

---

## 10. Step Card Row — Shared Bottom Element

Place in all 5 frames at y=790. 4 cards, 320px each, 16px gap, horizontally centred.

```
CARD STRUCTURE (each):
  Size: 320 × 80px
  Corner radius: 12px
  Padding: 16px

CARD 1 — Forward Pass:
  Active in Frame 1
  Active style: bg white, border 2px accent-sky, top-left corner accent-sky square 4×4px
  Inactive style: bg-panel-dim, border border-default
  Content: "① Forward Pass" heading-sm | "Produces A^k feature maps" body

CARD 2 — Backpropagation:
  Active in Frame 2, accent-orange
  Content: "② Backpropagation" | "Computes ∂y^c/∂A^k gradients"

CARD 3 — Pool α_k:
  Active in Frame 3, accent-violet
  Content: "③ Pool α_k" | "Weights each feature map"

CARD 4 — Heatmap + ReLU:
  Active in Frame 4, accent-teal
  Content: "④ Heatmap + ReLU" | "L = ReLU( Σ_k α_k · A^k )"

Completed steps (frames after active): add "✓" prefix to card title, lighter border
```

---

## 11. Prototype Interactions

Set up in Figma's Prototype tab. Use **Smart Animate** for all transitions.

```
Idle → Frame 1:
  Trigger: Click button "1. Forward Pass" (add button hotspot in top bar)
  Animation: Smart Animate, ease-out, 400ms

Frame 1 → Frame 2:
  Trigger: Click "2. Backprop" button hotspot
  Animation: Smart Animate, ease-out, 400ms

Frame 2 → Frame 3:
  Trigger: Click "3. Pool α_k" button hotspot
  Animation: Smart Animate, ease-out, 400ms

Frame 3 → Frame 4:
  Trigger: Click "4. Heatmap" button hotspot
  Animation: Smart Animate, ease-in-out, 600ms (slower — payoff moment)

Any Frame → Idle:
  Trigger: Click "↺ Reset" button hotspot (top bar right side)
  Animation: Dissolve, 300ms

SMART ANIMATE REQUIREMENTS:
  All FeatureMapTile components must keep same layer name across frames
  All AlphaBar components must keep same layer name (Figma matches by name for Smart Animate)
  Position changes between frames will animate smoothly:
    - Feature maps: scale and opacity change (Idle→Active)
    - Alpha bars: height change (0→full in Frame 3)
    - Heatmap: opacity change (0→80% in Frame 4)
    - Formula highlights: colour change per frame
```

---

## 12. Class Selector Interaction

Add 3 prototype flows — one per class — or use Figma's **Variables** (if available):

```
Minimal approach (3 class variants per frame = 15 total frames):
  Frame naming: "F0-Healthy", "F0-Bleached", "F0-Dead", "F1-Healthy" etc.
  Class tab click → navigate to same step but different class frame

Component variants to duplicate per class:
  InputCoralImage: 3 variants (Healthy / Bleached / Dead)
  HeatmapOverlay:  3 variants
  ClassNode:       3 variants
  AlphaBar:        3 alpha value sets (see §3 hardcoded data below)
```

### Alpha Values per Class

```
         α₁    α₂    α₃    α₄    α₅    α₆
Healthy: 0.82  0.41  0.65  0.91  0.33  0.77
Bleached:0.55  0.79  0.44  0.88  0.71  0.63
Dead:    0.38  0.62  0.85  0.47  0.93  0.56
```

---

## 13. Export & Handoff Requirements

```
After Figma file is built, Claude Code must:

1. Share Figma file as "Anyone with link can view"
2. Export each frame as PNG 2× for documentation:
   - Filenames: gradcam_idle.png, gradcam_step1.png, gradcam_step2.png,
                gradcam_step3.png, gradcam_step4.png
3. Export component library as PNG sprite sheet (optional)
4. Share prototype link (View Mode URL with prototype interactions)
```

---

## 14. Claude Code Execution Sequence

```
STEP 1 — Verify Figma MCP is connected
  Call: use_figma → whoami  (confirm authentication)

STEP 2 — Create file
  Call: use_figma → create_new_file
  Name: "GradCAM Simulation — Coral Reef CNN EfficientNetB0"

STEP 3 — Build component library
  For each component in §2 (FeatureMapTile, AlphaBar, etc.):
    Call: use_figma → create component with specified geometry, fills, text

STEP 4 — Build Frame 0 (Idle)
  Create 1440×900 frame, place component instances per §5

STEP 5 — Build Frames 1–4 (Steps 1–4)
  Duplicate Frame 0 for each, modify per §6–§9
  Keep layer names identical for Smart Animate

STEP 6 — Add prototype connections
  Call: use_figma → set prototype interactions per §11

STEP 7 — Set view settings
  Zoom: Fit frames in viewport
  Grid: 8px baseline grid on all frames

STEP 8 — Share
  Get shareable view link
  Get prototype link
  Report both URLs to user
```

---

> Student: Muhammad Luqman Haziq Bin Mohamad Lofi (221022249)
> Project: Coral Reef Health Assessment via CNN-based Image Analysis
> Architecture: EfficientNetB0 + 5-seed SWA Ensemble + Grad-CAM
> Design tool: Figma (via Claude Code Figma MCP)
> Frames: 5 (Idle + 4 steps) with Smart Animate prototype interactions
