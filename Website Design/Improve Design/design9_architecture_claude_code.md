# Claude Code Task: Redesign Architecture Comparison Section in design9.html

## Context

File: `design9.html` (3184 lines)
Target: The **Architecture Comparison tab** — the third tab inside the 3-tab switcher section.
Scope: Only modify `id="layout-architecture"` div (lines ~706–827) and the `populateArchitecture()` JS function (lines ~3110–3174). Do NOT touch other sections.

---

## Current State (What Exists)

### Tab switcher (DO NOT MODIFY)
```html
<button id="tab-architecture" onclick="switchTab('architecture')">
  <i data-lucide="git-compare"></i>
  <span>Architecture Comparison</span>
</button>
```

### Current architecture section HTML (REPLACE this block)
```html
<div id="layout-architecture" class="space-y-8 hidden">
  <!-- Block G: Summary Comparison Table -->
  <!-- Futuristic Architecture Comparison Graph (SVG) -->
</div>
```

### Current graph: Static SVG with hardcoded pixel coordinates — NO interactivity, NO tooltips, NO hover states.

### Current `populateArchitecture()` function:
- Reads from `metricsData.architecture_comparison` (Flask API response)
- Falls back to hardcoded data if API missing
- Currently injects base64 PNG images into `arch-acc-params`, `arch-f1-chart`, `arch-cm-img` containers — these containers do NOT exist yet in the HTML (they are referenced in JS but missing from the DOM)

---

## Task: Replace the Architecture Comparison Section

Replace the contents of `id="layout-architecture"` with this improved layout.

### New Layout (Top to Bottom)

```
[ 3 Metric Cards Row ]
[ Custom Legend ]
[ Interactive Scatter Chart (Chart.js) — replaces static SVG ]
[ Summary Table ]
[ Key Findings — 3 bullet points ]
```

---

## New HTML Block

Replace the entire `<div id="layout-architecture" ...>` block with:

```html
<div id="layout-architecture" class="space-y-8 hidden">

  <!-- Metric Cards -->
  <div class="grid grid-cols-3 gap-4">
    <div class="bg-[#131a2b] border border-gray-800 rounded-2xl p-5 text-center">
      <p class="text-gray-400 text-xs uppercase tracking-widest mb-1">Best Accuracy</p>
      <p class="text-2xl font-bold text-white">98.11%</p>
      <p class="text-teal-400 text-xs mt-1">EfficientNetB0 Ensemble</p>
    </div>
    <div class="bg-[#131a2b] border border-gray-800 rounded-2xl p-5 text-center">
      <p class="text-gray-400 text-xs uppercase tracking-widest mb-1">Fewest Parameters</p>
      <p class="text-2xl font-bold text-white">20.3M</p>
      <p class="text-teal-400 text-xs mt-1">EfficientNetB0 Ensemble</p>
    </div>
    <div class="bg-[#131a2b] border border-gray-800 rounded-2xl p-5 text-center">
      <p class="text-gray-400 text-xs uppercase tracking-widest mb-1">Best Macro F1</p>
      <p class="text-2xl font-bold text-white">0.98</p>
      <p class="text-teal-400 text-xs mt-1">EfficientNetB0 Ensemble</p>
    </div>
  </div>

  <!-- Chart Card -->
  <div class="bg-[#131a2b] border border-gray-800 rounded-2xl p-6">
    <h4 class="text-lg font-semibold mb-4 text-gray-200">Model Size vs Test Accuracy</h4>

    <!-- Custom Legend -->
    <div class="flex gap-6 mb-4 flex-wrap">
      <span class="flex items-center gap-2 text-xs text-gray-300">
        <span style="width:12px;height:12px;border-radius:50%;background:#2DD4BF;display:inline-block"></span>
        EfficientNetB0 Ensemble
      </span>
      <span class="flex items-center gap-2 text-xs text-gray-300">
        <span style="width:12px;height:12px;border-radius:3px;background:#F43F5E;display:inline-block"></span>
        ResNet50 Single
      </span>
      <span class="flex items-center gap-2 text-xs text-gray-300">
        <span style="width:0;height:0;border-left:7px solid transparent;border-right:7px solid transparent;border-bottom:12px solid #3B82F6;display:inline-block"></span>
        ConvNeXtTiny Single
      </span>
    </div>

    <!-- Chart -->
    <div style="position:relative; width:100%; height:300px;">
      <canvas id="archScatterChart"
        role="img"
        aria-label="Scatter chart: EfficientNetB0 at 20.3M params 98.11% accuracy, ResNet50 at 23.6M 98.11%, ConvNeXtTiny at 27.8M 97.48%">
        EfficientNetB0: 20.3M params, 98.11%. ResNet50: 23.6M, 98.11%. ConvNeXtTiny: 27.8M, 97.48%.
      </canvas>
    </div>

    <!-- Tooltip div -->
    <div id="arch-tooltip" style="position:fixed;display:none;background:#1e2536;border:1px solid rgba(45,212,191,0.3);border-radius:10px;padding:10px 14px;font-size:12px;pointer-events:none;z-index:999;min-width:180px;color:#e2e8f0;"></div>
  </div>

  <!-- Summary Table -->
  <div class="bg-[#131a2b] border border-gray-800 rounded-2xl p-6 overflow-x-auto">
    <h4 class="text-lg font-semibold mb-4 text-gray-200">Architecture Comparison Summary</h4>
    <table class="w-full text-sm text-left border-collapse">
      <thead class="text-gray-400 text-xs uppercase bg-[#1e2536]">
        <tr>
          <th class="px-4 py-3 rounded-l-lg">Model</th>
          <th class="px-4 py-3 text-right">Type</th>
          <th class="px-4 py-3 text-right">Params (M)</th>
          <th class="px-4 py-3 text-right">Accuracy</th>
          <th class="px-4 py-3 text-right">Macro F1</th>
          <th class="px-4 py-3 text-right rounded-r-lg">Errors</th>
        </tr>
      </thead>
      <tbody class="divide-y divide-gray-800" id="arch-summary-body">
        <!-- Populated by populateArchitecture() -->
      </tbody>
    </table>
  </div>

  <!-- Key Findings -->
  <div class="bg-[#131a2b] border border-gray-800 rounded-2xl p-6">
    <h4 class="text-lg font-semibold mb-4 text-gray-200">Key Findings</h4>
    <ul class="space-y-3 text-sm text-gray-300">
      <li class="flex gap-3">
        <span class="text-teal-400 font-bold mt-0.5">→</span>
        <span>EfficientNetB0 Ensemble achieves the highest macro F1 (0.98) with the fewest parameters (20.3M), demonstrating superior parameter efficiency.</span>
      </li>
      <li class="flex gap-3">
        <span class="text-blue-400 font-bold mt-0.5">→</span>
        <span>ResNet50 Single matches EfficientNetB0's accuracy (98.11%) but requires 16% more parameters and yields a lower macro F1 (0.96).</span>
      </li>
      <li class="flex gap-3">
        <span class="text-rose-400 font-bold mt-0.5">→</span>
        <span>ConvNeXtTiny Single uses the most parameters (27.8M) yet achieves the lowest accuracy (97.48%), indicating diminishing returns at higher model complexity.</span>
      </li>
    </ul>
  </div>

</div>
```

---

## Chart.js Script to Add

Add this script block **just before `</script>` of the main script tag** (around line 3182), or as a separate `<script>` block before `</body>`:

```javascript
// ── Architecture Scatter Chart ──────────────────────────────────────
function initArchScatterChart() {
  const canvas = document.getElementById('archScatterChart');
  if (!canvas || canvas._chartInstance) return;

  const models = [
    { label: 'EfficientNetB0 Ensemble', x: 20.27, y: 98.11, f1: '0.98', errors: 3, shape: 'circle', color: '#2DD4BF' },
    { label: 'ResNet50 Single',         x: 23.59, y: 98.11, f1: '0.96', errors: 3, shape: 'rect',   color: '#F43F5E' },
    { label: 'ConvNeXtTiny Single',     x: 27.82, y: 97.48, f1: '0.97', errors: 4, shape: 'triangle', color: '#3B82F6' },
  ];

  const shapePlugin = {
    id: 'customShapes',
    afterDatasetsDraw(chart) {
      const ctx = chart.ctx;
      chart.data.datasets.forEach((ds, di) => {
        const meta = chart.getDatasetMeta(di);
        meta.data.forEach(el => {
          const m = models[di];
          const { x, y } = el.getCenterPoint();
          ctx.save();
          ctx.fillStyle = m.color;
          if (m.shape === 'circle') {
            ctx.beginPath(); ctx.arc(x, y, 9, 0, Math.PI * 2); ctx.fill();
            // glow ring for EfficientNetB0
            ctx.globalAlpha = 0.25;
            ctx.beginPath(); ctx.arc(x, y, 15, 0, Math.PI * 2); ctx.fill();
            ctx.globalAlpha = 1;
          } else if (m.shape === 'rect') {
            ctx.fillRect(x - 8, y - 8, 16, 16);
          } else {
            ctx.beginPath(); ctx.moveTo(x, y - 10); ctx.lineTo(x + 9, y + 7); ctx.lineTo(x - 9, y + 7); ctx.closePath(); ctx.fill();
          }
          ctx.restore();
        });
      });
    }
  };

  const chartInstance = new Chart(canvas, {
    type: 'scatter',
    data: {
      datasets: models.map(m => ({
        label: m.label,
        data: [{ x: m.x, y: m.y }],
        pointRadius: 0,
        pointHoverRadius: 0,
      }))
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: { enabled: false }
      },
      scales: {
        x: {
          min: 18, max: 30,
          title: { display: true, text: 'Number of parameters (millions)', color: '#94A3B8', font: { size: 12 } },
          ticks: { color: '#94A3B8', font: { size: 11 }, stepSize: 2 },
          grid: { color: 'rgba(148,163,184,0.1)' },
          border: { color: 'rgba(148,163,184,0.3)' }
        },
        y: {
          min: 97.0, max: 98.6,
          title: { display: true, text: 'Test accuracy (%)', color: '#94A3B8', font: { size: 12 } },
          ticks: { color: '#94A3B8', font: { size: 11 }, callback: v => v.toFixed(1) + '%' },
          grid: { color: 'rgba(148,163,184,0.1)' },
          border: { color: 'rgba(148,163,184,0.3)' }
        }
      },
      layout: { padding: { top: 24, right: 30, bottom: 8, left: 8 } }
    },
    plugins: [shapePlugin]
  });

  canvas._chartInstance = chartInstance;

  // Tooltip
  const tip = document.getElementById('arch-tooltip');
  canvas.addEventListener('mousemove', e => {
    const rect = canvas.getBoundingClientRect();
    const mx = e.clientX - rect.left;
    const my = e.clientY - rect.top;
    let hit = null;
    chartInstance.data.datasets.forEach((ds, di) => {
      const meta = chartInstance.getDatasetMeta(di);
      meta.data.forEach(el => {
        const { x, y } = el.getCenterPoint();
        if (Math.abs(mx - x) < 16 && Math.abs(my - y) < 16) hit = models[di];
      });
    });
    if (hit) {
      tip.innerHTML = `
        <div style="font-weight:600;font-size:13px;color:#2DD4BF;margin-bottom:6px">${hit.label}</div>
        <div style="color:#94A3B8">Parameters: <span style="color:#e2e8f0">${hit.x}M</span></div>
        <div style="color:#94A3B8">Accuracy: <span style="color:#e2e8f0">${hit.y.toFixed(2)}%</span></div>
        <div style="color:#94A3B8">Macro F1: <span style="color:#e2e8f0">${hit.f1}</span></div>
        <div style="color:#94A3B8">Errors: <span style="color:#e2e8f0">${hit.errors}</span></div>`;
      tip.style.display = 'block';
      tip.style.left = (e.clientX + 16) + 'px';
      tip.style.top  = (e.clientY - 10) + 'px';
    } else {
      tip.style.display = 'none';
    }
  });
  canvas.addEventListener('mouseleave', () => { tip.style.display = 'none'; });
}
// ────────────────────────────────────────────────────────────────────
```

---

## Update `switchTab()` Function

Find the existing `switchTab` function and ensure it calls `initArchScatterChart()` when the architecture tab is activated:

```javascript
// Inside switchTab(), after showing layout-architecture:
if (tabName === 'architecture') {
  populateArchitecture();
  // Add this line:
  setTimeout(initArchScatterChart, 50); // slight delay ensures canvas is visible
}
```

---

## Update `populateArchitecture()` Function

The function already handles the summary table correctly. **Remove** the three lines referencing `arch-acc-params`, `arch-f1-chart`, `arch-cm-img` (lines 3161–3173) since those containers no longer exist in the new layout:

```javascript
// DELETE these lines from populateArchitecture():
const cAcc = document.getElementById('arch-acc-params');
const cF1  = document.getElementById('arch-f1-chart');
const cCm  = document.getElementById('arch-cm-img');
if (cAcc && arch.accuracy_vs_parameters) { ... }
if (cF1 && arch.per_class_f1) { ... }
if (cCm && arch.confusion_matrix_three_models) { ... }
```

The table population logic (`arch-summary-body`) remains unchanged.

---

## CDN Dependency

Chart.js is already loaded in design9.html. Verify this line exists in `<head>` or before `</body>`:
```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js"></script>
```
If missing, add it before the main `<script>` block.

---

## Design Tokens (Match Existing design9.html Style)

| Element | Value |
|---|---|
| Card background | `#131a2b` |
| Card border | `border-gray-800` / `rgba(55,65,81,1)` |
| Card radius | `rounded-2xl` |
| Section text | `text-gray-200` |
| Muted text | `#94A3B8` |
| EfficientNetB0 color | `#2DD4BF` (teal) |
| ResNet50 color | `#F43F5E` (rose) |
| ConvNeXtTiny color | `#3B82F6` (blue) |
| Grid lines | `rgba(148,163,184,0.1)` |

---

## Summary of Changes

| Location | Action |
|---|---|
| `id="layout-architecture"` div | Replace entire block with new HTML |
| `populateArchitecture()` function | Remove 3 dead container references at end |
| `switchTab()` function | Add `setTimeout(initArchScatterChart, 50)` for architecture tab |
| New JS function | Add `initArchScatterChart()` before `</script>` |
| Chart.js CDN | Verify it exists; add if missing |

**Do NOT modify**: tab switcher HTML, `switchTab()` logic beyond the one addition, any other section, CSS classes outside `layout-architecture`.
