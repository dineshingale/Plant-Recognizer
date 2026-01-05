import React, { useState } from 'react';
import { Upload, Camera, X } from 'lucide-react';

const ImageUpload = ({ image, onImageSelect, onClear }) => {
    const [isDragging, setIsDragging] = useState(false);

    // Handle Drag Events
    const handleDragOver = (e) => {
        e.preventDefault();
        setIsDragging(true);
    };

    const handleDragLeave = (e) => {
        e.preventDefault();
        setIsDragging(false);
    };

    const handleDrop = (e) => {
        e.preventDefault();
        setIsDragging(false);
        const file = e.dataTransfer.files[0];
        if (file && file.type.startsWith('image/')) {
            onImageSelect(file);
        }
    };

    // Handle Click Upload
    const handleFileInput = (e) => {
        const file = e.target.files[0];
        if (file) onImageSelect(file);
    };

    return (
        <div
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            onClick={() => document.getElementById('fileInput').click()}
            className={`
        group relative border-2 border-dashed rounded-[2rem] p-4 transition-all duration-300 ease-in-out min-h-[450px] flex flex-col items-center justify-center text-center cursor-pointer overflow-hidden
        ${isDragging
                    ? 'border-emerald-500 bg-emerald-50/50 scale-[1.02] shadow-2xl shadow-emerald-100/50'
                    : 'border-gray-200 bg-white hover:border-emerald-400 hover:shadow-xl hover:shadow-gray-100'
                }
        ${image ? 'border-none p-0 bg-gray-900' : ''}
      `}
        >
            <input
                id="fileInput"
                type="file"
                accept="image/*"
                onChange={handleFileInput}
                className="hidden"
            />

            {image ? (
                <div className="relative w-full h-full flex items-center justify-center bg-gray-900 rounded-[2rem]">
                    <img
                        src={image}
                        alt="Preview"
                        className="w-full h-full object-cover opacity-90 transition-opacity group-hover:opacity-60"
                    />
                    <div className="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                        <span className="bg-white/20 backdrop-blur-md text-white px-6 py-3 rounded-full font-medium border border-white/30 flex items-center gap-2">
                            <Camera className="w-5 h-5" /> Change Photo
                        </span>
                    </div>
                    <button
                        onClick={(e) => { e.stopPropagation(); onClear(); }}
                        className="absolute top-4 right-4 p-2 bg-black/50 hover:bg-black/70 text-white rounded-full backdrop-blur-sm transition-colors z-20"
                    >
                        <X className="w-5 h-5" />
                    </button>
                </div>
            ) : (
                <div className="space-y-6 pointer-events-none">
                    <div className={`
            w-24 h-24 rounded-3xl flex items-center justify-center mx-auto transition-all duration-300
            ${isDragging ? 'bg-white scale-110 shadow-lg' : 'bg-emerald-50 group-hover:scale-110 group-hover:bg-emerald-100'}
          `}>
                        <Upload className={`w-10 h-10 transition-colors ${isDragging ? 'text-emerald-600' : 'text-emerald-500'}`} />
                    </div>
                    <div className="space-y-2">
                        <h3 className="text-2xl font-bold text-gray-800">
                            Drop image here
                        </h3>
                        <p className="text-gray-500">
                            or click to browse files
                        </p>
                    </div>
                    <div className="pt-8 flex items-center justify-center gap-4 opacity-50">
                        <span className="text-xs px-2 py-1 bg-gray-100 rounded text-gray-600 font-mono">JPG</span>
                        <span className="text-xs px-2 py-1 bg-gray-100 rounded text-gray-600 font-mono">PNG</span>
                        <span className="text-xs px-2 py-1 bg-gray-100 rounded text-gray-600 font-mono">WEBP</span>
                    </div>
                </div>
            )}
        </div>
    );
};

export default ImageUpload;
