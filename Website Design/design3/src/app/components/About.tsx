import React from "react";
import { motion } from "motion/react";
import { Play } from "lucide-react";

export function About() {
  return (
    <section id="about" className="py-24 bg-white border-y border-gray-100">
      <div className="max-w-7xl mx-auto px-6">
        <div className="grid lg:grid-cols-2 gap-16 items-center">
          <motion.div 
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true, margin: "-100px" }}
            transition={{ duration: 0.5 }}
            className="relative order-2 lg:order-1 flex justify-center"
          >
            {/* Mask Reveal Video Placeholder */}
            <motion.div 
              initial={{ clipPath: "circle(10% at 50% 50%)" }}
              whileInView={{ clipPath: "circle(150% at 50% 50%)" }}
              viewport={{ once: true, margin: "-100px" }}
              transition={{ duration: 1.5, ease: "easeInOut" }}
              className="relative w-full rounded-2xl overflow-hidden shadow-2xl aspect-video group cursor-pointer bg-gray-900"
            >
              <img 
                src="https://images.unsplash.com/photo-1628371217613-714161455f6b?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHx1bmRlcndhdGVyJTIwY29yYWwlMjByZWVmJTIwc2N1YmF8ZW58MXx8fHwxNzcyODY5MjQ1fDA&ixlib=rb-4.1.0&q=80&w=1080" 
                alt="Underwater coral reef video placeholder" 
                className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105 opacity-80"
              />
              <div className="absolute inset-0 bg-gray-900/20 group-hover:bg-gray-900/10 transition-colors flex items-center justify-center backdrop-blur-[1px]">
                <div className="w-16 h-16 bg-white/90 backdrop-blur-sm rounded-full flex items-center justify-center shadow-lg group-hover:scale-110 transition-transform">
                  <Play className="text-teal-600 ml-1" fill="currentColor" size={24} />
                </div>
              </div>
            </motion.div>
            
            {/* Decorative element */}
            <div className="absolute -bottom-6 -right-6 w-32 h-32 bg-[radial-gradient(circle_at_center,_var(--tw-gradient-stops))] from-teal-500/20 to-transparent blur-2xl -z-10" />
          </motion.div>

          {/* Fade-in-right with Blur-to-Clear */}
          <motion.div 
            initial={{ opacity: 0, x: 40, filter: "blur(10px)" }}
            whileInView={{ opacity: 1, x: 0, filter: "blur(0px)" }}
            viewport={{ once: true, margin: "-100px" }}
            transition={{ duration: 0.8, ease: "easeOut" }}
            className="order-1 lg:order-2"
          >
            <h2 className="text-sm font-semibold text-teal-600 tracking-wider uppercase mb-3">The Mission</h2>
            <h3 className="text-3xl md:text-4xl font-bold text-gray-900 mb-6 tracking-tight">
              Automating Reef Monitoring for Marine Biologists
            </h3>
            <p className="text-gray-600 mb-6 leading-relaxed text-lg">
              Manual assessment of coral health is slow, expensive, and subject to human error. Coral Health AI leverages state-of-the-art computer vision to instantly classify reef conditions.
            </p>
            <p className="text-gray-600 leading-relaxed text-lg">
              Powered by an <strong className="text-gray-900 font-semibold">EfficientNet-B0</strong> backbone, our model balances exceptional accuracy with lightweight inference, making it perfect for real-time edge deployment on autonomous underwater vehicles (AUVs) and diver-operated cameras.
            </p>
          </motion.div>
        </div>
      </div>
    </section>
  );
}
