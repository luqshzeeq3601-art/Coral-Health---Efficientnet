import re

file_path = r'c:\Users\ZeeqRyz\Desktop\BASEPROJECT\04_Web_Application\templates\design9.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Define boundaries
start_marker = '<!-- Try Model Section -->'
end_marker = '</section>\n    </main>'

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx == -1 or end_idx == -1:
    print('Could not find the section.')
    exit(1)

old_html = r'''<!-- Try Model Section -->
    <section id="try-model" class="py-24 bg-[#f0fdf9] border-t-2 border-teal-100 relative" aria-labelledby="try-model-heading">
      
      <div class="max-w-4xl mx-auto px-6">
        <div class="text-center mb-12">
          <h2 id="try-model-heading" class="text-3xl md:text-4xl font-bold text-gray-900 tracking-tight mb-4">Try the Model</h2>
          <p id="try-model-description" class="text-gray-600 text-lg">
            Upload a coral reef image to run our EfficientNet-B0 ensemble and receive Healthy, Bleached, or Dead predictions with confidence scores.
          </p>
        </div>

        <div class="bg-white rounded-3xl shadow-xl shadow-blue-900/5 border border-gray-100 overflow-hidden transform transition-all duration-500 translate-y-0 opacity-100">
          <div class="p-8 md:p-12">
            
            <div id="upload-status" class="sr-only" role="status" aria-live="polite"></div>

            <!-- ── FEAT-01: Model Selection ── -->
            <div class="mb-5">
              <p class="text-xs font-semibold text-slate-500 uppercase tracking-widest mb-3">Model</p>
              <div class="grid grid-cols-2 gap-3">
                <label id="label-ensemble"
                  class="flex flex-col gap-1 p-3 rounded-xl border-2 border-teal-500 bg-teal-50 cursor-pointer transition-all">
                  <div class="flex items-center gap-2">
                    <input type="radio" name="model_type" value="ensemble" checked
                           class="accent-teal-600" onchange="onModelChange()">
                    <i data-lucide="layers" class="w-4 h-4 text-teal-600 shrink-0"></i>
                    <span class="text-sm font-semibold text-slate-800">Ensemble</span>
                  </div>
                  <span class="text-xs text-slate-500">5-seed SWA · 98.11%</span>
                  <div class="flex gap-1 flex-wrap mt-1">
                    <span class="text-[10px] bg-teal-100 text-teal-800 px-1.5 py-0.5 rounded font-medium">SWA</span>
                    <span class="text-[10px] bg-teal-100 text-teal-800 px-1.5 py-0.5 rounded font-medium">TTA</span>
                  </div>
                </label>
                <label id="label-base"
                  class="flex flex-col gap-1 p-3 rounded-xl border-2 border-slate-200 bg-white cursor-pointer transition-all hover:border-slate-300">
                  <div class="flex items-center gap-2">
                    <input type="radio" name="model_type" value="base"
                           class="accent-blue-600" onchange="onModelChange()">
                    <i data-lucide="cpu" class="w-4 h-4 text-blue-500 shrink-0"></i>
                    <span class="text-sm font-semibold text-slate-800">Base</span>
                  </div>
                  <span class="text-xs text-slate-500">Single seed · faster</span>
                  <div class="flex gap-1 flex-wrap mt-1">
                    <span class="text-[10px] bg-blue-100 text-blue-800 px-1.5 py-0.5 rounded font-medium">EfficientNetB0</span>
                  </div>
                </label>
              </div>
            </div>
            <!-- ── end FEAT-01 ── -->

            <!-- ── FEAT-02: Grad-CAM Toggle ── -->
            <div class="mb-5">
              <p class="text-xs font-semibold text-slate-500 uppercase tracking-widest mb-3">Explainability</p>
              <div class="flex items-center justify-between p-3 rounded-xl border border-slate-200 bg-white">
                <div class="flex items-center gap-2">
                  <i id="gradcam-icon-on"  data-lucide="eye"     class="w-4 h-4 text-teal-600"></i>
                  <i id="gradcam-icon-off" data-lucide="eye-off" class="w-4 h-4 text-slate-400 hidden"></i>
                  <div>
                    <p class="text-sm font-semibold text-slate-800">Grad-CAM Heatmap</p>
                    <p class="text-xs text-slate-500 mt-0.5">Visualize attention regions</p>
                  </div>
                </div>
                <label class="relative inline-flex items-center cursor-pointer">
                  <input type="checkbox" id="gradcam-toggle" checked class="sr-only peer"
                         onchange="onGradcamChange(this.checked)">
                  <div class="w-10 h-5 bg-slate-200 rounded-full peer transition-all duration-300 ease-in-out
                              peer-checked:bg-teal-500
                              after:content-[''] after:absolute after:top-0.5 after:left-0.5
                              after:bg-white after:rounded-full after:h-4 after:w-4
                              after:transition-all peer-checked:after:translate-x-5"></div>
                </label>
              </div>
              <div id="gradcam-hint-on"
                class="mt-2 px-3 py-2 rounded-lg bg-amber-50 border border-amber-200 text-xs text-amber-700">
                <span class="font-medium">Grad-CAM Active</span> — adds ~2–4 ms latency. Highlights regions influencing the prediction.
              </div>
              <div id="gradcam-hint-off"
                class="mt-2 px-3 py-2 rounded-lg bg-slate-100 border border-slate-200 text-xs text-slate-500 hidden">
                Grad-CAM disabled. Only classification output will be shown.
              </div>
            </div>
            <!-- ── end FEAT-02 ── -->

            <div id="drop-zone" class="border-2 border-dashed rounded-2xl p-8 sm:p-12 text-center transition-all duration-300 group cursor-pointer border-teal-200 bg-white hover:bg-teal-50/30" role="group" aria-describedby="try-model-description upload-help-text">
              <div id="upload-icon-container" class="w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-6 transition-transform duration-300 bg-teal-100 text-teal-600 group-hover:scale-110">
                <i data-lucide="upload-cloud" class="w-7 h-7"></i>
              </div>
              <h4 class="text-xl font-semibold text-gray-900 mb-2">Drag & drop an image</h4>
              <p id="upload-help-text" class="text-gray-500 mb-6">or click to browse from your computer</p>
              
              <label for="file-input" class="px-6 py-2.5 bg-white text-teal-700 font-medium rounded-full shadow-sm border border-teal-100 hover:bg-teal-50 transition-colors cursor-pointer inline-block pointer-events-auto">
                Browse Files
              </label>
              <input type="file" id="file-input" class="sr-only" accept="image/*" aria-describedby="upload-help-text" />
            </div>

            <div id="file-preview-area" class="space-y-6 hidden w-full max-w-2xl mx-auto">
              <!-- Selected File Info -->
              <div class="flex items-center justify-between p-4 bg-white rounded-[24px] border border-gray-100 shadow-sm">
                <div class="flex items-center gap-5">
                  <div class="w-14 h-14 rounded-2xl bg-rose-50 flex items-center justify-center shrink-0">
                    <i data-lucide="image" class="w-6 h-6 text-rose-500"></i>
                  </div>
                  <div>
                    <p id="file-name" class="font-bold text-gray-900 text-lg leading-tight truncate max-w-[200px] sm:max-w-xs">150.png</p>
                    <p id="file-size" class="text-[13px] font-medium text-gray-400 mt-1">121.7 KB</p>
                  </div>
                </div>
                <button id="remove-btn" type="button" class="w-12 h-12 rounded-2xl bg-white border border-gray-100 hover:border-rose-200 hover:bg-rose-50 flex items-center justify-center text-rose-400 hover:text-rose-600 transition-colors shrink-0 group" aria-label="Remove selected image">
                  <i data-lucide="trash-2" class="w-5 h-5 group-hover:scale-110 transition-transform"></i>
                  <span class="sr-only">Remove</span>
                </button>
              </div>

              <!-- Image Preview -->
              <div class="rounded-[24px] border border-gray-100 bg-[#f8fafc] shadow-sm p-8 flex items-center justify-center min-h-[300px]">
                  <img id="upload-preview" src="" alt="Selected Image Preview" class="max-w-full max-h-[400px] rounded-[16px] object-contain shadow-sm">
              </div>

              <!-- Actions & Results -->
              <div id="action-area" class="text-center">
                <button id="run-btn" type="button" class="px-8 py-3.5 bg-gray-900 text-white rounded-full font-semibold shadow-md hover:bg-gray-800 transition-colors w-full sm:w-auto">
                  Run Assessment
                </button>
              </div>

              <div id="loading" class="hidden relative overflow-hidden rounded-[24px] bg-white border border-gray-100 p-8 sm:p-12 sm:py-16 text-center shadow-sm w-full max-w-3xl mx-auto" role="status" aria-live="polite" aria-label="Analyzing coral image">
                
                <!-- Visualization -->
                <div class="relative w-48 h-48 mx-auto mb-8 flex items-center justify-center" aria-hidden="true">
                  <!-- Outer rings -->
                  <div class="absolute inset-0 rounded-full border border-gray-100 animate-[spin_12s_linear_infinite]">
                     <div class="absolute top-4 right-8 w-2 h-2 bg-teal-500 rounded-full"></div>
                     <div class="absolute bottom-6 left-2 w-1.5 h-1.5 bg-gray-200 rounded-full"></div>
                  </div>
                  <div class="absolute inset-6 rounded-full border border-gray-100 animate-[spin_8s_linear_infinite_reverse]">
                     <div class="absolute bottom-2 left-6 w-1.5 h-1.5 bg-teal-200 rounded-full"></div>
                  </div>
                  
                  <!-- Central Icon -->
                  <div class="relative w-24 h-24 rounded-full flex items-center justify-center z-10" style="background: radial-gradient(circle, rgba(204,251,241,1) 0%, rgba(204,251,241,0.2) 100%); box-shadow: 0 0 40px rgba(45,212,191,0.2);">
                     <i data-lucide="brain" class="w-10 h-10 text-teal-500 animate-pulse"></i>
                  </div>
                  
                  <!-- Floating particles -->
                  <div class="absolute top-0 left-1/4 w-1 h-1 bg-teal-300 rounded-full"></div>
                  <div class="absolute top-1/4 -left-2 w-1.5 h-1.5 bg-teal-400 rounded-full opacity-50"></div>
                  <div class="absolute top-1/4 left-10 w-1.5 h-1.5 bg-blue-400 rounded-full"></div>
                  <div class="absolute bottom-1/4 -right-4 w-1 h-1 bg-teal-200 rounded-full"></div>
                  <div class="absolute top-6 right-0 w-1 h-1 bg-teal-300 rounded-full animate-ping"></div>
                </div>

                <!-- Text -->
                <h3 class="text-2xl font-bold text-gray-900 mb-2">Analyzing coral image</h3>
                <p class="text-gray-500 mb-12">This may take a few seconds. Please wait...</p>
                
                <!-- Stepper -->
                <div class="relative flex items-center justify-between max-w-lg mx-auto mb-16 mt-8">
                  <!-- Connecting lines (Base gray) -->
                  <div class="absolute top-6 left-0 w-full h-[2px] bg-gray-100 -z-10"></div>
                  <!-- Connecting lines (Active teal up to step 2) -->
                  <div id="stepper-line" class="absolute top-6 left-0 w-[33%] h-[2px] bg-teal-400 transition-all duration-[800ms] ease-in-out -z-10"></div>
                  
                  <!-- Static Gap Arrows -->
                  <div id="arrow-1" class="absolute top-6 left-[16.6%] -translate-y-1/2 -translate-x-1/2 z-10 text-teal-400 animate-bounce-right">
                     <i data-lucide="chevrons-right" class="w-5 h-5"></i>
                  </div>
                  <div id="arrow-2" class="absolute top-6 left-[50%] -translate-y-1/2 -translate-x-1/2 z-10 text-gray-300 transition-colors">
                     <i data-lucide="chevrons-right" class="w-5 h-5"></i>
                  </div>
                  <div id="arrow-3" class="absolute top-6 left-[83.3%] -translate-y-1/2 -translate-x-1/2 z-10 text-gray-300 transition-colors">
                     <i data-lucide="chevrons-right" class="w-5 h-5"></i>
                  </div>
                  
                  <!-- Step 1: Preprocessing -->
                  <div class="flex flex-col items-center gap-3">
                     <div class="w-12 h-12 rounded-full bg-white border-[2px] border-teal-400 flex items-center justify-center relative z-10">
                       <i data-lucide="image" class="w-5 h-5 text-teal-500"></i>
                     </div>
                     <span class="text-xs font-semibold text-gray-700">Preprocessing</span>
                  </div>
                  
                  <!-- Step 2: Analyzing -->
                  <div class="flex flex-col items-center gap-3 relative" id="step-2">
                     <!-- Active glow ring -->
                     <div id="step-2-glow" class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-[calc(50%+12px)] w-16 h-16 bg-teal-50 rounded-full border-[3px] border-teal-100/50 -z-0 transition-opacity"></div>
                     <div id="step-2-bg" class="w-12 h-12 rounded-full bg-white border border-transparent flex items-center justify-center relative z-10 transition-colors duration-300">
                       <i id="step-2-icon" data-lucide="brain" class="w-5 h-5 text-teal-500 transition-colors"></i>
                     </div>
                     <span id="step-2-text" class="text-xs font-bold text-teal-500 transition-colors">Analyzing</span>
                  </div>
                  
                  <!-- Step 3: Generating -->
                  <div class="flex flex-col items-center gap-3 relative" id="step-3">
                     <div id="step-3-glow" class="hidden absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-[calc(50%+12px)] w-16 h-16 bg-teal-50 rounded-full border-[3px] border-teal-100/50 -z-0 transition-opacity"></div>
                     <div id="step-3-bg" class="w-12 h-12 rounded-full bg-white border-[2px] border-gray-100 flex items-center justify-center relative z-10 transition-colors duration-300">
                       <i id="step-3-icon" data-lucide="bar-chart-2" class="w-5 h-5 text-gray-400 transition-colors"></i>
                     </div>
                     <span id="step-3-text" class="text-xs font-medium text-gray-400 transition-colors">Generating</span>
                  </div>
                  
                  <!-- Step 4: Finalizing -->
                  <div class="flex flex-col items-center gap-3 relative" id="step-4">
                     <div id="step-4-glow" class="hidden absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-[calc(50%+12px)] w-16 h-16 bg-teal-50 rounded-full border-[3px] border-teal-100/50 -z-0 transition-opacity"></div>
                     <div id="step-4-bg" class="w-12 h-12 rounded-full bg-white border-[2px] border-gray-100 flex items-center justify-center relative z-10 transition-colors duration-300">
                       <i id="step-4-icon" data-lucide="check" class="w-5 h-5 text-gray-400 transition-colors"></i>
                     </div>
                     <span id="step-4-text" class="text-xs font-medium text-gray-400 transition-colors">Finalizing</span>
                  </div>
                </div>
                
                <!-- Footer Badge -->
                <div class="inline-flex items-center gap-2.5 px-5 py-3 rounded-[12px] bg-teal-50/50 border border-teal-100/30">
                   <div class="w-5 h-5 rounded-full bg-teal-500 flex items-center justify-center shrink-0 shadow-sm">
                     <i data-lucide="shield-check" class="w-3 h-3 text-white"></i>
                   </div>
                   <span class="text-[13px] font-semibold text-gray-700 tracking-wide">Your data is secure and private</span>
                </div>
              </div>

                 <div id="result-area" class="hidden transform transition-all duration-500 translate-y-0 opacity-100 flex-col gap-10 w-full max-w-4xl mx-auto" role="region" aria-live="polite" aria-labelledby="result-class" tabindex="-1">
                
                <!-- Main Prediction Card -->
                <div class="rounded-[24px] border border-gray-100 bg-white shadow-sm overflow-hidden">
                  
                  <!-- Top Section: Prediction and Badge -->
                  <div class="p-8 pb-6 flex flex-col sm:flex-row sm:items-start justify-between border-b border-gray-100 gap-6">
                    <div class="flex items-center gap-6">
                      <div id="result-icon-container" class="w-16 h-16 rounded-full flex items-center justify-center shrink-0 bg-rose-100 text-rose-500">
                        <i id="result-icon" data-lucide="droplet" class="w-8 h-8"></i>
                      </div>
                      <div>
                        <p class="text-[11px] font-bold text-gray-400 uppercase tracking-widest mb-1.5">Prediction</p>
                         <h3 id="result-class" class="text-3xl sm:text-4xl font-extrabold text-gray-900 capitalize tracking-tight">Dead Coral</h3>
                         <p id="model-used-label" class="text-xs text-slate-400 mt-0.5"></p>
                      </div>
                    </div>
                    
                    <div class="flex flex-col sm:items-end gap-2">
                      <div id="badge-bg" class="px-6 py-2 rounded-full text-white font-bold text-xl shadow-sm bg-rose-500 w-fit">
                        <span id="result-badge-confidence">99.9%</span>
                      </div>
                      <div class="flex items-center gap-1.5 text-[11px] font-semibold text-gray-400 mr-2">
                        <span>Confidence Score</span>
                        <i data-lucide="info" class="w-3.5 h-3.5"></i>
                      </div>
                    </div>
                  </div>

                  <!-- Bottom Section: Bars and Probabilities -->
                  <div class="grid grid-cols-1 md:grid-cols-2 divide-y md:divide-y-0 md:divide-x divide-gray-100">
                    
                    <!-- Left: Main Confidence Bar -->
                    <div class="p-8 sm:pr-12">
                      <p class="text-[11px] font-bold text-gray-400 uppercase tracking-widest mb-8">Confidence Score</p>
                      
                      <div class="flex items-center gap-4 mb-4">
                        <div class="flex-1 h-3.5 bg-gray-100 rounded-full relative">
                          <div id="main-result-bar" class="h-full rounded-full transition-all duration-1000 ease-out bg-rose-500 relative" style="width: 0%"></div>
                        </div>
                        <span id="main-result-confidence-text" class="font-extrabold text-gray-900 text-lg tabular-nums">99.9%</span>
                      </div>
                      
                      <div class="flex justify-between text-[11px] font-bold text-gray-400 px-1">
                        <span>0%</span>
                        <span class="ml-4">50%</span>
                        <span>100%</span>
                      </div>
                    </div>
                    
                    <!-- Right: Class Probabilities -->
                    <div class="p-8 sm:pl-12">
                      <p class="text-[11px] font-bold text-gray-400 uppercase tracking-widest mb-6">Class Probabilities</p>
                      <div id="result-probs" class="space-y-4">
                        <!-- Populated by JS -->
                      </div>
                    </div>

                  </div>
                </div>

                <!-- Uncertainty warning banner -->
                <div id="uncertainty-banner-card"
                  class="hidden items-center gap-2 px-3 py-2 rounded-lg
                         bg-amber-50 border border-amber-300 text-amber-800 text-xs font-medium mt-1">
                  <i data-lucide="triangle-alert" class="w-4 h-4 shrink-0"></i>
                  <span>Moderate confidence — manual review recommended.</span>
                </div>

                <!-- Grad-CAM Skeleton Loader (shown while fetching) -->
                <div id="gradcam-skeleton" class="hidden grid grid-cols-1 sm:grid-cols-3 gap-6 mt-4">
                  <div class="h-36 rounded-[20px] bg-slate-200 animate-pulse"></div>
                  <div class="h-36 rounded-[20px] bg-slate-200 animate-pulse" style="animation-delay:0.1s"></div>
                  <div class="h-36 rounded-[20px] bg-slate-200 animate-pulse" style="animation-delay:0.2s"></div>
                </div>

                <!-- Grad-CAM Analysis Section -->
                <div id="demo-gradcam" class="hidden flex-col gap-6">
                    <div class="flex items-start gap-4 mb-2">
                        <div class="w-10 h-10 rounded-full bg-teal-50 flex items-center justify-center shrink-0">
                            <i data-lucide="eye" class="w-5 h-5 text-teal-600"></i>
                        </div>
                        <div>
                            <h3 class="text-xl font-bold text-gray-900">Grad-CAM Explainability</h3>
                            <p class="text-sm text-gray-500 mt-1 mb-3">Visualizing model focus and decision areas</p>
                            <ul class="list-none text-[13px] text-gray-600 space-y-1.5">
                                <li class="flex items-center gap-2"><span class="w-2 h-2 rounded-full bg-rose-500"></span> <strong>Red/Yellow areas:</strong> High importance regions strongly influencing the prediction.</li>
                                <li class="flex items-center gap-2"><span class="w-2 h-2 rounded-full bg-blue-500"></span> <strong>Blue/Dark areas:</strong> Low importance regions not significantly affecting the decision.</li>
                            </ul>
                            <!-- Gradient legend -->
                            <div class="flex items-center gap-4 mt-3 text-xs text-slate-500">
                              <div class="flex items-center gap-1.5">
                                <span class="w-16 h-2 rounded-full"
                                  style="background: linear-gradient(to right, #00f, #0ff, #0f0, #ff0, #f00)"></span>
                                <span>Low → High importance</span>
                              </div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="grid grid-cols-1 sm:grid-cols-3 gap-6">
                        <!-- Original Image -->
                        <div class="rounded-[20px] overflow-hidden border border-gray-100 bg-white shadow-sm flex flex-col hover:shadow-md transition-shadow">
                            <div class="relative aspect-square w-full">
                                <img id="gc-original" src="" alt="Original Image" class="w-full h-full object-cover">
                            </div>
                            <div class="p-5 bg-white flex items-center gap-3">
                                <i data-lucide="image" class="w-5 h-5 text-gray-400"></i>
                                <p class="text-sm font-semibold text-gray-600">Original Image</p>
                            </div>
                        </div>
                        <!-- Overlay -->
                        <div class="rounded-[20px] overflow-hidden border border-gray-100 bg-white shadow-sm flex flex-col hover:shadow-md transition-shadow">
                            <div class="relative aspect-square w-full">
                                <img id="gc-overlay" src="" alt="Grad-CAM" class="w-full h-full object-cover">
                            </div>
                            <div class="p-5 bg-white flex items-center gap-3">
                                <i data-lucide="layers" class="w-5 h-5 text-gray-400"></i>
                                <p class="text-sm font-semibold text-gray-600">Grad-CAM</p>
                            </div>
                        </div>
                        <!-- Heatmap -->
                        <div class="rounded-[20px] overflow-hidden border border-gray-100 bg-white shadow-sm flex flex-col hover:shadow-md transition-shadow">
                            <div class="relative aspect-square w-full">
                                <img id="gc-heatmap" src="" alt="Attention Heatmap" class="w-full h-full object-cover">
                            </div>
                            <div class="p-5 bg-white flex items-center gap-3">
                                <i data-lucide="grid" class="w-5 h-5 text-gray-400"></i>
                                <p class="text-sm font-semibold text-gray-600">Attention Heatmap</p>
                            </div>
                        </div>
                    </div>
                </div>
                <p id="gradcam-disabled-msg"
                   class="hidden text-center text-sm text-slate-400 py-4">
                  Grad-CAM is disabled. Enable it above to visualize attention regions.
                </p>
                <div id="gradcam-placeholder"
                  class="hidden mt-4 p-4 rounded-xl border-2 border-dashed border-slate-200 text-center text-sm text-slate-400">
                  <i data-lucide="eye" class="inline w-4 h-4 mr-1"></i>
                  Grad-CAM will appear here after running the assessment.
                </div>
                <p id="gradcam-rerun-msg"
                  class="hidden text-center text-sm text-teal-600 py-2 animate-pulse">
                  <i data-lucide="loader" class="inline w-3 h-3 mr-1"></i>
                  Fetching Grad-CAM — re-running assessment...
                </p>
                <!-- ── FEAT-03: Run Again button ── -->
                <div id="run-again-container" class="hidden mt-4 pt-4 border-t border-slate-100">
                  <button id="btn-run-again" type="button" onclick="runAssessment()"
                    class="w-full flex items-center justify-center gap-2 px-4 py-3
                           rounded-xl bg-teal-600 hover:bg-teal-700 active:bg-teal-800
                           text-white text-sm font-semibold transition-all duration-200 shadow-sm">
                    <i id="run-again-icon" data-lucide="refresh-cw" class="w-4 h-4 transition-transform duration-500"></i>
                    Run Again
                  </button>
                  <p class="text-center text-xs text-slate-400 mt-2">
                    Reruns with current model &amp; Grad-CAM settings — no need to re-upload.
                  </p>
                </div>
              </div>

            </div>

          </div>
        </div>
      </div>
    </section>'''

new_content = content[:start_idx] + old_html + content[end_idx:]

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_content)
    
print("Successfully reverted Try Model section!")
