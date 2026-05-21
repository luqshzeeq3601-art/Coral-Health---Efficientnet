import re

file_path = r'c:\Users\ZeeqRyz\Desktop\BASEPROJECT\04_Web_Application\templates\design9.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find the start and end of the Try Model section
start_marker = '<!-- Try Model Section -->'
end_marker = '</section>\n    </main>'

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx == -1 or end_idx == -1:
    print('Could not find the section.')
    exit(1)

new_html = '''<!-- Try Model Section -->
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,600;1,9..144,600&display=swap');
      .font-fraunces { font-family: 'Fraunces', serif; }
    </style>
    <section id="try-model" class="py-24 relative" style="background-color: #F4F7FF; background-image: radial-gradient(circle, rgba(21,88,214,.15) 1px, transparent 1px); background-size: 28px 28px; mask-image: radial-gradient(ellipse 80% 80% at 50% 50%, #000 40%, transparent 100%);" aria-labelledby="try-model-heading">
      
      <div class="max-w-6xl mx-auto px-6 relative z-10">
        <div class="text-center mb-16">
          <p class="text-sm font-bold text-[#1558D6] uppercase tracking-widest mb-3">Interactive Demo</p>
          <h2 id="try-model-heading" class="text-4xl md:text-5xl font-fraunces text-slate-900 tracking-tight mb-4">
            Try the <span class="italic text-[#1558D6]">Model</span>
          </h2>
          <p id="try-model-description" class="text-slate-600 text-lg max-w-2xl mx-auto">
            Upload a coral reef image to run our AI assessment and receive real-time predictions with confidence scores and explainable heatmaps.
          </p>
        </div>

        <!-- 2-Panel Layout -->
        <div class="flex flex-col lg:flex-row gap-8 items-start">
          
          <!-- CONFIG PANEL -->
          <div class="w-full lg:w-[340px] shrink-0 flex flex-col gap-6">
            
            <!-- Model Selection -->
            <div class="bg-white rounded-2xl shadow-sm border border-slate-200 p-5">
              <p class="text-[11px] font-bold text-slate-400 uppercase tracking-widest mb-4">1. Select Model</p>
              <div class="flex flex-col gap-3">
                <label id="label-ensemble" class="flex flex-col gap-1 p-3.5 rounded-xl border-2 border-[#1558D6] bg-[#EEF3FF] cursor-pointer transition-all">
                  <div class="flex items-center gap-2">
                    <input type="radio" name="model_type" value="ensemble" checked class="accent-[#1558D6]" onchange="onModelChange()">
                    <i data-lucide="layers" class="w-4 h-4 text-[#1558D6] shrink-0"></i>
                    <span class="text-sm font-semibold text-slate-800">Ensemble</span>
                  </div>
                  <span class="text-xs text-slate-500 pl-6">5-seed SWA · 98.11%</span>
                  <div class="flex gap-1 flex-wrap mt-1 pl-6">
                    <span class="text-[10px] bg-blue-100 text-[#1558D6] px-1.5 py-0.5 rounded font-medium">SWA</span>
                    <span class="text-[10px] bg-blue-100 text-[#1558D6] px-1.5 py-0.5 rounded font-medium">TTA</span>
                  </div>
                </label>
                <label id="label-base" class="flex flex-col gap-1 p-3.5 rounded-xl border-2 border-slate-100 bg-white cursor-pointer transition-all hover:border-slate-300">
                  <div class="flex items-center gap-2">
                    <input type="radio" name="model_type" value="base" class="accent-blue-600" onchange="onModelChange()">
                    <i data-lucide="cpu" class="w-4 h-4 text-slate-500 shrink-0"></i>
                    <span class="text-sm font-semibold text-slate-800">Base</span>
                  </div>
                  <span class="text-xs text-slate-500 pl-6">Single seed · faster</span>
                  <div class="flex gap-1 flex-wrap mt-1 pl-6">
                    <span class="text-[10px] bg-slate-100 text-slate-600 px-1.5 py-0.5 rounded font-medium">EfficientNetB0</span>
                  </div>
                </label>
              </div>
            </div>

            <!-- Explainability -->
            <div class="bg-white rounded-2xl shadow-sm border border-slate-200 p-5">
              <p class="text-[11px] font-bold text-slate-400 uppercase tracking-widest mb-4">2. Explainability</p>
              <div class="flex items-center justify-between p-3.5 rounded-xl border border-teal-200 bg-[#E6F7F2]">
                <div class="flex items-center gap-3">
                  <div class="w-8 h-8 rounded-full bg-white flex items-center justify-center shrink-0 text-[#0D7A5F] shadow-sm">
                    <i id="gradcam-icon-on" data-lucide="eye" class="w-4 h-4"></i>
                    <i id="gradcam-icon-off" data-lucide="eye-off" class="w-4 h-4 hidden text-slate-400"></i>
                  </div>
                  <div>
                    <p class="text-sm font-semibold text-slate-800">Grad-CAM</p>
                    <p class="text-[11px] text-[#0D7A5F] mt-0.5">Visualize focus</p>
                  </div>
                </div>
                <label class="relative inline-flex items-center cursor-pointer">
                  <input type="checkbox" id="gradcam-toggle" checked class="sr-only peer" onchange="onGradcamChange(this.checked)">
                  <div class="w-9 h-5 bg-slate-300 rounded-full peer transition-all duration-300 ease-in-out peer-checked:bg-[#0D7A5F] after:content-[''] after:absolute after:top-0.5 after:left-0.5 after:bg-white after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:after:translate-x-4 shadow-inner"></div>
                </label>
              </div>
              <div id="gradcam-disabled-msg-ui" class="hidden text-[11px] text-slate-400 mt-2">Grad-CAM is disabled.</div>
            </div>

            <!-- Stats Grid -->
            <div class="grid grid-cols-2 gap-4">
              <div class="bg-white rounded-2xl shadow-sm border border-slate-200 p-4 flex flex-col items-center justify-center text-center">
                <span class="text-[11px] font-bold text-slate-400 uppercase tracking-widest mb-1">Accuracy</span>
                <span class="font-fraunces text-2xl font-semibold text-slate-800">98.11%</span>
              </div>
              <div class="bg-white rounded-2xl shadow-sm border border-slate-200 p-4 flex flex-col items-center justify-center text-center">
                <span class="text-[11px] font-bold text-slate-400 uppercase tracking-widest mb-1">Macro F1</span>
                <span class="font-fraunces text-2xl font-semibold text-slate-800">0.98</span>
              </div>
            </div>

          </div>
          
          <!-- INTERACTIVE PANEL -->
          <div class="flex-1 w-full bg-white rounded-3xl shadow-lg shadow-blue-900/5 border border-slate-200 p-6 sm:p-10 min-h-[480px] flex flex-col justify-center relative overflow-hidden">
            
            <div id="upload-status" class="sr-only" role="status" aria-live="polite"></div>

            <!-- Upload State -->
            <div id="drop-zone" class="border-2 border-dashed rounded-2xl p-8 sm:p-12 text-center transition-all duration-300 group cursor-pointer border-slate-300 bg-[#F8FAFC] hover:border-[#1558D6] hover:bg-[#EEF3FF] h-full flex flex-col items-center justify-center" role="group">
              <div id="upload-icon-container" class="w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-6 transition-transform duration-300 bg-white shadow-sm text-[#1558D6] group-hover:-translate-y-1 group-hover:shadow-md">
                <i data-lucide="upload-cloud" class="w-7 h-7"></i>
              </div>
              <h4 class="text-xl font-semibold text-slate-900 mb-2">Drag & drop an image</h4>
              <p id="upload-help-text" class="text-slate-500 mb-8 text-sm">PNG, JPG up to 10MB</p>
              
              <label for="file-input" class="px-8 py-3 bg-[#1558D6] text-white font-medium rounded-full shadow-sm hover:bg-blue-700 transition-colors cursor-pointer inline-block pointer-events-auto shadow-blue-600/20">
                Browse Files
              </label>
              <input type="file" id="file-input" class="sr-only" accept="image/*" />
            </div>

            <!-- Preview State -->
            <div id="file-preview-area" class="hidden w-full h-full flex flex-col items-center justify-center">
              <div class="relative w-full max-w-md aspect-[4/3] rounded-2xl overflow-hidden shadow-md group border border-slate-200">
                <img id="upload-preview" src="" alt="Preview" class="w-full h-full object-cover">
                <div class="absolute inset-x-0 bottom-0 pt-16 pb-4 px-4 bg-gradient-to-t from-black/80 to-transparent flex items-end justify-between">
                  <div class="text-white">
                    <p id="file-name" class="font-medium text-sm truncate max-w-[200px]">image.png</p>
                    <p id="file-size" class="text-[11px] text-white/70 mt-0.5">120 KB</p>
                  </div>
                  <button id="remove-btn" type="button" class="w-8 h-8 rounded-full bg-white/20 hover:bg-red-500 backdrop-blur-sm flex items-center justify-center text-white transition-colors">
                    <i data-lucide="trash-2" class="w-4 h-4"></i>
                  </button>
                </div>
              </div>
              <div id="action-area" class="mt-8 text-center w-full max-w-md">
                <button id="run-btn" type="button" class="w-full py-4 bg-[#1558D6] text-white rounded-full font-semibold shadow-lg shadow-blue-600/30 hover:bg-blue-700 hover:shadow-blue-600/40 transition-all active:scale-[0.98] flex items-center justify-center gap-2">
                  <i data-lucide="scan" class="w-5 h-5"></i>
                  Analyze Image
                </button>
              </div>
            </div>

            <!-- Loading State -->
            <div id="loading" class="hidden flex-col items-center justify-center w-full h-full py-8">
              <div class="relative w-24 h-24 mb-10 flex items-center justify-center">
                <div class="absolute inset-0 rounded-full border-2 border-slate-100 animate-[spin_3s_linear_infinite]">
                  <div class="absolute top-0 left-1/2 -translate-x-1/2 -translate-y-1/2 w-3 h-3 bg-[#1558D6] rounded-full shadow-[0_0_10px_#1558D6]"></div>
                </div>
                <div class="w-16 h-16 bg-[#EEF3FF] rounded-full flex items-center justify-center animate-pulse border border-[#1558D6]/20">
                  <i data-lucide="cpu" class="w-7 h-7 text-[#1558D6]"></i>
                </div>
              </div>
              
              <!-- Retain Stepper IDs for JS Compatibility -->
              <div class="w-full max-w-sm space-y-4">
                <div class="flex items-center gap-3 text-sm font-medium text-[#1558D6]">
                   <i data-lucide="check-circle-2" class="w-5 h-5"></i>
                   <span>Preprocessing</span>
                   <div id="stepper-line" class="hidden"></div>
                   <div id="step-2-glow" class="hidden"></div>
                   <div id="step-3-glow" class="hidden"></div>
                   <div id="step-4-glow" class="hidden"></div>
                   <div id="step-3-bg" class="hidden"></div>
                   <div id="step-4-bg" class="hidden"></div>
                   <i id="step-3-icon" class="hidden"></i>
                   <i id="step-4-icon" class="hidden"></i>
                   <div id="arrow-1" class="hidden"></div>
                   <div id="arrow-2" class="hidden"></div>
                   <div id="arrow-3" class="hidden"></div>
                </div>
                <div class="flex items-center gap-3 text-sm font-medium text-slate-800 animate-pulse">
                   <i data-lucide="loader-2" class="w-5 h-5 animate-spin text-[#1558D6]"></i>
                   <span id="step-2-text">Running neural network inference...</span>
                </div>
                <div class="flex items-center gap-3 text-sm font-medium text-slate-400">
                   <i data-lucide="circle" class="w-5 h-5"></i>
                   <span id="step-3-text">Generating Grad-CAM visualization</span>
                </div>
                <div class="flex items-center gap-3 text-sm font-medium text-slate-400 hidden">
                   <span id="step-4-text">Finalizing</span>
                </div>
              </div>
            </div>

            <!-- Results State -->
            <div id="result-area" class="hidden flex-col gap-8 w-full animate-in fade-in zoom-in-95 duration-500">
              
              <!-- Verdict -->
              <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
                <div class="flex items-center gap-4">
                  <div id="result-icon-container" class="w-14 h-14 rounded-2xl flex items-center justify-center shrink-0 shadow-sm">
                    <i id="result-icon" data-lucide="alert-triangle" class="w-7 h-7 text-white"></i>
                  </div>
                  <div>
                    <p class="text-[11px] font-bold text-slate-400 uppercase tracking-widest mb-1">Prediction</p>
                    <h3 id="result-class" class="font-fraunces text-3xl font-bold text-slate-900 capitalize">Dead Coral</h3>
                    <p id="model-used-label" class="text-xs text-slate-400 mt-0.5"></p>
                  </div>
                </div>
                <div class="text-right">
                  <p class="text-[11px] font-bold text-slate-400 uppercase tracking-widest mb-1">Confidence</p>
                  <div id="badge-bg" class="inline-flex items-center justify-center px-4 py-1.5 rounded-full text-white font-bold text-lg">
                    <span id="result-badge-confidence">99.9%</span>
                  </div>
                  <div class="hidden">
                    <span id="main-result-confidence-text">99.9%</span>
                  </div>
                </div>
              </div>

              <!-- Uncertainty warning banner -->
              <div id="uncertainty-banner-card" class="hidden items-center gap-2 px-3 py-2 rounded-lg bg-amber-50 border border-amber-300 text-amber-800 text-xs font-medium mt-1">
                <i data-lucide="triangle-alert" class="w-4 h-4 shrink-0"></i>
                <span>Moderate confidence — manual review recommended.</span>
              </div>

              <div class="w-full h-[1px] bg-slate-100"></div>

              <!-- Probabilities -->
              <div>
                <p class="text-[11px] font-bold text-slate-400 uppercase tracking-widest mb-4">Class Probabilities</p>
                <div class="flex items-center gap-4 mb-5">
                  <div class="flex-1 h-3 bg-slate-100 rounded-full overflow-hidden relative">
                    <div id="main-result-bar" class="h-full rounded-full transition-all duration-1000 ease-out" style="width: 0%"></div>
                  </div>
                </div>
                <div id="result-probs" class="space-y-3">
                  <!-- Populated by JS -->
                </div>
              </div>
              
              <!-- Grad-CAM Skeleton -->
              <div id="gradcam-skeleton" class="hidden grid grid-cols-2 gap-4 mt-4">
                <div class="h-48 rounded-xl bg-slate-200 animate-pulse aspect-[4/3]"></div>
                <div class="h-48 rounded-xl bg-slate-200 animate-pulse aspect-[4/3]" style="animation-delay:0.1s"></div>
              </div>

              <!-- Grad-CAM -->
              <div id="demo-gradcam" class="hidden flex-col gap-4 pt-4 border-t border-slate-100">
                 <p class="text-[11px] font-bold text-slate-400 uppercase tracking-widest">Explainability (Grad-CAM)</p>
                 <div class="grid grid-cols-2 gap-4">
                    <div class="rounded-xl overflow-hidden border border-slate-200 shadow-sm relative aspect-[4/3]">
                       <img id="gc-original" src="" class="w-full h-full object-cover">
                       <span class="absolute top-2 left-2 px-2 py-1 bg-black/60 backdrop-blur-md text-white text-[10px] font-bold uppercase rounded-md">Original</span>
                    </div>
                    <div class="rounded-xl overflow-hidden border border-slate-200 shadow-sm relative aspect-[4/3]">
                       <img id="gc-heatmap" src="" class="w-full h-full object-cover">
                       <img id="gc-overlay" src="" class="hidden"> <!-- Hidden but retained for JS -->
                       <span class="absolute top-2 left-2 px-2 py-1 bg-black/60 backdrop-blur-md text-[#0D7A5F] text-[10px] font-bold uppercase rounded-md">Heatmap</span>
                    </div>
                 </div>
              </div>
              
              <div id="gradcam-disabled-msg" class="hidden text-center text-xs text-slate-400 py-2">Grad-CAM is disabled.</div>
              <div id="gradcam-placeholder" class="hidden text-center text-xs text-slate-400 py-2 border-2 border-dashed border-slate-200 rounded-xl mt-4">No Grad-CAM available.</div>
              <p id="gradcam-rerun-msg" class="hidden text-center text-xs text-[#0D7A5F] py-2 animate-pulse">Fetching Grad-CAM...</p>

              <div id="run-again-container" class="hidden pt-4 mt-2 border-t border-slate-100">
                <button id="btn-run-again" type="button" onclick="runAssessment()" class="w-full flex items-center justify-center gap-2 px-4 py-3 rounded-xl bg-slate-50 hover:bg-slate-100 text-slate-700 text-sm font-semibold transition-colors border border-slate-200">
                  <i id="run-again-icon" data-lucide="refresh-cw" class="w-4 h-4 text-slate-500"></i>
                  Analyze Another Image
                </button>
              </div>

            </div>

          </div>
        </div>
        
        <!-- Trust Bar -->
        <div class="mt-8 flex justify-center">
          <div class="inline-flex items-center gap-2.5 px-4 py-2 rounded-full bg-white/60 backdrop-blur-md border border-white/40 shadow-sm">
            <i data-lucide="lock" class="w-3.5 h-3.5 text-slate-400"></i>
            <span class="text-xs font-medium text-slate-500">Images are processed locally and never stored.</span>
          </div>
        </div>

      </div>
    </section>
'''

new_content = content[:start_idx] + new_html + content[end_idx:]

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_content)
    
print("Successfully replaced Try Model section!")
