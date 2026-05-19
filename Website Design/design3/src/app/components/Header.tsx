import React from "react";
import { motion } from "motion/react";
import { Activity } from "lucide-react";

export function Header() {
  return (
    <motion.header 
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
      className="fixed top-0 left-0 right-0 z-50 bg-white/80 backdrop-blur-md border-b border-gray-100"
    >
      <div className="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-teal-400 to-blue-500 flex items-center justify-center text-white shadow-lg shadow-teal-500/30">
            <Activity size={18} />
          </div>
          <span className="font-bold text-xl tracking-tight text-gray-900">Coral Health AI</span>
        </div>
        <nav className="hidden md:flex items-center gap-8 text-sm font-medium text-gray-600">
          <a href="#about" className="hover:text-teal-600 transition-colors">About</a>
          <a href="#features" className="hover:text-teal-600 transition-colors">Technology</a>
          <a href="#performance" className="hover:text-teal-600 transition-colors">Performance</a>
        </nav>
        <a 
          href="#try-model"
          className="px-5 py-2.5 bg-gray-900 text-white text-sm font-medium rounded-full hover:bg-gray-800 transition-colors shadow-sm"
        >
          Try Model
        </a>
      </div>
    </motion.header>
  );
}
