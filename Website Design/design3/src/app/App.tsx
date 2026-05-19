import React from 'react';
import { Header } from './components/Header';
import { Hero } from './components/Hero';
import { About } from './components/About';
import { Features } from './components/Features';
import { Performance } from './components/Performance';
import { TryModel } from './components/TryModel';
import { Footer } from './components/Footer';

export default function App() {
  return (
    <div className="min-h-screen bg-white font-sans text-gray-900 selection:bg-teal-100 selection:text-teal-900">
      <Header />
      <main>
        <Hero />
        <About />
        <Features />
        <Performance />
        <TryModel />
      </main>
      <Footer />
    </div>
  );
}
