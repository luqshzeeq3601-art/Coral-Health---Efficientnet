html_content = """<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Coral Health AI Assessment</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
        
        body {
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
            background-color: #ffffff;
            color: #111827;
        }
        .mesh-bg {
            background: linear-gradient(120deg, #ffffff, #e0f7fa, #ffffff);
            background-size: 200% 200%;
            animation: meshGradient 15s ease infinite;
        }
        @keyframes meshGradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        .animate-pulse-slow {
            animation: pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite;
        }
    </style>
</head>
<body class="selection:bg-teal-100 selection:text-teal-900 min-h-screen bg-white font-sans text-gray-900">

    <!-- Header -->
    <header class="fixed top-0 left-0 right-0 z-50 bg-white/80 backdrop-blur-md border-b border-gray-100 transition-all duration-300 transform translate-y-0 opacity-100">
      <div class="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
        <div class="flex items-center gap-2">
          <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-teal-400 to-blue-500 flex items-center justify-center text-white shadow-lg shadow-teal-500/30">
            <i data-lucide="activity" class="w-[18px] h-[18px]"></i>
          </div>
          <span class="font-bold text-xl tracking-tight text-gray-900">Coral Health AI</span>
        </div>
        <nav class="hidden md:flex items-center gap-8 text-sm font-medium text-gray-600">
          <a href="#about" class="hover:text-teal-600 transition-colors">About</a>
          <a href="#features" class="hover:text-teal-600 transition-colors">Technology</a>
          <a href="#performance" class="hover:text-teal-600 transition-colors">Performance</a>
        </nav>
        <a href="#try-model" class="px-5 py-2.5 bg-gray-900 text-white text-sm font-medium rounded-full hover:bg-gray-800 transition-colors shadow-sm">
          Try Model
        </a>
      </div>
    </header>

    <!-- Hero Section -->
    <section class="relative pt-32 pb-20 lg:pt-48 lg:pb-32 overflow-hidden">
      <!-- Animated Mesh Gradient Background -->
      <div class="absolute inset-0 mesh-bg -z-10"></div>

      <div class="max-w-7xl mx-auto px-6 grid lg:grid-cols-2 gap-16 items-center">
        <div class="max-w-2xl transform transition-all duration-700 translate-x-0 opacity-100">
          <div class="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-teal-50 text-teal-700 text-sm font-medium mb-6 border border-teal-100/50">
            <i data-lucide="sparkles" class="w-3.5 h-3.5 text-teal-500"></i>
            <span>Introducing v2.0 Architecture</span>
          </div>

          <h1 class="text-5xl lg:text-7xl font-extrabold tracking-tight text-gray-900 leading-[1.1] mb-6 flex flex-wrap">
            <span>C</span><span>o</span><span>r</span><span>a</span><span>l</span><span>&nbsp;</span><span>H</span><span>e</span><span>a</span><span>l</span><span>t</span><span>h</span><span>&nbsp;</span>
            <span class="text-transparent bg-clip-text bg-gradient-to-r from-teal-500 to-blue-600">A</span>
            <span class="text-transparent bg-clip-text bg-gradient-to-r from-teal-500 to-blue-600">I</span>
            <span class="text-transparent bg-clip-text bg-gradient-to-r from-teal-500 to-blue-600">&nbsp;</span>
            <span class="text-transparent bg-clip-text bg-gradient-to-r from-teal-500 to-blue-600">A</span>
            <span class="text-transparent bg-clip-text bg-gradient-to-r from-teal-500 to-blue-600">s</span>
            <span class="text-transparent bg-clip-text bg-gradient-to-r from-teal-500 to-blue-600">s</span>
            <span class="text-transparent bg-clip-text bg-gradient-to-r from-teal-500 to-blue-600">e</span>
            <span class="text-transparent bg-clip-text bg-gradient-to-r from-teal-500 to-blue-600">s</span>
            <span class="text-transparent bg-clip-text bg-gradient-to-r from-teal-500 to-blue-600">s</span>
            <span class="text-transparent bg-clip-text bg-gradient-to-r from-teal-500 to-blue-600">m</span>
            <span class="text-transparent bg-clip-text bg-gradient-to-r from-teal-500 to-blue-600">e</span>
            <span class="text-transparent bg-clip-text bg-gradient-to-r from-teal-500 to-blue-600">n</span>
            <span class="text-transparent bg-clip-text bg-gradient-to-r from-teal-500 to-blue-600">t</span>
          </h1>

          <p class="text-lg text-gray-600 mb-8 leading-relaxed max-w-xl">
            98.11% Accuracy in Real-Time Reef Assessment. Empowering marine biologists with explainable, high-speed deep learning to monitor and protect coral ecosystems globally.
          </p>
          <div class="flex flex-col sm:flex-row items-center gap-4">
            <a href="#try-model" class="w-full sm:w-auto px-8 py-4 bg-gradient-to-r from-teal-500 to-blue-600 text-white rounded-full font-semibold shadow-lg shadow-blue-500/25 hover:shadow-xl hover:shadow-blue-500/40 transition-all flex items-center justify-center gap-2 group">
              Try Model
              <i data-lucide="arrow-right" class="w-[18px] h-[18px] group-hover:translate-x-1 transition-transform"></i>
            </a>
            <a href="#performance" class="w-full sm:w-auto px-8 py-4 bg-white/50 backdrop-blur-sm text-gray-700 rounded-full font-semibold border border-gray-200 hover:border-gray-300 hover:bg-white transition-all flex items-center justify-center">
              View Metrics
            </a>
          </div>
        </div>

        <div class="relative [perspective:1000px] transform transition-all duration-1000 delay-200 scale-100 opacity-100">
          <div class="relative rounded-3xl overflow-hidden shadow-2xl shadow-blue-900/10 border border-white/60 bg-white/20 backdrop-blur-xl aspect-[4/3] group transform-gpu transition-transform ease-in-out duration-500 hover:-translate-y-4 hover:shadow-[0_30px_60px_-15px_rgba(0,0,0,0.5)]">
            <div class="absolute inset-0 bg-gradient-to-tr from-teal-500/10 to-blue-500/10 z-10 pointer-events-none"></div>
            <img src="https://images.unsplash.com/photo-1641377784198-4a207ff00894?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHwzZCUyMGFic3RyYWN0JTIwY29yYWwlMjByZWVmJTIwYmx1ZXxlbnwxfHx8fDE3NzI4NjkyNDV8MA&ixlib=rb-4.1.0&q=80&w=1080" alt="3D abstract coral representation" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700 ease-out" />
            
            <div class="absolute top-1/4 left-1/4 w-3 h-3 bg-teal-400 rounded-full blur-[2px] animate-pulse z-20 shadow-[0_0_15px_rgba(45,212,191,0.8)]"></div>
            <div class="absolute top-2/3 right-1/4 w-4 h-4 bg-blue-400 rounded-full blur-[2px] animate-pulse z-20 shadow-[0_0_20px_rgba(96,165,250,0.8)]" style="animation-delay: 1s"></div>
            <div class="absolute bottom-1/4 left-1/3 w-2 h-2 bg-white rounded-full blur-[1px] animate-ping z-20" style="animation-duration: 3s"></div>
          </div>
        </div>
      </div>
    </section>

    <!-- About Section -->
    <section id="about" class="py-24 bg-white border-y border-gray-100">
      <div class="max-w-7xl mx-auto px-6">
        <div class="grid lg:grid-cols-2 gap-16 items-center">
          <div class="relative order-2 lg:order-1 flex justify-center transform transition-all duration-500 opacity-100">
            <div class="relative w-full rounded-2xl overflow-hidden shadow-2xl aspect-video group cursor-pointer bg-gray-900" style="clip-path: circle(150% at 50% 50%); transition: clip-path 1.5s ease-in-out;">
              <img src="https://images.unsplash.com/photo-1628371217613-714161455f6b?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHx1bmRlcndhdGVyJTIwY29yYWwlMjByZWVmJTIwc2N1YmF8ZW58MXx8fHwxNzcyODY5MjQ1fDA&ixlib=rb-4.1.0&q=80&w=1080" alt="Underwater coral reef video placeholder" class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105 opacity-80" />
              <div class="absolute inset-0 bg-gray-900/20 group-hover:bg-gray-900/10 transition-colors flex items-center justify-center backdrop-blur-[1px]">
                <div class="w-16 h-16 bg-white/90 backdrop-blur-sm rounded-full flex items-center justify-center shadow-lg group-hover:scale-110 transition-transform">
                  <i data-lucide="play" class="text-teal-600 ml-1 w-6 h-6" fill="currentColor"></i>
                </div>
              </div>
            </div>
            <div class="absolute -bottom-6 -right-6 w-32 h-32 bg-[radial-gradient(circle_at_center,_var(--tw-gradient-stops))] from-teal-500/20 to-transparent blur-2xl -z-10"></div>
          </div>
          <div class="order-1 lg:order-2 transform transition-all duration-800 translate-x-0 opacity-100 blur-none">
            <h2 class="text-sm font-semibold text-teal-600 tracking-wider uppercase mb-3">The Mission</h2>
            <h3 class="text-3xl md:text-4xl font-bold text-gray-900 mb-6 tracking-tight">Automating Reef Monitoring for Marine Biologists</h3>
            <p class="text-gray-600 mb-6 leading-relaxed text-lg">
              Manual assessment of coral health is slow, expensive, and subject to human error. Coral Health AI leverages state-of-the-art computer vision to instantly classify reef conditions.
            </p>
            <p class="text-gray-600 leading-relaxed text-lg">
              Powered by an <strong class="text-gray-900 font-semibold">EfficientNet-B0</strong> backbone, our model balances exceptional accuracy with lightweight inference, making it perfect for real-time edge deployment on autonomous underwater vehicles (AUVs) and diver-operated cameras.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section id="features" class="py-24 bg-slate-50 relative">
      <div class="max-w-7xl mx-auto px-6">
        <div class="text-center max-w-2xl mx-auto mb-16">
          <h2 class="text-sm font-semibold text-blue-600 tracking-wider uppercase mb-3">Technology</h2>
          <h3 class="text-3xl md:text-4xl font-bold text-gray-900 tracking-tight">Built for Precision and Speed</h3>
        </div>

        <div class="grid md:grid-cols-3 gap-8">
          <div class="relative group rounded-2xl p-8 bg-white border border-transparent shadow-sm transition-all duration-300 overflow-hidden transform hover:-translate-y-2 opacity-100 translate-y-0 delay-[0ms]">
            <div class="absolute inset-0 rounded-2xl border-2 border-transparent group-hover:border-teal-400/60 shadow-[0_0_0_0_transparent] group-hover:shadow-[0_0_30px_rgba(45,212,191,0.25)] transition-all duration-500 pointer-events-none"></div>
            <div class="relative z-10">
              <div class="w-14 h-14 rounded-xl bg-gray-50 flex items-center justify-center mb-6 transition-colors border border-gray-100 group-hover:border-transparent group-hover:bg-white group-hover:shadow-sm">
                <i data-lucide="network" class="text-teal-500 w-8 h-8 animate-[pulse_2.5s_infinite]"></i>
              </div>
              <h4 class="text-xl font-bold text-gray-900 mb-3">EfficientNet-B0 Backbone</h4>
              <p class="text-gray-600 leading-relaxed">
                Optimized compound scaling provides state-of-the-art accuracy while maintaining a small parameter footprint.
              </p>
            </div>
          </div>

          <div class="relative group rounded-2xl p-8 bg-white border border-transparent shadow-sm transition-all duration-300 overflow-hidden transform hover:-translate-y-2 opacity-100 translate-y-0 delay-[150ms]">
            <div class="absolute inset-0 rounded-2xl border-2 border-transparent group-hover:border-teal-400/60 shadow-[0_0_0_0_transparent] group-hover:shadow-[0_0_30px_rgba(45,212,191,0.25)] transition-all duration-500 pointer-events-none"></div>
            <div class="relative z-10">
              <div class="w-14 h-14 rounded-xl bg-gray-50 flex items-center justify-center mb-6 transition-colors border border-gray-100 group-hover:border-transparent group-hover:bg-white group-hover:shadow-sm">
                <i data-lucide="zap" class="text-blue-500 w-8 h-8 animate-[pulse_2.5s_infinite]"></i>
              </div>
              <h4 class="text-xl font-bold text-gray-900 mb-3">Real-time Classification</h4>
              <p class="text-gray-600 leading-relaxed">
                Sub-50ms inference latency allows for smooth, continuous analysis of live underwater video feeds.
              </p>
            </div>
          </div>

          <div class="relative group rounded-2xl p-8 bg-white border border-transparent shadow-sm transition-all duration-300 overflow-hidden transform hover:-translate-y-2 opacity-100 translate-y-0 delay-[300ms]">
            <div class="absolute inset-0 rounded-2xl border-2 border-transparent group-hover:border-teal-400/60 shadow-[0_0_0_0_transparent] group-hover:shadow-[0_0_30px_rgba(45,212,191,0.25)] transition-all duration-500 pointer-events-none"></div>
            <div class="relative z-10">
              <div class="w-14 h-14 rounded-xl bg-gray-50 flex items-center justify-center mb-6 transition-colors border border-gray-100 group-hover:border-transparent group-hover:bg-white group-hover:shadow-sm">
                <i data-lucide="eye" class="text-indigo-500 w-8 h-8 animate-[pulse_2.5s_infinite]"></i>
              </div>
              <h4 class="text-xl font-bold text-gray-900 mb-3">Explainable AI</h4>
              <p class="text-gray-600 leading-relaxed">
                Grad-CAM heatmaps highlight exactly which visual features the model used to make its health determination.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Performance Section -->
    <section id="performance" class="py-24 bg-slate-50 relative border-t border-gray-100">
      <div class="max-w-7xl mx-auto px-6">
        <!-- Dark Glass Container nested in light theme -->
        <div class="bg-gray-900/95 backdrop-blur-2xl rounded-[2.5rem] border border-gray-800 p-8 md:p-12 shadow-[0_30px_60px_-15px_rgba(0,0,0,0.5)] relative overflow-hidden">
          <!-- Subtle lighting inside glass -->
          <div class="absolute top-0 left-1/2 -translate-x-1/2 w-[800px] h-[400px] bg-blue-500/10 blur-[100px] rounded-full pointer-events-none"></div>
          
          <div class="text-center max-w-2xl mx-auto mb-16 relative z-10">
            <h2 class="text-sm font-semibold text-teal-400 tracking-wider uppercase mb-3">Model Evaluation</h2>
            <h3 class="text-3xl md:text-4xl font-bold text-white tracking-tight">Rigorous Benchmarking</h3>
            <p class="mt-4 text-gray-400">Our EfficientNet-B0 architecture demonstrates exceptional performance across all key metrics on the Global Coral Reef Dataset.</p>
          </div>

          <div class="grid lg:grid-cols-3 gap-8 mb-8 relative z-10">
            <!-- Metrics -->
            <div class="lg:col-span-1 space-y-4">
              <div class="bg-gray-800/50 rounded-2xl p-6 border border-gray-700/50 flex items-center justify-between backdrop-blur-sm shadow-inner transition-all transform translate-x-0 opacity-100 duration-500">
                <div>
                  <p class="text-sm font-medium text-gray-400 mb-1">Accuracy</p>
                  <p class="text-3xl font-bold text-white">98.11%</p>
                </div>
                <div class="text-sm font-semibold text-teal-400 bg-teal-400/10 px-2.5 py-1 rounded-md border border-teal-400/20">+1.2%</div>
              </div>

              <div class="bg-gray-800/50 rounded-2xl p-6 border border-gray-700/50 flex items-center justify-between backdrop-blur-sm shadow-inner transition-all transform translate-x-0 opacity-100 duration-500 delay-100">
                <div>
                  <p class="text-sm font-medium text-gray-400 mb-1">Precision</p>
                  <p class="text-3xl font-bold text-white">96.40%</p>
                </div>
                <div class="text-sm font-semibold text-teal-400 bg-teal-400/10 px-2.5 py-1 rounded-md border border-teal-400/20">+0.8%</div>
              </div>

              <div class="bg-gray-800/50 rounded-2xl p-6 border border-gray-700/50 flex items-center justify-between backdrop-blur-sm shadow-inner transition-all transform translate-x-0 opacity-100 duration-500 delay-200">
                <div>
                  <p class="text-sm font-medium text-gray-400 mb-1">Recall</p>
                  <p class="text-3xl font-bold text-white">96.40%</p>
                </div>
                <div class="text-sm font-semibold text-teal-400 bg-teal-400/10 px-2.5 py-1 rounded-md border border-teal-400/20">+1.5%</div>
              </div>
            </div>

            <!-- Chart -->
            <div class="lg:col-span-2 bg-gray-800/40 rounded-2xl p-6 border border-gray-700/50 backdrop-blur-sm transition-all duration-700 scale-100 opacity-100">
              <div class="mb-6 flex justify-between items-center">
                <div>
                  <h4 class="font-bold text-white">Training & Validation Loss</h4>
                  <p class="text-sm text-gray-400">Cross-entropy loss over 50 epochs</p>
                </div>
                <div class="flex gap-4 text-sm font-medium">
                  <div class="flex items-center gap-2 text-teal-400">
                    <span class="w-3 h-3 rounded-full bg-teal-400 shadow-[0_0_8px_rgba(45,212,191,0.6)]"></span>Train
                  </div>
                  <div class="flex items-center gap-2 text-blue-400">
                    <span class="w-3 h-3 rounded-full bg-blue-500 shadow-[0_0_8px_rgba(59,130,246,0.6)]"></span>Val
                  </div>
                </div>
              </div>

              <div class="h-64 w-full relative">
                <canvas id="lossChart"></canvas>
              </div>
            </div>
          </div>

          <!-- Confusion Matrix Dark UI -->
          <div class="bg-gray-800/40 rounded-2xl p-8 border border-gray-700/50 max-w-3xl mx-auto relative z-10 backdrop-blur-sm transition-all duration-600 delay-300 translate-y-0 opacity-100">
            <div class="mb-6">
              <h4 class="font-bold text-white">Confusion Matrix</h4>
              <p class="text-sm text-gray-400">True vs Predicted Classes</p>
            </div>

            <div class="grid grid-cols-4 gap-2 text-center text-sm font-medium">
              <div class="col-span-1"></div>
              <div class="text-gray-400">Pred: Healthy</div>
              <div class="text-gray-400">Pred: Bleached</div>
              <div class="text-gray-400">Pred: Dead</div>

              <div class="text-gray-400 text-right pr-4 self-center">True: Healthy</div>
              <div class="bg-teal-500/90 text-white rounded-lg py-3 shadow-inner">985</div>
              <div class="bg-gray-800 text-teal-400 rounded-lg py-3 border border-gray-700/50">12</div>
              <div class="bg-gray-800/50 text-teal-500 rounded-lg py-3 border border-gray-700/30">3</div>

              <div class="text-gray-400 text-right pr-4 self-center">True: Bleached</div>
              <div class="bg-gray-800 text-blue-400 rounded-lg py-3 border border-gray-700/50">8</div>
              <div class="bg-blue-500/90 text-white rounded-lg py-3 shadow-inner">482</div>
              <div class="bg-gray-800/50 text-blue-500 rounded-lg py-3 border border-gray-700/30">10</div>

              <div class="text-gray-400 text-right pr-4 self-center">True: Dead</div>
              <div class="bg-gray-800/50 text-gray-500 rounded-lg py-3 border border-gray-700/30">2</div>
              <div class="bg-gray-800 text-gray-400 rounded-lg py-3 border border-gray-700/50">14</div>
              <div class="bg-gray-600/90 text-white rounded-lg py-3 shadow-inner">284</div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Try Model Section -->
    <section id="try-model" class="py-32 relative bg-white overflow-hidden">
      <!-- Subtle Radial Gradient Background -->
      <div class="absolute inset-0 bg-[radial-gradient(circle_at_center,var(--tw-gradient-stops))] from-teal-50/60 via-white to-white -z-10"></div>
      
      <div class="max-w-4xl mx-auto px-6">
        <div class="text-center mb-12">
          <h2 class="text-3xl md:text-4xl font-bold text-gray-900 tracking-tight mb-4">Try the Model</h2>
          <p class="text-gray-600 text-lg">
            Upload a sample image of a coral colony to test our real-time classification engine.
          </p>
        </div>

        <div class="bg-white rounded-3xl shadow-xl shadow-blue-900/5 border border-gray-100 overflow-hidden transform transition-all duration-500 translate-y-0 opacity-100">
          <div class="p-8 md:p-12">
            
            <div id="drop-zone" class="border-2 border-dashed rounded-2xl p-12 text-center transition-all duration-300 group cursor-pointer border-teal-200 bg-white hover:bg-teal-50/30">
              <div id="upload-icon-container" class="w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-6 transition-transform duration-300 bg-teal-100 text-teal-600 group-hover:scale-110">
                <i data-lucide="upload-cloud" class="w-7 h-7"></i>
              </div>
              <h4 class="text-xl font-semibold text-gray-900 mb-2">Drag & drop an image</h4>
              <p class="text-gray-500 mb-6">or click to browse from your computer</p>
              
              <label class="px-6 py-2.5 bg-white text-teal-700 font-medium rounded-full shadow-sm border border-teal-100 hover:bg-teal-50 transition-colors cursor-pointer inline-block pointer-events-auto">
                Browse Files
                <input type="file" id="file-input" class="hidden" accept="image/*" />
              </label>
            </div>

            <div id="file-preview-area" class="space-y-8 hidden">
              <!-- Selected File -->
              <div class="flex items-center justify-between p-4 bg-gray-50 rounded-xl border border-gray-200">
                <div class="flex items-center gap-4">
                  <div class="w-12 h-12 bg-white rounded-lg border border-gray-200 flex items-center justify-center">
                    <i data-lucide="file-image" class="text-gray-500 w-6 h-6"></i>
                  </div>
                  <div>
                    <p id="file-name" class="font-medium text-gray-900 truncate max-w-[200px] sm:max-w-xs">image.jpg</p>
                    <p id="file-size" class="text-sm text-gray-500">120 KB</p>
                  </div>
                </div>
                <button id="remove-btn" class="text-gray-400 hover:text-gray-600 p-2">Remove</button>
              </div>

              <!-- Actions & Results -->
              <div id="action-area" class="text-center">
                <button id="run-btn" class="px-8 py-3.5 bg-gray-900 text-white rounded-full font-semibold shadow-md hover:bg-gray-800 transition-colors w-full sm:w-auto">
                  Run Assessment
                </button>
              </div>

              <div id="loading" class="relative overflow-hidden rounded-2xl bg-gray-50 border border-gray-100 p-12 text-center hidden">
                <div class="absolute inset-0 bg-gradient-to-r from-transparent via-white/80 to-transparent skew-x-[-20deg] animate-[shimmer_1.5s_infinite_linear]"></div>
                <div class="relative z-10">
                  <div class="inline-block w-8 h-8 border-4 border-teal-100 border-t-teal-500 rounded-full animate-spin mb-4"></div>
                  <p class="text-gray-600 font-medium">Analyzing neural pathways...</p>
                </div>
              </div>

              <div id="result-area" class="p-6 rounded-2xl border hidden transform transition-all duration-500 translate-y-0 opacity-100">
                <div class="flex items-center gap-4 mb-6">
                  <div id="result-icon-container" class="w-12 h-12 rounded-full flex items-center justify-center">
                    <i id="result-icon" data-lucide="check-circle" class="w-6 h-6"></i>
                  </div>
                  <div>
                    <p class="text-sm text-gray-500 font-medium uppercase tracking-wider">Prediction</p>
                    <h4 id="result-class" class="text-2xl font-bold capitalize">Result Coral</h4>
                  </div>
                </div>
                <div>
                  <div class="flex justify-between text-sm mb-2">
                    <span class="font-medium text-gray-700">Confidence Score</span>
                    <span id="result-confidence" class="font-bold text-gray-900">98.00%</span>
                  </div>
                  <div class="h-2.5 w-full bg-gray-200 rounded-full overflow-hidden">
                    <div id="result-bar" class="h-full rounded-full w-0 transition-all duration-800 ease-out"></div>
                  </div>
                </div>
              </div>

            </div>

          </div>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="bg-white border-t border-gray-100 py-12">
      <div class="max-w-7xl mx-auto px-6 flex flex-col md:flex-row items-center justify-between">
        <div class="flex items-center gap-2 mb-6 md:mb-0">
          <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-teal-400 to-blue-500 flex items-center justify-center text-white shadow-sm">
            <i data-lucide="activity" class="w-[18px] h-[18px]"></i>
          </div>
          <span class="font-bold text-xl tracking-tight text-gray-900">Coral Health AI</span>
        </div>
        <div class="text-gray-500 text-sm">
          &copy;  2026 Coral Health AI Initiative. Built for marine conservation.
        </div>
      </div>
    </footer>

    <style>
      @keyframes shimmer { 
        0% { transform: translateX(-150%) skewX(-20deg); }
        100% { transform: translateX(250%) skewX(-20deg); }
      }
    </style>

    <script>
      lucide.createIcons();

      // Chart setup
      document.addEventListener("DOMContentLoaded", function() {
        const ctx = document.getElementById('lossChart').getContext('2d');
        const data = [
          { epoch: 1, loss: 0.95, val_loss: 0.88 },
          { epoch: 5, loss: 0.65, val_loss: 0.60 },
          { epoch: 10, loss: 0.40, val_loss: 0.45 },
          { epoch: 15, loss: 0.25, val_loss: 0.30 },
          { epoch: 20, loss: 0.15, val_loss: 0.22 },
          { epoch: 25, loss: 0.10, val_loss: 0.18 },
          { epoch: 30, loss: 0.05, val_loss: 0.15 },
          { epoch: 40, loss: 0.02, val_loss: 0.10 },
          { epoch: 50, loss: 0.01, val_loss: 0.08 },
        ];

        let gradientLoss = ctx.createLinearGradient(0, 0, 0, 400);
        gradientLoss.addColorStop(0, 'rgba(45, 212, 191, 0.3)');
        gradientLoss.addColorStop(1, 'rgba(45, 212, 191, 0)');

        let gradientVal = ctx.createLinearGradient(0, 0, 0, 400);
        gradientVal.addColorStop(0, 'rgba(59, 130, 246, 0.3)');
        gradientVal.addColorStop(1, 'rgba(59, 130, 246, 0)');

        new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.map(d => d.epoch),
                datasets: [
                    {
                        label: 'Train Loss',
                        data: data.map(d => d.loss),
                        borderColor: '#2dd4bf',
                        backgroundColor: gradientLoss,
                        borderWidth: 3,
                        pointRadius: 0,
                        pointHoverRadius: 6,
                        fill: true,
                        tension: 0.4
                    },
                    {
                        label: 'Val Loss',
                        data: data.map(d => d.val_loss),
                        borderColor: '#3b82f6',
                        backgroundColor: gradientVal,
                        borderWidth: 3,
                        pointRadius: 0,
                        pointHoverRadius: 6,
                        fill: true,
                        tension: 0.4
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        mode: 'index',
                        intersect: false,
                        backgroundColor: '#1f2937',
                        titleColor: '#f3f4f6',
                        bodyColor: '#f3f4f6',
                        borderColor: '#374151',
                        borderWidth: 1,
                        padding: 10,
                        cornerRadius: 12
                    }
                },
                scales: {
                    x: {
                        grid: { display: false, drawBorder: false },
                        ticks: { color: '#9ca3af', font: { size: 12 } }
                    },
                    y: {
                        grid: { color: '#374151', borderDash: [3, 3], drawBorder: false },
                        ticks: { color: '#9ca3af', font: { size: 12 } },
                        beginAtZero: true
                    }
                },
                interaction: {
                    mode: 'nearest',
                    axis: 'x',
                    intersect: false
                }
            }
        });
      });

      // Try Model logic
      const fileInput = document.getElementById('file-input');
      const dropZone = document.getElementById('drop-zone');
      const uploadIconContainer = document.getElementById('upload-icon-container');
      
      const filePreviewArea = document.getElementById('file-preview-area');
      const fileNameStr = document.getElementById('file-name');
      const fileSizeStr = document.getElementById('file-size');
      const removeBtn = document.getElementById('remove-btn');
      
      const actionArea = document.getElementById('action-area');
      const runBtn = document.getElementById('run-btn');
      const loading = document.getElementById('loading');
      
      const resultArea = document.getElementById('result-area');
      const resultIconContainer = document.getElementById('result-icon-container');
      const resultIcon = document.getElementById('result-icon');
      const resultClass = document.getElementById('result-class');
      const resultConfidence = document.getElementById('result-confidence');
      const resultBar = document.getElementById('result-bar');

      let currentFile = null;

      fileInput.addEventListener('change', (e) => {
          if (e.target.files.length) {
              handleFile(e.target.files[0]);
          }
      });

      ['dragover', 'dragenter'].forEach(eventName => {
          dropZone.addEventListener(eventName, (e) => {
              e.preventDefault();
              dropZone.classList.remove('border-teal-200', 'bg-white', 'hover:bg-teal-50/30');
              dropZone.classList.add('border-teal-500', 'bg-teal-50', 'animate-pulse', 'scale-[1.02]');
              uploadIconContainer.classList.remove('bg-teal-100', 'text-teal-600', 'group-hover:scale-110');
              uploadIconContainer.classList.add('bg-teal-500', 'text-white', 'scale-110');
          });
      });

      ['dragleave', 'dragend', 'drop'].forEach(eventName => {
          dropZone.addEventListener(eventName, (e) => {
              e.preventDefault();
              dropZone.classList.remove('border-teal-500', 'bg-teal-50', 'animate-pulse', 'scale-[1.02]');
              dropZone.classList.add('border-teal-200', 'bg-white', 'hover:bg-teal-50/30');
              uploadIconContainer.classList.remove('bg-teal-500', 'text-white', 'scale-110');
              uploadIconContainer.classList.add('bg-teal-100', 'text-teal-600', 'group-hover:scale-110');
          });
      });

      dropZone.addEventListener('drop', (e) => {
          if (e.dataTransfer.files.length) {
              handleFile(e.dataTransfer.files[0]);
          }
      });

      function handleFile(file) {
          currentFile = file;
          dropZone.classList.add('hidden');
          filePreviewArea.classList.remove('hidden');
          
          fileNameStr.textContent = file.name;
          fileSizeStr.textContent = (file.size / 1024).toFixed(1) + ' KB';
          
          resetState();
      }

      removeBtn.addEventListener('click', () => {
          currentFile = null;
          fileInput.value = '';
          dropZone.classList.remove('hidden');
          filePreviewArea.classList.add('hidden');
      });

      function resetState() {
          actionArea.classList.remove('hidden');
          loading.classList.add('hidden');
          resultArea.classList.add('hidden');
          resultBar.style.width = '0%';
      }

      runBtn.addEventListener('click', async () => {
          if (!currentFile) return;
          
          actionArea.classList.add('hidden');
          loading.classList.remove('hidden');
          resultArea.classList.add('hidden');

          const formData = new FormData();
          formData.append("file", currentFile);

          try {
              const response = await fetch("/api/predict", {
                  method: "POST",
                  body: formData,
              });
              const data = await response.json();
              
              loading.classList.add('hidden');
              resultArea.classList.remove('hidden');
              
              if (data.class) {
                  const res = data.class.toLowerCase();
                  resultClass.textContent = data.class + ' Coral';
                  resultConfidence.textContent = (data.confidence * 100).toFixed(2) + '%';
                  
                  // Setup UI based on result
                  resultArea.className = 'p-6 rounded-2xl border transition-all duration-500 translate-y-0 opacity-100 ' + 
                      (res === 'healthy' ? 'bg-teal-50/50 border-teal-100' : 
                       res === 'bleached' ? 'bg-amber-50/50 border-amber-100' : 
                       'bg-rose-50/50 border-rose-100');
                       
                  resultIconContainer.className = 'w-12 h-12 rounded-full flex items-center justify-center ' +
                      (res === 'healthy' ? 'bg-teal-100 text-teal-600' : 
                       res === 'bleached' ? 'bg-amber-100 text-amber-600' : 
                       'bg-rose-100 text-rose-600');
                       
                  resultIcon.setAttribute('data-lucide', 
                      res === 'healthy' ? 'check-circle' : 
                      res === 'bleached' ? 'alert-triangle' : 
                      'x-circle');
                      
                  resultClass.className = 'text-2xl font-bold capitalize ' +
                      (res === 'healthy' ? 'text-teal-700' : 
                       res === 'bleached' ? 'text-amber-700' : 
                       'text-rose-700');
                       
                  resultBar.className = 'h-full rounded-full transition-all duration-800 ease-out ' +
                      (res === 'healthy' ? 'bg-teal-500' : 
                       res === 'bleached' ? 'bg-amber-500' : 
                       'bg-rose-500');
                  
                  lucide.createIcons();
                  
                  // Animate bar width
                  setTimeout(() => {
                      resultBar.style.width = (data.confidence * 100) + '%';
                  }, 100);
                  
              } else {
                  throw new Error("No class returned");
              }
          } catch (error) {
              loading.classList.add('hidden');
              resultArea.classList.remove('hidden');
              resultClass.textContent = 'Error';
              resultClass.className = 'text-2xl font-bold capitalize text-rose-700';
              resultConfidence.textContent = '0%';
              resultArea.className = 'p-6 rounded-2xl border transition-all duration-500 translate-y-0 opacity-100 bg-rose-50/50 border-rose-100';
              resultIconContainer.className = 'w-12 h-12 rounded-full flex items-center justify-center bg-rose-100 text-rose-600';
              resultIcon.setAttribute('data-lucide', 'x-circle');
              resultBar.className = 'h-full rounded-full transition-all duration-800 ease-out bg-rose-500';
              lucide.createIcons();
          }
      });
    </script>
</body>
</html>
"""

with open('templates/design9.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Generated precise templates/design9.html")
