import React from 'react';
import { Leaf, Loader2, ScanLine } from 'lucide-react';

const Navbar = ({ onRecognize, isAnalyzing, hasImage }) => {
    return (
        <nav className="w-full bg-white/90 backdrop-blur-md border-b border-emerald-100 px-6 py-4 flex items-center justify-between sticky top-0 z-50 shadow-sm transition-all">
            {/* 1. Branding */}
            <div className="flex items-center gap-3 cursor-pointer group">
                <div className="bg-emerald-100 p-2.5 rounded-xl group-hover:bg-emerald-200 transition-colors duration-300">
                    <Leaf className="w-6 h-6 text-emerald-600" />
                </div>
                <span className="text-xl font-bold text-gray-800 tracking-tight">
                    Plant<span className="text-emerald-600">Lens</span>
                </span>
            </div>

            {/* 2. Recognize Button */}
            <button
                onClick={onRecognize}
                disabled={isAnalyzing || !hasImage}
                className={`
          flex items-center gap-2 px-6 py-2.5 rounded-full font-medium transition-all transform active:scale-95 shadow-lg shadow-emerald-200
          ${isAnalyzing || !hasImage
                        ? 'bg-gray-100 text-gray-400 cursor-not-allowed shadow-none'
                        : 'bg-emerald-600 hover:bg-emerald-700 text-white hover:shadow-emerald-300'
                    }
        `}
            >
                {isAnalyzing ? (
                    <>
                        <Loader2 className="w-4 h-4 animate-spin" />
                        Scanning...
                    </>
                ) : (
                    <>
                        <ScanLine className="w-4 h-4" />
                        Recognize Plant
                    </>
                )}
            </button>
        </nav>
    );
};

export default Navbar;
