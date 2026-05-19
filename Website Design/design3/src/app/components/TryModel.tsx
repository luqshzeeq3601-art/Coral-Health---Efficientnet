import React, { useState } from "react";
import { motion } from "motion/react";
import { UploadCloud, FileImage, CheckCircle, AlertTriangle, XCircle, Leaf } from "lucide-react";

export function TryModel() {
  const [file, setFile] = useState<File | null>(null);
  const [status, setStatus] = useState<"idle" | "analyzing" | "result">("idle");
  const [result, setResult] = useState<"healthy" | "bleached" | "dead" | null>(null);
  const [confidence, setConfidence] = useState(0);
  const [probabilities, setProbabilities] = useState<Record<string, number>>({});
  const [isDragOver, setIsDragOver] = useState(false);

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(true);
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setFile(e.dataTransfer.files[0]);
      setStatus("idle");
    }
  };

const handleRun = async () => {
    if (!file) return;
    setStatus("analyzing");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("/api/predict", {
        method: "POST",
        body: formData,
      });
      const data = await response.json();
      
      setStatus("result");
      if (data.prediction || data.class) {
        const cls = (data.prediction || data.class).toLowerCase();
        setResult(cls);
        setConfidence(data.confidence ?? 0);
        if (data.probabilities && typeof data.probabilities === "object") {
          const norm: Record<string, number> = {};
          for (const [k, v] of Object.entries(data.probabilities)) {
            norm[k.toLowerCase()] = Number(v);
          }
          setProbabilities(norm);
        } else {
          const conf = (data.confidence ?? 0) * 100;
          const rest = (100 - conf) / 2;
          const others = ["healthy", "bleached", "dead"].filter(c => c !== cls);
          setProbabilities({ [cls]: conf, [others[0]]: rest, [others[1]]: rest });
        }
      } else {
        setResult("dead");
        setConfidence(0);
        setProbabilities({});
      }
    } catch (e) {
      console.error(e);
      setStatus("result");
      setResult("dead");
      setConfidence(0);
      setProbabilities({});
    }
  };

  return (
    <section id="try-model" className="py-32 relative bg-white overflow-hidden">
      {/* Subtle Radial Gradient Background */}
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,var(--tw-gradient-stops))] from-teal-50/60 via-white to-white -z-10" />

      <div className="max-w-4xl mx-auto px-6">
        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 tracking-tight mb-4">
            Try the Model
          </h2>
          <p className="text-gray-600 text-lg">
            Upload a sample image of a coral colony to test our real-time classification engine.
          </p>
        </div>

        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="bg-white rounded-3xl shadow-xl shadow-blue-900/5 border border-gray-100 overflow-hidden"
        >
          <div className="p-8 md:p-12">
            {!file ? (
              <div 
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
                className={`border-2 border-dashed rounded-2xl p-12 text-center transition-all duration-300 group cursor-pointer ${
                  isDragOver 
                    ? 'border-teal-500 bg-teal-50 animate-pulse scale-[1.02]' 
                    : 'border-teal-200 bg-white hover:bg-teal-50/30'
                }`}
              >
                <div className={`w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-6 transition-transform duration-300 ${
                  isDragOver ? 'bg-teal-500 text-white scale-110' : 'bg-teal-100 text-teal-600 group-hover:scale-110'
                }`}>
                  <UploadCloud size={28} />
                </div>
                <h4 className="text-xl font-semibold text-gray-900 mb-2">Drag & drop an image</h4>
                <p className="text-gray-500 mb-6">or click to browse from your computer</p>
                
                <label className="px-6 py-2.5 bg-white text-teal-700 font-medium rounded-full shadow-sm border border-teal-100 hover:bg-teal-50 transition-colors cursor-pointer inline-block pointer-events-auto">
                  Browse Files
                  <input 
                    type="file" 
                    className="hidden" 
                    accept="image/*"
                    onChange={(e) => {
                      if (e.target.files && e.target.files[0]) {
                        setFile(e.target.files[0]);
                        setStatus("idle");
                      }
                    }}
                  />
                </label>
              </div>
            ) : (
              <div className="space-y-8">
                {/* Selected File */}
                <div className="flex items-center justify-between p-4 bg-gray-50 rounded-xl border border-gray-200">
                  <div className="flex items-center gap-4">
                    <div className="w-12 h-12 bg-white rounded-lg border border-gray-200 flex items-center justify-center">
                      <FileImage className="text-gray-500" size={24} />
                    </div>
                    <div>
                      <p className="font-medium text-gray-900 truncate max-w-[200px] sm:max-w-xs">{file.name}</p>
                      <p className="text-sm text-gray-500">{(file.size / 1024).toFixed(1)} KB</p>
                    </div>
                  </div>
                  <button 
                    onClick={() => { setFile(null); setStatus("idle"); }}
                    className="text-gray-400 hover:text-gray-600 p-2"
                  >
                    Remove
                  </button>
                </div>

                {/* Actions & Results */}
                {status === "idle" && (
                  <div className="text-center">
                    <button 
                      onClick={handleRun}
                      className="px-8 py-3.5 bg-gray-900 text-white rounded-full font-semibold shadow-md hover:bg-gray-800 transition-colors w-full sm:w-auto"
                    >
                      Run Assessment
                    </button>
                  </div>
                )}

                {status === "analyzing" && (
                  <div className="relative overflow-hidden rounded-2xl bg-gray-50 border border-gray-100 p-12 text-center">
                    {/* Shimmer Effect */}
                    <motion.div 
                      className="absolute inset-0 bg-gradient-to-r from-transparent via-white/80 to-transparent skew-x-[-20deg]"
                      animate={{ x: ["-150%", "250%"] }}
                      transition={{ repeat: Infinity, duration: 1.5, ease: "linear" }}
                    />
                    <div className="relative z-10">
                      <div className="inline-block w-8 h-8 border-4 border-teal-100 border-t-teal-500 rounded-full animate-spin mb-4" />
                      <p className="text-gray-600 font-medium">Analyzing neural pathways...</p>
                    </div>
                  </div>
                )}

                {status === "result" && result && (
                  <motion.div
                    initial={{ opacity: 0, y: -40 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ type: "spring", stiffness: 300, damping: 24 }}
                    className={`rounded-2xl border overflow-hidden ${
                      result === "healthy" ? "bg-teal-50/40 border-teal-100" :
                      result === "bleached" ? "bg-amber-50/40 border-amber-100" :
                      "bg-rose-50/40 border-rose-100"
                    }`}
                  >
                    {/* Header row */}
                    <div className="flex items-center justify-between px-6 pt-5 pb-4">
                      <div className="flex items-center gap-3">
                        <div className={`w-11 h-11 rounded-full flex items-center justify-center ${
                          result === "healthy" ? "bg-teal-100 text-teal-600" :
                          result === "bleached" ? "bg-amber-100 text-amber-700" :
                          "bg-rose-100 text-rose-600"
                        }`}>
                          {result === "healthy" ? <Leaf size={20} /> :
                           result === "bleached" ? <AlertTriangle size={20} /> :
                           <XCircle size={20} />}
                        </div>
                        <div>
                          <p className="text-[10px] font-bold uppercase tracking-widest text-gray-400">Prediction</p>
                          <h4 className={`text-xl font-bold capitalize leading-tight ${
                            result === "healthy" ? "text-gray-900" :
                            result === "bleached" ? "text-gray-900" :
                            "text-gray-900"
                          }`}>
                            {result.charAt(0).toUpperCase() + result.slice(1)} Coral
                          </h4>
                          <p className="text-xs text-gray-400 mt-0.5">EfficientNetB0 SWA Ensemble (5-seed)</p>
                        </div>
                      </div>
                      {/* Ocean-blue confidence badge */}
                      <div className="flex flex-col items-end gap-0.5">
                        <span className="text-2xl font-bold text-white bg-blue-600 rounded-full px-4 py-1.5 leading-none tabular-nums">
                          {(confidence * 100).toFixed(1)}%
                        </span>
                        <span className="text-[10px] text-gray-400 pr-1">Confidence Score</span>
                      </div>
                    </div>

                    <div className="h-px bg-gray-100 mx-6" />

                    {/* Class Probabilities — full width */}
                    <div className="px-6 py-5 space-y-3">
                      <p className="text-[10px] font-bold uppercase tracking-widest text-gray-400 mb-3">Class Probabilities</p>

                      {(["healthy", "bleached", "dead"] as const).map((cls) => {
                        const pct = probabilities[cls] ?? 0;
                        const isActive = cls === result;
                        const barColor =
                          cls === "healthy" ? "bg-emerald-500" :
                          cls === "bleached" ? "bg-amber-600" :
                          "bg-rose-500";
                        const labelColor =
                          cls === "healthy" ? "text-emerald-600" :
                          cls === "bleached" ? "text-amber-700" :
                          "text-rose-500";
                        const icon =
                          cls === "healthy" ? <Leaf size={14} /> :
                          cls === "bleached" ? <AlertTriangle size={14} /> :
                          <XCircle size={14} />;

                        return (
                          <div key={cls} className="flex items-center gap-3">
                            <div className={`w-6 h-6 rounded-full flex items-center justify-center shrink-0 ${
                              cls === "healthy" ? "bg-emerald-100 text-emerald-600" :
                              cls === "bleached" ? "bg-amber-100 text-amber-700" :
                              "bg-rose-100 text-rose-500"
                            }`}>
                              {icon}
                            </div>
                            <span className={`w-16 text-sm font-medium capitalize ${isActive ? labelColor : "text-gray-500"}`}>
                              {cls.charAt(0).toUpperCase() + cls.slice(1)}
                            </span>
                            <div className="flex-1 h-2 bg-gray-200 rounded-full overflow-hidden">
                              <motion.div
                                initial={{ width: 0 }}
                                animate={{ width: `${pct}%` }}
                                transition={{ duration: 0.8, ease: "easeOut", delay: 0.1 }}
                                className={`h-full rounded-full ${barColor}`}
                              />
                            </div>
                            <span className={`w-12 text-right text-sm font-bold tabular-nums ${isActive ? labelColor : "text-gray-400"}`}>
                              {pct.toFixed(1)}%
                            </span>
                          </div>
                        );
                      })}

                      {/* Automated insight */}
                      <div className={`mt-4 rounded-xl px-4 py-3 text-sm font-medium flex items-center gap-2 ${
                        result === "healthy" ? "bg-emerald-50 text-emerald-700 border border-emerald-100" :
                        result === "bleached" ? "bg-amber-50 text-amber-800 border border-amber-100" :
                        "bg-rose-50 text-rose-700 border border-rose-100"
                      }`}>
                        {result === "healthy" ? <CheckCircle size={15} className="shrink-0" /> :
                         result === "bleached" ? <AlertTriangle size={15} className="shrink-0" /> :
                         <XCircle size={15} className="shrink-0" />}
                        {result === "healthy" && confidence >= 0.9
                          ? "High confidence — no manual review required."
                          : result === "healthy"
                          ? "Healthy classification detected. Verify with Grad-CAM for confidence."
                          : result === "bleached"
                          ? "Bleaching detected. Manual review and monitoring recommended."
                          : "Dead coral classified. Field verification advised."}
                      </div>
                    </div>
                  </motion.div>
                )}
              </div>
            )}
          </div>
        </motion.div>
      </div>
    </section>
  );
}
