import React from "react";
import { Activity } from "lucide-react";

export function Footer() {
  return (
    <footer className="bg-white border-t border-gray-100 py-12">
      <div className="max-w-7xl mx-auto px-6 flex flex-col md:flex-row items-center justify-between">
        <div className="flex items-center gap-2 mb-6 md:mb-0">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-teal-400 to-blue-500 flex items-center justify-center text-white shadow-sm">
            <Activity size={18} />
          </div>
          <span className="font-bold text-xl tracking-tight text-gray-900">Coral Health AI</span>
        </div>
        
        <div className="text-gray-500 text-sm">
          &copy; {new Date().getFullYear()} Coral Health AI Initiative. Built for marine conservation.
        </div>
      </div>
    </footer>
  );
}
