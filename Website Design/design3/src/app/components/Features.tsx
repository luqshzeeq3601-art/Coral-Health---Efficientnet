import React from "react";
import { motion } from "motion/react";
import { Network, Zap, Eye } from "lucide-react";

export function Features() {
  const features = [
    {
      icon: <Network className="text-teal-500" size={32} />,
      title: "EfficientNet-B0 Backbone",
      description: "Optimized compound scaling provides state-of-the-art accuracy while maintaining a small parameter footprint."
    },
    {
      icon: <Zap className="text-blue-500" size={32} />,
      title: "Real-time Classification",
      description: "Sub-50ms inference latency allows for smooth, continuous analysis of live underwater video feeds."
    },
    {
      icon: <Eye className="text-indigo-500" size={32} />,
      title: "Explainable AI",
      description: "Grad-CAM heatmaps highlight exactly which visual features the model used to make its health determination."
    }
  ];

  return (
    <section id="features" className="py-24 bg-slate-50 relative">
      <div className="max-w-7xl mx-auto px-6">
        <div className="text-center max-w-2xl mx-auto mb-16">
          <h2 className="text-sm font-semibold text-blue-600 tracking-wider uppercase mb-3">Technology</h2>
          <h3 className="text-3xl md:text-4xl font-bold text-gray-900 tracking-tight">
            Built for Precision and Speed
          </h3>
        </div>

        <div className="grid md:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: "-50px" }}
              transition={{ duration: 0.5, delay: index * 0.15 }}
              whileHover={{ y: -10 }}
              className="relative group rounded-2xl p-8 bg-white border border-transparent shadow-sm transition-all duration-300 overflow-hidden"
            >
              {/* Intense turquoise border glow on hover */}
              <div className="absolute inset-0 rounded-2xl border-2 border-transparent group-hover:border-teal-400/60 shadow-[0_0_0_0_transparent] group-hover:shadow-[0_0_30px_rgba(45,212,191,0.25)] transition-all duration-500 pointer-events-none" />
              
              <div className="relative z-10">
                <div className="w-14 h-14 rounded-xl bg-gray-50 flex items-center justify-center mb-6 transition-colors border border-gray-100 group-hover:border-transparent group-hover:bg-white group-hover:shadow-sm">
                  {/* Subtle Icon Pulse Animation */}
                  <motion.div
                    animate={{ scale: [1, 1.15, 1] }}
                    transition={{ repeat: Infinity, duration: 2.5, ease: "easeInOut" }}
                  >
                    {feature.icon}
                  </motion.div>
                </div>
                <h4 className="text-xl font-bold text-gray-900 mb-3">{feature.title}</h4>
                <p className="text-gray-600 leading-relaxed">
                  {feature.description}
                </p>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
