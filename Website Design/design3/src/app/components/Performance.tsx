import React, { useEffect, useRef } from "react";
import { motion, animate, useInView } from "motion/react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Area, AreaChart } from "recharts";

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

function CountUp({ value, prefix = "", suffix = "", decimals = 0, duration = 1.5 }: { value: number, prefix?: string, suffix?: string, decimals?: number, duration?: number }) {
  const ref = useRef<HTMLSpanElement>(null);
  const isInView = useInView(ref, { once: true, margin: "-50px" });

  useEffect(() => {
    if (isInView && ref.current) {
      const controls = animate(0, value, {
        duration,
        ease: "easeOut",
        onUpdate(val) {
          if (ref.current) {
            ref.current.textContent = prefix + val.toFixed(decimals) + suffix;
          }
        }
      });
      return () => controls.stop();
    }
  }, [value, duration, isInView, prefix, suffix, decimals]);

  return <span ref={ref}>0{suffix}</span>;
}

export function Performance() {
  const metrics = [
    { label: "Accuracy", value: 97.48, decimals: 2, trend: "+1.2%" },
    { label: "Precision", value: 96.4, decimals: 2, trend: "+0.8%" },
    { label: "Recall", value: 96.4, decimals: 2, trend: "+1.5%" },
  ];

  return (
    <section id="performance" className="py-24 bg-slate-50 relative border-t border-gray-100">
      <div className="max-w-7xl mx-auto px-6">
        
        {/* Dark Glass Container nested in light theme */}
        <div className="bg-gray-900/95 backdrop-blur-2xl rounded-[2.5rem] border border-gray-800 p-8 md:p-12 shadow-[0_30px_60px_-15px_rgba(0,0,0,0.5)] relative overflow-hidden">
          {/* Subtle lighting inside glass */}
          <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[800px] h-[400px] bg-blue-500/10 blur-[100px] rounded-full pointer-events-none" />

          <div className="text-center max-w-2xl mx-auto mb-16 relative z-10">
            <h2 className="text-sm font-semibold text-teal-400 tracking-wider uppercase mb-3">Model Evaluation</h2>
            <h3 className="text-3xl md:text-4xl font-bold text-white tracking-tight">
              Rigorous Benchmarking
            </h3>
            <p className="mt-4 text-gray-400">
              Our EfficientNet-B0 architecture demonstrates exceptional performance across all key metrics on the Global Coral Reef Dataset.
            </p>
          </div>

          {/* Dashboard Grid */}
          <div className="grid lg:grid-cols-3 gap-8 mb-8 relative z-10">
            {/* Metrics */}
            <div className="lg:col-span-1 space-y-4">
              {metrics.map((metric, i) => (
                <motion.div 
                  key={i}
                  initial={{ opacity: 0, x: -20 }}
                  whileInView={{ opacity: 1, x: 0 }}
                  viewport={{ once: true }}
                  transition={{ duration: 0.5, delay: i * 0.1 }}
                  className="bg-gray-800/50 rounded-2xl p-6 border border-gray-700/50 flex items-center justify-between backdrop-blur-sm shadow-inner"
                >
                  <div>
                    <p className="text-sm font-medium text-gray-400 mb-1">{metric.label}</p>
                    <p className="text-3xl font-bold text-white">
                      <CountUp value={metric.value} suffix="%" decimals={metric.decimals} duration={1.5} />
                    </p>
                  </div>
                  <div className="text-sm font-semibold text-teal-400 bg-teal-400/10 px-2.5 py-1 rounded-md border border-teal-400/20">
                    {metric.trend}
                  </div>
                </motion.div>
              ))}
            </div>

            {/* Chart */}
            <motion.div 
              initial={{ opacity: 0, scale: 0.95 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true }}
              transition={{ duration: 0.7 }}
              className="lg:col-span-2 bg-gray-800/40 rounded-2xl p-6 border border-gray-700/50 backdrop-blur-sm"
            >
              <div className="mb-6 flex justify-between items-center">
                <div>
                  <h4 className="font-bold text-white">Training & Validation Loss</h4>
                  <p className="text-sm text-gray-400">Cross-entropy loss over 50 epochs</p>
                </div>
                <div className="flex gap-4 text-sm font-medium">
                  <div className="flex items-center gap-2 text-teal-400"><span className="w-3 h-3 rounded-full bg-teal-400 shadow-[0_0_8px_rgba(45,212,191,0.6)]"></span>Train</div>
                  <div className="flex items-center gap-2 text-blue-400"><span className="w-3 h-3 rounded-full bg-blue-500 shadow-[0_0_8px_rgba(59,130,246,0.6)]"></span>Val</div>
                </div>
              </div>
              
              <div className="h-64 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={data} margin={{ top: 5, right: 0, left: -20, bottom: 0 }}>
                    <defs key="defs">
                      <linearGradient id="colorLoss" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#2dd4bf" stopOpacity={0.3}/>
                        <stop offset="95%" stopColor="#2dd4bf" stopOpacity={0}/>
                      </linearGradient>
                      <linearGradient id="colorVal" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3}/>
                        <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
                      </linearGradient>
                    </defs>
                    <CartesianGrid key="grid" strokeDasharray="3 3" vertical={false} stroke="#374151" />
                    <XAxis key="xaxis" dataKey="epoch" axisLine={false} tickLine={false} tick={{fill: '#9ca3af', fontSize: 12}} />
                    <YAxis key="yaxis" axisLine={false} tickLine={false} tick={{fill: '#9ca3af', fontSize: 12}} />
                    <Tooltip key="tooltip" 
                      contentStyle={{ borderRadius: '12px', border: '1px solid #374151', backgroundColor: '#1f2937', color: '#f3f4f6', boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.5)' }}
                      itemStyle={{ color: '#f3f4f6' }}
                    />
                    <Area key="area-loss" type="monotone" dataKey="loss" stroke="#2dd4bf" strokeWidth={3} fillOpacity={1} fill="url(#colorLoss)" activeDot={{r: 6, strokeWidth: 0}} isAnimationActive={true} animationDuration={2000} />
                    <Area key="area-val" type="monotone" dataKey="val_loss" stroke="#3b82f6" strokeWidth={3} fillOpacity={1} fill="url(#colorVal)" isAnimationActive={true} animationDuration={2000} />
                  </AreaChart>
                </ResponsiveContainer>
              </div>
            </motion.div>
          </div>

          {/* Confusion Matrix Dark UI */}
          <motion.div 
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6, delay: 0.3 }}
              className="bg-gray-800/40 rounded-2xl p-8 border border-gray-700/50 max-w-3xl mx-auto relative z-10 backdrop-blur-sm"
          >
            <div className="mb-6">
              <h4 className="font-bold text-white">Confusion Matrix</h4>
              <p className="text-sm text-gray-400">True vs Predicted Classes</p>
            </div>
            
            <div className="grid grid-cols-4 gap-2 text-center text-sm font-medium">
              <div className="col-span-1"></div>
              <div className="text-gray-400">Pred: Healthy</div>
              <div className="text-gray-400">Pred: Bleached</div>
              <div className="text-gray-400">Pred: Dead</div>

              <div className="text-gray-400 text-right pr-4 self-center">True: Healthy</div>
              <div className="bg-teal-500/90 text-white rounded-lg py-3 shadow-inner">985</div>
              <div className="bg-gray-800 text-teal-400 rounded-lg py-3 border border-gray-700/50">12</div>
              <div className="bg-gray-800/50 text-teal-500 rounded-lg py-3 border border-gray-700/30">3</div>

              <div className="text-gray-400 text-right pr-4 self-center">True: Bleached</div>
              <div className="bg-gray-800 text-blue-400 rounded-lg py-3 border border-gray-700/50">8</div>
              <div className="bg-blue-500/90 text-white rounded-lg py-3 shadow-inner">482</div>
              <div className="bg-gray-800/50 text-blue-500 rounded-lg py-3 border border-gray-700/30">10</div>

              <div className="text-gray-400 text-right pr-4 self-center">True: Dead</div>
              <div className="bg-gray-800/50 text-gray-500 rounded-lg py-3 border border-gray-700/30">2</div>
              <div className="bg-gray-800 text-gray-400 rounded-lg py-3 border border-gray-700/50">14</div>
              <div className="bg-gray-600/90 text-white rounded-lg py-3 shadow-inner">284</div>
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  );
}
