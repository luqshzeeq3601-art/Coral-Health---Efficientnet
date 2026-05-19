import React from "react";
import { motion } from "motion/react";
import { ArrowRight, Sparkles } from "lucide-react";

export function Hero() {
  const titleText = "Coral Health AI Assessment";
  const container = {
    hidden: { opacity: 0 },
    show: {
      opacity: 1,
      transition: { staggerChildren: 0.04, delayChildren: 0.2 }
    }
  };
  const item = {
    hidden: { opacity: 0, y: 30 },
    show: { opacity: 1, y: 0, transition: { type: "spring", damping: 12, stiffness: 100 } }
  };

  return (
    <section className="relative pt-32 pb-20 lg:pt-48 lg:pb-32 overflow-hidden">
      {/* Animated Mesh Gradient Background */}
      <motion.div 
        className="absolute inset-0 bg-[linear-gradient(120deg,#FFFFFF,#E0F7FA,#FFFFFF)] bg-[length:200%_200%] -z-10"
        animate={{ backgroundPosition: ["0% 50%", "100% 50%", "0% 50%"] }}
        transition={{ repeat: Infinity, duration: 15, ease: "linear" }}
      />
      
      <div className="max-w-7xl mx-auto px-6 grid lg:grid-cols-2 gap-16 items-center">
        <motion.div 
          initial={{ opacity: 0, x: -30 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.8, ease: "easeOut" }}
          className="max-w-2xl"
        >
          <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-teal-50 text-teal-700 text-sm font-medium mb-6 border border-teal-100/50">
            <Sparkles size={14} className="text-teal-500" />
            <span>Introducing v2.0 Architecture</span>
          </div>
          
          <motion.h1 
            variants={container}
            initial="hidden"
            animate="show"
            className="text-5xl lg:text-7xl font-extrabold tracking-tight text-gray-900 leading-[1.1] mb-6 flex flex-wrap"
          >
            {titleText.split("").map((char, i) => (
              <motion.span 
                key={i} 
                variants={item}
                className={i > 12 ? "text-transparent bg-clip-text bg-gradient-to-r from-teal-500 to-blue-600" : ""}
              >
                {char === " " ? "\u00A0" : char}
              </motion.span>
            ))}
          </motion.h1>

          <p className="text-lg text-gray-600 mb-8 leading-relaxed max-w-xl">
            98.11% Accuracy in Real-Time Reef Assessment. Empowering marine biologists with explainable, high-speed deep learning to monitor and protect coral ecosystems globally.
          </p>
          <div className="flex flex-col sm:flex-row items-center gap-4">
            <a 
              href="#try-model"
              className="w-full sm:w-auto px-8 py-4 bg-gradient-to-r from-teal-500 to-blue-600 text-white rounded-full font-semibold shadow-lg shadow-blue-500/25 hover:shadow-xl hover:shadow-blue-500/40 transition-all flex items-center justify-center gap-2 group"
            >
              Try Model
              <ArrowRight size={18} className="group-hover:translate-x-1 transition-transform" />
            </a>
            <a 
              href="#performance"
              className="w-full sm:w-auto px-8 py-4 bg-white/50 backdrop-blur-sm text-gray-700 rounded-full font-semibold border border-gray-200 hover:border-gray-300 hover:bg-white transition-all flex items-center justify-center"
            >
              View Metrics
            </a>
          </div>
        </motion.div>

        <motion.div 
          initial={{ opacity: 0, scale: 0.9, rotateY: 15 }}
          animate={{ opacity: 1, scale: 1, rotateY: 0 }}
          transition={{ duration: 1, ease: "easeOut", delay: 0.2 }}
          className="relative perspective-1000"
        >
          {/* Glassmorphism container with floating animation */}
          <motion.div 
            animate={{ y: [-15, 15, -15] }}
            transition={{ repeat: Infinity, duration: 5, ease: "easeInOut" }}
            className="relative rounded-3xl overflow-hidden shadow-2xl shadow-blue-900/10 border border-white/60 bg-white/20 backdrop-blur-xl aspect-[4/3] group transform-gpu"
          >
            <div className="absolute inset-0 bg-gradient-to-tr from-teal-500/10 to-blue-500/10 z-10 pointer-events-none" />
            <img 
              src="https://images.unsplash.com/photo-1641377784198-4a207ff00894?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHwzZCUyMGFic3RyYWN0JTIwY29yYWwlMjByZWVmJTIwYmx1ZXxlbnwxfHx8fDE3NzI4NjkyNDV8MA&ixlib=rb-4.1.0&q=80&w=1080" 
              alt="3D abstract coral representation" 
              className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700 ease-out"
            />
            
            {/* Floating particle effects (simulated) */}
            <div className="absolute top-1/4 left-1/4 w-3 h-3 bg-teal-400 rounded-full blur-[2px] animate-pulse z-20 shadow-[0_0_15px_rgba(45,212,191,0.8)]" />
            <div className="absolute top-2/3 right-1/4 w-4 h-4 bg-blue-400 rounded-full blur-[2px] animate-pulse z-20 shadow-[0_0_20px_rgba(96,165,250,0.8)]" style={{ animationDelay: '1s' }} />
            <div className="absolute bottom-1/4 left-1/3 w-2 h-2 bg-white rounded-full blur-[1px] animate-ping z-20" style={{ animationDuration: '3s' }} />
          </motion.div>
        </motion.div>
      </div>
    </section>
  );
}
