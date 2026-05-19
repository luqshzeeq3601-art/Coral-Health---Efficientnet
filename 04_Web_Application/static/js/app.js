/* ============================================================
   Coral Health Assessment using CNN — Interactive Frontend Logic
   ============================================================ */

let currentFile = null;

// ============================================================
// Navigation
// ============================================================
function switchPage(page) {
    // Update nav
    document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
    document.querySelector(`.nav-item[data-page="${page}"]`).classList.add('active');

    // Switch page
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
    document.getElementById(`page-${page}`).classList.add('active');

    // Load metrics on first visit
    if (page === 'metrics') {
        loadMetrics();
    }

    // Close mobile sidebar
    document.getElementById('sidebar').classList.remove('open');
}

function toggleSidebar() {
    document.getElementById('sidebar').classList.toggle('open');
}

// ============================================================
// Sidebar Collapse (Desktop Toggle Arrow)
// ============================================================
function collapseSidebar() {
    const sidebar = document.getElementById('sidebar');
    const main = document.getElementById('mainContent');
    sidebar.classList.toggle('collapsed');
    main.classList.toggle('sidebar-collapsed');
}

// ============================================================
// Upload Handling
// ============================================================
function handleDragOver(e) {
    e.preventDefault();
    e.stopPropagation();
    document.getElementById('uploadZone').classList.add('dragover');
}

function handleDragLeave(e) {
    e.preventDefault();
    e.stopPropagation();
    document.getElementById('uploadZone').classList.remove('dragover');
}

// Drop-zone drag-enter/leave visual feedback (design9 uses #drop-zone)
function initDropZoneFeedback() {
    const dz = document.getElementById('drop-zone');
    if (!dz) return;
    dz.addEventListener('dragenter', () => {
        dz.classList.add('border-teal-400', 'bg-teal-50', 'scale-[1.01]');
    });
    dz.addEventListener('dragleave', () => {
        dz.classList.remove('border-teal-400', 'bg-teal-50', 'scale-[1.01]');
    });
    dz.addEventListener('drop', () => {
        dz.classList.remove('border-teal-400', 'bg-teal-50', 'scale-[1.01]');
    });
}

function handleDrop(e) {
    e.preventDefault();
    e.stopPropagation();
    document.getElementById('uploadZone').classList.remove('dragover');
    const files = e.dataTransfer.files;
    if (files.length > 0 && files[0].type.startsWith('image/')) {
        setFile(files[0]);
    }
}

function handleFileSelect(e) {
    if (e.target.files.length > 0) {
        setFile(e.target.files[0]);
    }
}

function setFile(file) {
    currentFile = file;
    const reader = new FileReader();
    reader.onload = (e) => {
        document.getElementById('previewImage').src = e.target.result;
        document.getElementById('uploadPlaceholder').style.display = 'none';
        document.getElementById('uploadPreview').style.display = 'block';
        document.getElementById('analyzeBtn').disabled = false;
    };
    reader.readAsDataURL(file);

    // Reset results
    resetResults();
}

function clearUpload() {
    currentFile = null;
    document.getElementById('fileInput').value = '';
    document.getElementById('uploadPlaceholder').style.display = 'flex';
    document.getElementById('uploadPreview').style.display = 'none';
    document.getElementById('analyzeBtn').disabled = true;
    resetResults();
}

function resetResults() {
    document.getElementById('emptyState').style.display = 'block';
    document.getElementById('loadingState').style.display = 'none';
    document.getElementById('resultPrimary').style.display = 'none';
    document.getElementById('resultsContent').style.display = 'none';
    document.getElementById('uncertaintyBanner').style.display = 'none';
    document.getElementById('resultDescription').innerHTML = '';
    document.getElementById('resultRecommendation').innerHTML = '';
    document.getElementById('probabilityBars').innerHTML = '';
    document.getElementById('modelGrid').innerHTML = '';
}

// ============================================================
// Prediction
// ============================================================
async function runPrediction() {
    if (!currentFile) return;

    const btn = document.getElementById('analyzeBtn');
    btn.disabled = true;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> <span>Analyzing...</span>';

    document.getElementById('emptyState').style.display = 'none';
    document.getElementById('loadingState').style.display = 'block';
    document.getElementById('resultPrimary').style.display = 'none';
    document.getElementById('resultsContent').style.display = 'none';

    const formData = new FormData();
    formData.append('image', currentFile);

    try {
        const response = await fetch('/api/predict', { method: 'POST', body: formData });

        if (!response.ok) {
            const errData = await response.json();
            throw new Error(errData.error || 'Server error');
        }

        const data = await response.json();
        displayResults(data);

    } catch (err) {
        document.getElementById('loadingState').style.display = 'none';
        document.getElementById('resultPrimary').style.display = 'none';
        document.getElementById('emptyState').style.display = 'flex';
        document.getElementById('emptyState').innerHTML = `
            <i class="fas fa-exclamation-circle" style="color: var(--dead); font-size: 2rem;"></i>
            <p style="color: var(--dead);">${err.message}</p>
            <small style="color: var(--text-muted);">Check console for details.</small>
        `;
        console.error('Prediction error:', err);
    } finally {
        btn.disabled = false;
        btn.innerHTML = '<i class="fas fa-microscope"></i> <span>Run Assessment</span>';
    }
}

// ============================================================
// Severity colour system
// ============================================================
const SEVERITY_COLORS = {
    Healthy:  { bar: 'bg-emerald-500', badge: 'bg-emerald-500', border: 'border-emerald-400', icon: 'leaf',        iconColor: 'text-emerald-600', css: '#10b981' },
    Bleached: { bar: 'bg-amber-400',   badge: 'bg-amber-500',   border: 'border-amber-400',   icon: 'thermometer', iconColor: 'text-amber-500',   css: '#f59e0b' },
    Dead:     { bar: 'bg-red-500',     badge: 'bg-red-500',     border: 'border-red-400',     icon: 'skull',       iconColor: 'text-red-500',     css: '#ef4444' },
};

// ============================================================
// Display Results
// ============================================================
function displayResults(data) {
    const loadingEl = document.getElementById('loadingState');
    const emptyEl = document.getElementById('emptyState');
    const primaryEl = document.getElementById('resultPrimary');
    const contentEl = document.getElementById('resultsContent');

    if (loadingEl) loadingEl.style.display = 'none';
    if (emptyEl) emptyEl.style.display = 'none';

    // ── Design9 result card path ──
    const resultArea = document.getElementById('result-area');
    if (resultArea) {
        _displayResultsDesign9(data);
        return;
    }

    // ── Legacy result card path ──
    if (primaryEl) primaryEl.style.display = 'block';
    if (contentEl) contentEl.style.display = 'block';

    const colorMap = { 'Healthy': 'var(--healthy)', 'Bleached': 'var(--bleached)', 'Dead': 'var(--dead)' };
    const classMap = { 'Healthy': 'healthy', 'Bleached': 'bleached', 'Dead': 'dead' };
    const color = colorMap[data.prediction] || 'var(--accent)';
    const fallbackStatusByPrediction = {
        Healthy: {
            severity: 'Good',
            description: 'Coral appears healthy with normal coloration and structure.',
            recommendation: 'Continue monitoring. Maintain water quality parameters.'
        },
        Bleached: {
            severity: 'Warning',
            description: 'Coral shows signs of bleaching - loss of symbiotic algae.',
            recommendation: 'Investigate stressors: temperature, pH, pollution. Consider intervention.'
        },
        Dead: {
            severity: 'Critical',
            description: 'Coral appears to be dead (algae covered or skeletal).',
            recommendation: 'Document location. Assess potential for recovery or substrate rehabilitation.'
        }
    };
    const status = data.status || data.status_info || fallbackStatusByPrediction[data.prediction] || { severity: '', description: '', recommendation: '' };

    const badgeIconEl = document.getElementById('badgeIcon');
    if (badgeIconEl) {
        const sc = SEVERITY_COLORS[data.prediction];
        badgeIconEl.innerHTML = sc ? `<i data-lucide="${sc.icon}" class="w-5 h-5 ${sc.iconColor}"></i>` : '';
        if (typeof lucide !== 'undefined') lucide.createIcons();
    }

    const resultLabelEl = document.getElementById('resultLabel');
    if (resultLabelEl) { resultLabelEl.textContent = data.prediction; resultLabelEl.style.color = color; }

    const severityEl = document.getElementById('resultSeverity');
    if (severityEl) { severityEl.textContent = status.severity || ''; severityEl.className = 'severity ' + (status.severity || '').toLowerCase(); }

    const conf = data.confidence;
    const confValueEl = document.getElementById('confidenceValue');
    if (confValueEl) { confValueEl.textContent = conf.toFixed(1) + '%'; confValueEl.style.color = color; }

    const ring = document.getElementById('confRingFill');
    if (ring) {
        const circumference = 2 * Math.PI * 52;
        ring.style.strokeDasharray = circumference;
        ring.style.stroke = color;
        ring.style.strokeDashoffset = circumference;
        requestAnimationFrame(() => {
            ring.style.transition = 'stroke-dashoffset 1s ease-out';
            ring.style.strokeDashoffset = circumference - (conf / 100) * circumference;
        });
    }

    const uncertaintyEl = document.getElementById('uncertaintyBanner');
    if (uncertaintyEl) uncertaintyEl.style.display = data.uncertainty ? 'flex' : 'none';

    const descEl = document.getElementById('resultDescription');
    if (descEl) descEl.innerHTML = status.description || '';
    const recEl = document.getElementById('resultRecommendation');
    if (recEl) recEl.innerHTML = `<strong>Recommendation:</strong> ${status.recommendation || ''}`;

    const probsEl = document.getElementById('probabilityBars');
    if (probsEl) {
        probsEl.innerHTML = '';
        const probabilities = data.probabilities || {};
        for (const [cls, prob] of Object.entries(probabilities)) {
            if (prob < 1.0) continue;
            const barClass = classMap[cls] || 'healthy';
            const pct = prob.toFixed(2);
            probsEl.innerHTML += `
                <div class="prob-item">
                    <span class="prob-label">${cls}</span>
                    <div class="prob-bar-container">
                        <div class="prob-bar ${barClass}" style="width: 0%; background: ${colorMap[cls]};" data-width="${pct}%"></div>
                    </div>
                    <span class="prob-value-outer">${pct}%</span>
                </div>`;
        }
        probsEl.querySelectorAll('.prob-bar').forEach((bar, i) => {
            setTimeout(() => { bar.style.width = bar.dataset.width; }, 100 + i * 120);
        });
    }

    const grid = document.getElementById('modelGrid');
    if (grid) {
        grid.innerHTML = '';
        if (data.individual_models) {
            data.individual_models.forEach((m, i) => {
                const mColor = colorMap[m.prediction] || 'var(--accent)';
                grid.innerHTML += `
                    <div class="model-item">
                        <div class="model-item-header">Model ${i + 1} (Seed ${m.fold})</div>
                        <div class="model-item-pred" style="color: ${mColor};">${m.prediction}</div>
                        <div class="model-item-conf">${m.confidence.toFixed(1)}% confidence</div>
                    </div>`;
            });
        }
    }

    const gcSection = document.getElementById('gradcamSection');
    if (gcSection) {
        if (data.gradcam && data.gradcam.heatmap) {
            gcSection.style.display = 'block';
            const origImg = document.getElementById('gradcamOriginal');
            const heatImg = document.getElementById('gradcamHeatmap');
            const overImg = document.getElementById('gradcamOverlay');
            [origImg, heatImg, overImg].forEach(img => {
                img.style.opacity = '0';
                img.style.transform = 'translateY(10px) scale(0.98)';
                img.style.transition = 'all 0.4s ease-out';
            });
            setTimeout(() => {
                origImg.src = 'data:image/png;base64,' + data.original_image;
                heatImg.src = 'data:image/png;base64,' + data.gradcam.heatmap;
                overImg.src = 'data:image/png;base64,' + data.gradcam.overlay;
                setTimeout(() => {
                    origImg.style.opacity = '1'; origImg.style.transform = 'translateY(0) scale(1)';
                    setTimeout(() => { heatImg.style.opacity = '1'; heatImg.style.transform = 'translateY(0) scale(1)'; }, 100);
                    setTimeout(() => { overImg.style.opacity = '1'; overImg.style.transform = 'translateY(0) scale(1)'; }, 200);
                }, 50);
            }, 50);
        } else {
            gcSection.style.display = 'none';
        }
    }

    if (window.innerWidth <= 1024 && contentEl) {
        contentEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

// ============================================================
// Design9 result rendering (modern card layout)
// ============================================================
function _displayResultsDesign9(data) {
    const resultArea = document.getElementById('result-area');
    const loadingEl  = document.getElementById('loading');
    const skeleton   = document.getElementById('gradcam-skeleton');

    if (loadingEl) loadingEl.classList.add('hidden');

    // Hide skeleton if visible
    if (skeleton) skeleton.classList.add('hidden');

    resultArea.classList.remove('hidden');
    resultArea.classList.add('flex');

    // Entrance animation — restart each time
    resultArea.classList.remove('result-enter');
    void resultArea.offsetWidth;
    resultArea.classList.add('result-enter');

    const pred = data.prediction;
    const conf = data.confidence;
    const colors = SEVERITY_COLORS[pred] || SEVERITY_COLORS['Dead'];

    // ── Result icon (Lucide, severity-coloured) ──
    const iconContainer = document.getElementById('result-icon-container');
    const iconEl = document.getElementById('result-icon');
    if (iconContainer && iconEl) {
        iconContainer.className = `w-16 h-16 rounded-full flex items-center justify-center shrink-0`;
        iconContainer.style.backgroundColor = colors.css + '1a';
        iconEl.setAttribute('data-lucide', colors.icon);
        iconEl.className = `w-8 h-8 ${colors.iconColor}`;
        if (typeof lucide !== 'undefined') lucide.createIcons();
    }

    // ── Prediction label ──
    const classEl = document.getElementById('result-class');
    if (classEl) { classEl.textContent = pred; classEl.style.color = colors.css; }

    const modelLabel = document.getElementById('model-used-label');
    if (modelLabel) modelLabel.textContent = data.model_used ? `Model: ${data.model_used}` : '';

    // ── Confidence badge (severity colour + pulse on high conf) ──
    const badgeBg = document.getElementById('badge-bg');
    const badgeConf = document.getElementById('result-badge-confidence');
    if (badgeBg && badgeConf) {
        badgeBg.className = `px-6 py-2 rounded-full text-white font-bold text-xl shadow-sm w-fit ${colors.badge}`;
        badgeConf.textContent = conf.toFixed(1) + '%';
        badgeBg.classList.remove('badge-pulse');
        if (conf >= 90) {
            void badgeBg.offsetWidth;
            badgeBg.classList.add('badge-pulse');
        }
    }

    // ── Confidence bar (severity colour, animated from 0) ──
    const mainBar = document.getElementById('main-result-bar');
    const mainConfText = document.getElementById('main-result-confidence-text');
    if (mainBar) {
        mainBar.className = `h-full rounded-full transition-all duration-1000 ease-out ${colors.bar} relative`;
        mainBar.style.width = '0%';
        requestAnimationFrame(() => {
            mainBar.style.width = conf + '%';
        });
    }
    if (mainConfText) mainConfText.textContent = conf.toFixed(1) + '%';

    // ── Class probability bars (staggered, severity-coloured for winning class) ──
    const probsContainer = document.getElementById('result-probs');
    if (probsContainer) {
        probsContainer.innerHTML = '';
        const probabilities = data.probabilities || {};
        const BAR_COLORS = {
            Healthy:  'bg-emerald-500',
            Bleached: 'bg-amber-400',
            Dead:     'bg-red-500',
        };
        const entries = Object.entries(probabilities).filter(([, v]) => v >= 0.1);
        entries.forEach(([cls, prob], i) => {
            const barColor = BAR_COLORS[cls] || 'bg-teal-500';
            const pct = prob.toFixed(1);
            const row = document.createElement('div');
            row.className = 'flex items-center gap-3';
            row.innerHTML = `
                <span class="text-[11px] font-bold text-gray-500 uppercase tracking-widest w-16 shrink-0">${cls}</span>
                <div class="flex-1 h-2.5 bg-gray-100 rounded-full overflow-hidden">
                    <div class="prob-bar-fill h-full rounded-full ${barColor}" data-width="${pct}%"></div>
                </div>
                <span class="text-xs font-bold text-gray-700 tabular-nums w-10 text-right">${pct}%</span>`;
            probsContainer.appendChild(row);

            // Staggered fill
            const fill = row.querySelector('.prob-bar-fill');
            setTimeout(() => { fill.style.width = pct + '%'; }, i * 120);
        });
    }

    // ── Result card border accent ──
    const resultCard = resultArea.querySelector('.rounded-\\[24px\\]');
    if (resultCard) {
        resultCard.classList.remove('border-emerald-400', 'border-amber-400', 'border-red-400', 'border-gray-100');
        resultCard.classList.add(colors.border);
    }

    // ── Uncertainty banner ──
    const uncertaintyCardEl = document.getElementById('uncertainty-banner-card');
    if (uncertaintyCardEl) {
        uncertaintyCardEl.classList.toggle('hidden', !data.uncertainty);
        if (typeof lucide !== 'undefined') lucide.createIcons();
    }

    // ── Run Again button ──
    const runAgainContainer = document.getElementById('run-again-container');
    if (runAgainContainer) runAgainContainer.classList.remove('hidden');

    // ── Grad-CAM section ──
    const demoGradcam = document.getElementById('demo-gradcam');
    const gcDisabledMsg = document.getElementById('gradcam-disabled-msg');
    const gcPlaceholder = document.getElementById('gradcam-placeholder');
    const gcRerunMsg = document.getElementById('gradcam-rerun-msg');

    if (data.gradcam && data.gradcam.heatmap && data.original_image) {
        if (skeleton) skeleton.classList.add('hidden');
        if (gcDisabledMsg) gcDisabledMsg.classList.add('hidden');
        if (gcPlaceholder) gcPlaceholder.classList.add('hidden');
        if (gcRerunMsg) gcRerunMsg.classList.add('hidden');

        document.getElementById('gc-original').src = 'data:image/png;base64,' + data.original_image;
        document.getElementById('gc-overlay').src  = 'data:image/png;base64,' + data.gradcam.overlay;
        document.getElementById('gc-heatmap').src  = 'data:image/png;base64,' + data.gradcam.heatmap;

        if (demoGradcam) {
            demoGradcam.classList.remove('hidden', 'gradcam-enter');
            void demoGradcam.offsetWidth;
            demoGradcam.classList.add('flex', 'gradcam-enter');
        }
    } else if (data.gradcam === undefined || (data.gradcam && !data.gradcam.heatmap)) {
        if (demoGradcam) { demoGradcam.classList.add('hidden'); demoGradcam.classList.remove('flex'); }
        if (gcPlaceholder) gcPlaceholder.classList.remove('hidden');
    }

    // Update shared state for toggle
    if (typeof lastOriginal !== 'undefined') {
        lastOriginal = data.original_image || null;
        lastGradcam  = (data.gradcam && data.gradcam.heatmap) ? data.gradcam : null;
    }

    // Update chatbot context
    if (typeof latestPredictionContext !== 'undefined') {
        latestPredictionContext = {
            prediction: pred,
            confidence: conf,
            probabilities: data.probabilities || {},
            uncertainty: data.uncertainty || false
        };
    }

    // Refresh lucide icons rendered by JS
    if (typeof lucide !== 'undefined') lucide.createIcons();
    if (typeof refreshDecorativeIcons === 'function') refreshDecorativeIcons();
}

// ============================================================
// Collapsibles
// ============================================================
function toggleSection(id) {
    const el = document.getElementById(id);
    const toggle = document.getElementById(id + 'Toggle');
    if (el.style.display === 'none') {
        el.style.display = 'block';
        toggle.classList.add('open');
    } else {
        el.style.display = 'none';
        toggle.classList.remove('open');
    }
}

// ============================================================
// Metrics Page
// ============================================================
// Metrics Page
let metricsData = null; // Store fetched data
let currentPhase = 'deployment'; // 'research' or 'deployment'

async function loadMetrics() {
    if (metricsData) return; // Already loaded

    try {
        const response = await fetch('/api/metrics');
        if (!response.ok) {
            throw new Error(`Server returned ${response.status}: ${response.statusText}`);
        }
        const data = await response.json();
        if (data.error) {
            throw new Error(data.error);
        }
        metricsData = data;

        // Initial Render
        renderMetrics(currentPhase);

    } catch (err) {
        console.error('Failed to load metrics:', err);
        metricsData = null; // Reset so retry is possible
        const reportEl = document.getElementById('reportTable');
        if (reportEl) reportEl.innerHTML = `<div class="alert alert-danger">Error loading metrics: ${err.message}</div>`;
    }
}

function switchMetricPhase(phase) {
    currentPhase = phase;

    // Update Toggle UI
    document.querySelectorAll('.phase-btn').forEach(btn => btn.classList.remove('active'));
    document.getElementById(`btn-${phase}`).classList.add('active');

    renderMetrics(phase);
}

function renderMetrics(phase) {
    if (!metricsData || !metricsData[phase]) return;

    const data = metricsData[phase];

    // Summary Cards
    if (data.model_info) {
        document.getElementById('metricAccuracy').textContent = data.model_info.accuracy;
        document.getElementById('metricSamples').textContent = data.model_info.total_samples ? data.model_info.total_samples.toLocaleString() : 'N/A';
        document.getElementById('metricErrors').textContent = data.model_info.total_errors;

        // Hide models count for research if not applicable, or show generic
        const modelsEl = document.getElementById('metricModels');
        if (modelsEl) modelsEl.textContent = data.model_info.total_models || 'N/A';
    }

    // Classification Report Table
    if (data.classification_report) {
        renderReportTable(data.classification_report);
    } else {
        document.getElementById('reportTable').innerHTML = '<p class="text-muted">No report table available for this phase.</p>';
        document.getElementById('f1Chart').innerHTML = ''; // Clear chart
    }

    // Confusion Matrix
    if (data.confusion_matrix) {
        document.getElementById('confusionMatrix').innerHTML =
            `<img src="data:image/png;base64,${data.confusion_matrix}" alt="Confusion Matrix">`;
    } else {
        document.getElementById('confusionMatrix').innerHTML =
            '<p style="color: var(--text-muted);">Confusion matrix image not available.</p>';
    }

    // Report Heatmap
    if (data.report_heatmap) {
        document.getElementById('reportHeatmap').innerHTML =
            `<img src="data:image/png;base64,${data.report_heatmap}" alt="Report Heatmap">`;
    } else {
        document.getElementById('reportHeatmap').innerHTML =
            '<p style="color: var(--text-muted);">Heatmap image not available.</p>';
    }

    // Training History
    if (data.training_history) {
        document.getElementById('trainingHistory').innerHTML =
            `<img src="data:image/png;base64,${data.training_history}" alt="Training History">`;
    } else {
        document.getElementById('trainingHistory').innerHTML =
            '<p style="color: var(--text-muted);">Training history graph not available.</p>';
    }
}

function renderReportTable(report) {
    const container = document.getElementById('reportTable');
    console.log("renderReportTable called with:", report);
    if (!report || report.length === 0) {
        container.innerHTML = '<p style="color: var(--text-muted);">No data available.</p>';
        return;
    }

    // Determine columns
    try {
        const keys = Object.keys(report[0]);

        let html = '<table class="report-table"><thead><tr>';
        keys.forEach(k => {
            html += `<th>${formatHeader(k)}</th>`;
        });
        html += '</tr></thead><tbody>';

        // F1 data for chart
        const f1Data = {};

        report.forEach(row => {
            html += '<tr>';
            keys.forEach(k => {
                let val = row[k];
                let cls = '';

                // Highlight near-perfect values
                if (typeof val === 'number') {
                    if (val >= 0.99 && val <= 1.0 && k !== 'support') {
                        cls = 'highlight';
                    }
                    val = k === 'support' ? val.toLocaleString() : val.toFixed(4);
                }
                html += `<td class="${cls}">${val !== null && val !== undefined ? val : ''}</td>`;
            });
            html += '</tr>';

            // Collect F1 scores for chart
            const clsName = row['Class'] || row['class'];
            const f1 = row['f1-score'];
            if (['Healthy', 'Bleached', 'Dead'].includes(clsName) && f1 != null) {
                f1Data[clsName] = f1;
            }
        });

        html += '</tbody></table>';
        container.innerHTML = html;

        // Render F1 chart
        try {
            renderF1Chart(f1Data);
        } catch (e) {
            console.error("Error rendering chart:", e);
        }
    } catch (e) {
        console.error("Error rendering report table:", e);
        container.innerHTML = `<div class="alert alert-danger">Error rendering table: ${e.message}</div>`;
    }
}

function formatHeader(key) {
    return key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
}

function renderF1Chart(f1Data) {
    const chart = document.getElementById('f1Chart');
    const classMap = { 'Healthy': 'healthy', 'Bleached': 'bleached', 'Dead': 'dead' };

    function getIndicator(pct) {
        if (pct >= 97) return { label: 'Excellent', cls: 'excellent', icon: 'fa-check-circle' };
        if (pct >= 90) return { label: 'Good', cls: 'good', icon: 'fa-arrow-up' };
        return { label: 'Needs Work', cls: 'poor', icon: 'fa-exclamation-triangle' };
    }

    // Scale bars relative to a baseline so small differences are visible
    const SCALE_MIN = 90; // 90% maps to 0% bar width, 100% maps to 100%
    let html = '';
    for (const [cls, val] of Object.entries(f1Data)) {
        const pct = (val * 100).toFixed(2);
        const pctNum = parseFloat(pct);
        // Normalize: map SCALE_MIN–100 → 0–100 for visual bar width
        const scaledWidth = Math.max(0, Math.min(100, ((pctNum - SCALE_MIN) / (100 - SCALE_MIN)) * 100)).toFixed(1);
        const ind = getIndicator(pctNum);
        html += `
            <div class="bar-chart-item">
                <span class="bar-chart-label">${cls}</span>
                <div class="bar-chart-track">
                    <div class="bar-chart-fill ${classMap[cls] || ''}" style="width: 0%;" data-width="${scaledWidth}%"></div>
                </div>
                <span class="bar-chart-value-outer">${pct}%</span>
                <span class="f1-indicator ${ind.cls}"><i class="fas ${ind.icon}"></i> ${ind.label}</span>
            </div>
        `;
    }
    chart.innerHTML = html;

    // Animate
    setTimeout(() => {
        chart.querySelectorAll('.bar-chart-fill').forEach(bar => {
            bar.style.width = bar.dataset.width;
        });
    }, 300);
}

// Metrics Tabs
function switchMetricTab(tabName) {
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));

    event.target.closest('.tab').classList.add('active');
    document.getElementById(`tab-${tabName}`).classList.add('active');
}

// ============================================================
// Server Health Check
// ============================================================
async function checkHealth() {
    const el = document.getElementById('serverStatus');
    try {
        const response = await fetch('/api/health');
        const data = await response.json();
        el.innerHTML = `
            <span class="status-dot online"></span>
            <span class="status-text">System Online</span>
        `;
    } catch {
        el.innerHTML = `
            <span class="status-dot offline"></span>
            <span class="status-text">System Offline</span>
        `;
    }
}

// ============================================================
// Init
// ============================================================
document.addEventListener('DOMContentLoaded', () => {
    checkHealth();
    // Periodic health check
    setInterval(checkHealth, 30000);

    // Click on upload zone
    document.getElementById('uploadZone').addEventListener('click', (e) => {
        if (e.target.closest('.btn') || e.target.closest('.preview-overlay')) return;
        if (!currentFile) {
            document.getElementById('fileInput').click();
        }
    });
});
