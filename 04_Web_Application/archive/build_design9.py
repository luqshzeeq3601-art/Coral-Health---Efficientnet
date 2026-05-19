html_content = """<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Coral Health AI Assessment</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        body {
            font-family: system-ui, -apple-system, sans-serif;
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
        .dark-glass {
            background: rgba(17, 24, 39, 0.95);
            backdrop-filter: blur(24px);
            border: 1px solid rgba(31, 41, 55, 1);
            box-shadow: 0 30px 60px -15px rgba(0,0,0,0.5);
        }
    </style>
</head>
<body class="selection:bg-teal-100 selection:text-teal-900">

    <!-- Navbar -->
    <header class="fixed top-0 left-0 right-0 z-50 bg-white/80 backdrop-blur-md border-b border-gray-100 shadow-sm">
        <div class="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
            <div class="flex items-center gap-2">
                <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-teal-400 to-blue-500 flex items-center justify-center text-white font-bold shadow-lg shadow-teal-500/20">
                    C
                </div>
                <span class="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-gray-900 to-gray-600">Coral AI</span>
            </div>
            <nav class="hidden md:flex gap-8">
                <a href="#performance" class="text-sm font-medium text-gray-600 hover:text-teal-600 transition-colors">Performance</a>
                <a href="#try-model" class="text-sm font-medium text-gray-600 hover:text-teal-600 transition-colors">Try Model</a>
            </nav>
        </div>
    </header>

    <!-- Hero Section -->
    <section class="relative pt-32 pb-20 mt-10 lg:pt-48 lg:pb-32 overflow-hidden mesh-bg">
        <div class="max-w-7xl mx-auto px-6 grid lg:grid-cols-2 gap-16 items-center">
            <div class="max-w-2xl">
                <div class="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-teal-50 text-teal-700 text-sm font-medium mb-6 border border-teal-100">
                    <i data-lucide="sparkles" class="w-4 h-4 text-teal-500"></i>
                    <span>Introducing v4.0 Robust Architecture</span>
                </div>
                <h1 class="text-5xl lg:text-7xl font-extrabold tracking-tight text-gray-900 leading-[1.1] mb-6">
                    Coral Health AI<br>
                    <span class="text-transparent bg-clip-text bg-gradient-to-r from-teal-500 to-blue-600">Assessment</span>
                </h1>
                <p class="text-lg text-gray-600 mb-8 leading-relaxed max-w-xl">
                    98.11% Accuracy in Real-Time Reef Assessment. Empowering marine biologists with explainable, high-speed deep learning to monitor and protect coral ecosystems globally.
                </p>
                <div class="flex flex-col sm:flex-row items-center gap-4">
                    <a href="#try-model" class="w-full sm:w-auto px-8 py-4 bg-gradient-to-r from-teal-500 to-blue-600 text-white rounded-full font-semibold shadow-lg shadow-blue-500/25 hover:shadow-xl transition-all flex items-center justify-center gap-2 group">
                        Try Model <i data-lucide="arrow-right" class="w-4 h-4 group-hover:translate-x-1 transition-transform"></i>
                    </a>
                    <a href="#performance" class="w-full sm:w-auto px-8 py-4 bg-white/50 backdrop-blur-sm text-gray-700 rounded-full font-semibold border border-gray-200 hover:bg-white transition-all flex items-center justify-center">
                        View Metrics
                    </a>
                </div>
            </div>
            <div class="relative">
                <div class="relative rounded-3xl overflow-hidden shadow-2xl border border-white/60 bg-white/20 backdrop-blur-xl aspect-[4/3]">
                    <img src="https://images.unsplash.com/photo-1641377784198-4a207ff00894?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHwzZCUyMGFic3RyYWN0JTIwY29yYWwlMjByZWVmJTIwYmx1ZXxlbnwxfHx8fDE3NzI4NjkyNDV8MA&ixlib=rb-4.1.0&q=80&w=1080" class="w-full h-full object-cover">
                </div>
            </div>
        </div>
    </section>

    <!-- Performance Section -->
    <section id="performance" class="py-24 bg-slate-50 relative border-t border-gray-100">
        <div class="max-w-7xl mx-auto px-6">
            <div class="text-center mb-16">
                <h2 class="text-4xl font-bold text-gray-900 mb-4">Model Performance Summary</h2>
                <p class="text-lg text-gray-500 max-w-2xl mx-auto">V4-Robust Ensemble with Multiscale TTA & Temperature Scaling</p>
            </div>
            <div class="dark-glass rounded-[2.5rem] p-8 md:p-12 relative overflow-hidden">
                <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
                    <div class="bg-white/5 rounded-2xl p-6 border border-white/10">
                        <div class="flex items-center justify-between mb-4">
                            <p class="text-sm font-medium text-gray-400">Accuracy</p>
                        </div>
                        <p class="text-4xl font-bold text-white mb-2">98.11%</p>
                        <p class="text-sm text-teal-400 mt-2">+0.5% compared to V3</p>
                    </div>
                    <div class="bg-white/5 rounded-2xl p-6 border border-white/10">
                        <div class="flex items-center justify-between mb-4">
                            <p class="text-sm font-medium text-gray-400">Precision</p>
                        </div>
                        <p class="text-4xl font-bold text-white mb-2">96.40%</p>
                        <p class="text-sm text-teal-400 mt-2">Macro avg</p>
                    </div>
                    <div class="bg-white/5 rounded-2xl p-6 border border-white/10">
                        <div class="flex items-center justify-between mb-4">
                            <p class="text-sm font-medium text-gray-400">Recall</p>
                        </div>
                        <p class="text-4xl font-bold text-white mb-2">96.40%</p>
                        <p class="text-sm text-teal-400 mt-2">Macro avg</p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Try Model Section -->
    <section id="try-model" class="py-32 relative bg-white overflow-hidden">
        <div class="max-w-4xl mx-auto px-6 text-center">
            <h2 class="text-4xl md:text-5xl font-bold text-gray-900 mb-6">Test the AI Model</h2>
            <p class="text-lg text-gray-600 mb-12">Upload an underwater coral image and see real-time classification results.</p>
            
            <div class="p-8 border-2 border-dashed border-gray-300 rounded-[2rem] bg-gray-50/50 hover:bg-gray-50 hover:border-teal-400 transition-colors" id="drop-zone">
                <div class="flex flex-col items-center">
                    <i data-lucide="upload-cloud" class="w-12 h-12 text-teal-500 mb-4"></i>
                    <p class="text-gray-700 font-medium mb-2">Drag and drop your image here</p>
                    <p class="text-sm text-gray-500 mb-6">Supports JPG, PNG (Max 10MB)</p>
                    <input type="file" id="file-input" class="hidden" accept="image/*">
                    <button id="upload-btn" class="px-6 py-2.5 bg-gray-900 text-white rounded-full font-medium hover:bg-gray-800 transition-colors">
                        Browse Files
                    </button>
                    <p id="file-name" class="mt-4 text-sm text-blue-600 font-medium hidden"></p>
                </div>
            </div>

            <div id="action-area" class="mt-8 hidden">
                <button id="run-btn" class="px-8 py-3.5 bg-gradient-to-r from-teal-500 to-blue-600 text-white rounded-full font-semibold shadow-md hover:shadow-lg transition-all">
                    Run Assessment
                </button>
            </div>

            <div id="loading" class="mt-12 hidden">
                <div class="inline-block w-8 h-8 border-4 border-teal-100 border-t-teal-500 rounded-full animate-spin mb-4"></div>
                <p class="text-gray-600 font-medium">Analyzing neural pathways...</p>
            </div>

            <div id="result-area" class="mt-12 hidden">
                <div class="p-6 bg-teal-50 border border-teal-100 rounded-2xl inline-block min-w-[300px]">
                    <h3 class="text-2xl font-bold text-gray-900 mb-2">Result: <span id="result-class" class="text-teal-600 capitalize">Healthy</span></h3>
                    <p class="text-gray-600">Confidence: <span id="result-confidence" class="font-bold text-gray-900">98%</span></p>
                </div>
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer class="bg-gray-50 border-t border-gray-200 py-12">
        <div class="max-w-7xl mx-auto px-6 text-center text-gray-500 text-sm">
            <p>&copy; 2026 Coral Health AI. Built for marine conservation.</p>
        </div>
    </footer>

    <script>
        lucide.createIcons();

        const fileInput = document.getElementById('file-input');
        const uploadBtn = document.getElementById('upload-btn');
        const dropZone = document.getElementById('drop-zone');
        const fileName = document.getElementById('file-name');
        const actionArea = document.getElementById('action-area');
        const runBtn = document.getElementById('run-btn');
        const loading = document.getElementById('loading');
        const resultArea = document.getElementById('result-area');
        const resultClass = document.getElementById('result-class');
        const resultConfidence = document.getElementById('result-confidence');

        let currentFile = null;

        uploadBtn.addEventListener('click', () => fileInput.click());

        fileInput.addEventListener('change', (e) => {
            if (e.target.files.length) {
                handleFile(e.target.files[0]);
            }
        });

        dropZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            dropZone.classList.add('border-teal-400', 'bg-teal-50/50');
        });

        dropZone.addEventListener('dragleave', () => {
            dropZone.classList.remove('border-teal-400', 'bg-teal-50/50');
        });

        dropZone.addEventListener('drop', (e) => {
            e.preventDefault();
            dropZone.classList.remove('border-teal-400', 'bg-teal-50/50');
            if (e.dataTransfer.files.length) {
                handleFile(e.dataTransfer.files[0]);
            }
        });

        function handleFile(file) {
            currentFile = file;
            fileName.textContent = file.name;
            fileName.classList.remove('hidden');
            actionArea.classList.remove('hidden');
            resultArea.classList.add('hidden');
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
                    resultClass.textContent = data.class;
                    resultConfidence.textContent = (data.confidence * 100).toFixed(2) + '%';
                    
                    // Update color based on result
                    if (data.class.toLowerCase() === 'healthy') {
                        resultClass.className = 'text-teal-600 capitalize';
                    } else if (data.class.toLowerCase() === 'bleached') {
                        resultClass.className = 'text-amber-500 capitalize';
                    } else {
                        resultClass.className = 'text-rose-500 capitalize';
                    }
                } else {
                    resultClass.textContent = 'Error';
                    resultClass.className = 'text-rose-500 capitalize';
                    resultConfidence.textContent = 'N/A';
                }
            } catch (error) {
                loading.classList.add('hidden');
                resultArea.classList.remove('hidden');
                resultClass.textContent = 'Error';
                resultClass.className = 'text-rose-500 capitalize';
                resultConfidence.textContent = 'N/A';
            }
        });
    </script>
</body>
</html>
"""

with open('templates/design9.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Generated templates/design9.html")
