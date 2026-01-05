import React from 'react';
import { CheckCircle, Leaf } from 'lucide-react';

const ResultSection = ({ result }) => {
    if (!result) return null;

    return (
        <div className="w-full bg-white rounded-3xl shadow-xl shadow-emerald-100/50 border border-emerald-50 overflow-hidden animate-in fade-in slide-in-from-bottom-4 duration-700">
            {/* Header with status */}
            <div className="bg-emerald-50/50 px-8 py-6 border-b border-emerald-100 flex items-center justify-between">
                <div className="flex items-center gap-3">
                    <div className="bg-green-100 p-1.5 rounded-full">
                        <CheckCircle className="w-5 h-5 text-green-600" />
                    </div>
                    <span className="font-semibold text-emerald-900">Identification Successful</span>
                </div>
                <span className="px-3 py-1 bg-white rounded-full text-xs font-bold text-emerald-600 shadow-sm border border-emerald-100">
                    AI Model v2.4
                </span>
            </div>

            <div className="p-8 space-y-8">
                {/* Title Area */}
                <div>
                    <h2 className="text-4xl font-extrabold text-gray-900 mb-2 tracking-tight">{result.name}</h2>
                    <p className="text-lg text-emerald-600 font-medium italic font-serif flex items-center gap-2">
                        {result.scientificName}
                    </p>
                </div>

                {/* Stats Grid */}
                <div className="grid grid-cols-2 gap-4">
                    <div className="bg-gray-50 p-4 rounded-2xl border border-gray-100 hover:border-emerald-200 transition-colors group">
                        <span className="text-xs text-gray-500 uppercase font-bold tracking-wider mb-1 block group-hover:text-emerald-600">Match Confidence</span>
                        <div className="flex items-end gap-2">
                            <span className="text-3xl font-black text-gray-900">{result.confidence}%</span>
                            <div className="h-2 w-full bg-gray-200 rounded-full mb-1.5 overflow-hidden">
                                <div className="h-full bg-emerald-500 rounded-full" style={{ width: `${result.confidence}%` }}></div>
                            </div>
                        </div>
                    </div>

                    <div className="bg-gray-50 p-4 rounded-2xl border border-gray-100 hover:border-emerald-200 transition-colors group">
                        <span className="text-xs text-gray-500 uppercase font-bold tracking-wider mb-1 block group-hover:text-emerald-600">Health Status</span>
                        <div className="flex items-center gap-2">
                            <span className="text-2xl font-bold text-emerald-600">Healthy</span>
                            <Leaf className="w-5 h-5 text-emerald-500" />
                        </div>
                        <p className="text-xs text-gray-400 mt-1">No visible pests or diseases</p>
                    </div>
                </div>

                {/* Description */}
                <div className="prose prose-emerald">
                    <h4 className="font-bold text-gray-900 text-lg mb-3 flex items-center gap-2">
                        <span className="w-1 h-6 bg-emerald-500 rounded-full block"></span>
                        About this species
                    </h4>
                    <p className="text-gray-600 leading-relaxed text-lg">
                        {result.description}
                    </p>
                </div>

                {/* Tags */}
                <div className="flex flex-wrap gap-2 pt-4 border-t border-gray-100">
                    {['Indoor', 'Low Light', 'Purifier', 'Tropical'].map(tag => (
                        <span key={tag} className="px-3 py-1 bg-gray-100 text-gray-600 rounded-full text-sm font-medium hover:bg-emerald-100 hover:text-emerald-700 transition-colors cursor-default">
                            #{tag}
                        </span>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default ResultSection;
