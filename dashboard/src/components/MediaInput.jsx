import React, { useState } from 'react';
import { Youtube, Upload, FileVideo, X, Clock, Hash, Video } from 'lucide-react';

const DURATION_OPTIONS = [5, 10, 30, 60];
const CLIP_COUNT_OPTIONS = [
    { value: 0, label: 'Auto' },
    { value: 3, label: '3' },
    { value: 5, label: '5' },
    { value: 10, label: '10' },
    { value: 15, label: '15' },
];
const QUALITY_OPTIONS = [
    { value: 'best', label: 'Máxima' },
    { value: '1080p', label: '1080p' },
    { value: '720p', label: '720p' },
    { value: '480p', label: '480p' },
];

export default function MediaInput({ onProcess, isProcessing }) {
    const [mode, setMode] = useState('url'); // 'url' | 'file'
    const [url, setUrl] = useState('');
    const [file, setFile] = useState(null);
    const [targetDuration, setTargetDuration] = useState(30);
    const [clipCount, setClipCount] = useState(0);
    const [quality, setQuality] = useState('best');

    const handleSubmit = (e) => {
        e.preventDefault();
        const extras = { targetDuration, clipCount, quality };
        if (mode === 'url' && url) {
            onProcess({ type: 'url', payload: url, ...extras });
        } else if (mode === 'file' && file) {
            onProcess({ type: 'file', payload: file, ...extras });
        }
    };

    const handleDrop = (e) => {
        e.preventDefault();
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            setFile(e.dataTransfer.files[0]);
            setMode('file');
        }
    };

    return (
        <div className="bg-surface border border-white/5 rounded-2xl p-6 animate-[fadeIn_0.6s_ease-out]">
            <div className="flex gap-4 mb-6 border-b border-white/5 pb-4">
                <button
                    onClick={() => setMode('url')}
                    className={`flex items-center gap-2 pb-2 px-2 transition-all ${mode === 'url'
                        ? 'text-primary border-b-2 border-primary -mb-[17px]'
                        : 'text-zinc-400 hover:text-white'
                        }`}
                >
                    <Youtube size={18} />
                    YouTube URL
                </button>
                <button
                    onClick={() => setMode('file')}
                    className={`flex items-center gap-2 pb-2 px-2 transition-all ${mode === 'file'
                        ? 'text-primary border-b-2 border-primary -mb-[17px]'
                        : 'text-zinc-400 hover:text-white'
                        }`}
                >
                    <Upload size={18} />
                    Upload File
                </button>
            </div>

            <form onSubmit={handleSubmit}>
                {mode === 'url' ? (
                    <div className="space-y-4">
                        <input
                            type="url"
                            value={url}
                            onChange={(e) => setUrl(e.target.value)}
                            placeholder="https://www.youtube.com/watch?v=..."
                            className="input-field"
                            required
                        />
                    </div>
                ) : (
                    <div
                        className={`border-2 border-dashed rounded-xl p-8 text-center transition-all ${file ? 'border-primary/50 bg-primary/5' : 'border-zinc-700 hover:border-zinc-500 bg-white/5'
                            }`}
                        onDragOver={(e) => e.preventDefault()}
                        onDrop={handleDrop}
                    >
                        {file ? (
                            <div className="flex items-center justify-center gap-3 text-white">
                                <FileVideo className="text-primary" />
                                <span className="font-medium">{file.name}</span>
                                <button
                                    type="button"
                                    onClick={() => setFile(null)}
                                    className="p-1 hover:bg-white/10 rounded-full"
                                >
                                    <X size={16} />
                                </button>
                            </div>
                        ) : (
                            <label className="cursor-pointer block">
                                <input
                                    type="file"
                                    accept="video/*"
                                    onChange={(e) => setFile(e.target.files?.[0] || null)}
                                    className="hidden"
                                />
                                <Upload className="mx-auto mb-3 text-zinc-500" size={24} />
                                <p className="text-zinc-400">Click to upload or drag and drop</p>
                                <p className="text-xs text-zinc-600 mt-1">MP4, MOV up to 500MB</p>
                            </label>
                        )}
                    </div>
                )}

                <div className="mt-6">
                    <label className="flex items-center gap-2 text-sm text-zinc-400 mb-2">
                        <Clock size={14} />
                        Duración objetivo por short
                    </label>
                    <div className="flex gap-2 flex-wrap">
                        {DURATION_OPTIONS.map((secs) => (
                            <button
                                key={secs}
                                type="button"
                                onClick={() => setTargetDuration(secs)}
                                disabled={isProcessing}
                                className={`px-4 py-2 rounded-lg text-sm font-medium transition-all border ${
                                    targetDuration === secs
                                        ? 'bg-primary/20 border-primary text-primary'
                                        : 'bg-white/5 border-white/10 text-zinc-300 hover:bg-white/10'
                                } disabled:opacity-50 disabled:cursor-not-allowed`}
                            >
                                {secs}s
                            </button>
                        ))}
                    </div>
                </div>

                <div className="mt-4">
                    <label className="flex items-center gap-2 text-sm text-zinc-400 mb-2">
                        <Hash size={14} />
                        Cantidad de clips
                    </label>
                    <div className="flex gap-2 flex-wrap">
                        {CLIP_COUNT_OPTIONS.map(({ value, label }) => (
                            <button
                                key={value}
                                type="button"
                                onClick={() => setClipCount(value)}
                                disabled={isProcessing}
                                className={`px-4 py-2 rounded-lg text-sm font-medium transition-all border ${
                                    clipCount === value
                                        ? 'bg-primary/20 border-primary text-primary'
                                        : 'bg-white/5 border-white/10 text-zinc-300 hover:bg-white/10'
                                } disabled:opacity-50 disabled:cursor-not-allowed`}
                            >
                                {label}
                            </button>
                        ))}
                    </div>
                </div>

                <div className="mt-4">
                    <label className="flex items-center gap-2 text-sm text-zinc-400 mb-2">
                        <Video size={14} />
                        Calidad de video
                    </label>
                    <div className="flex gap-2 flex-wrap">
                        {QUALITY_OPTIONS.map(({ value, label }) => (
                            <button
                                key={value}
                                type="button"
                                onClick={() => setQuality(value)}
                                disabled={isProcessing}
                                className={`px-4 py-2 rounded-lg text-sm font-medium transition-all border ${
                                    quality === value
                                        ? 'bg-primary/20 border-primary text-primary'
                                        : 'bg-white/5 border-white/10 text-zinc-300 hover:bg-white/10'
                                } disabled:opacity-50 disabled:cursor-not-allowed`}
                            >
                                {label}
                            </button>
                        ))}
                    </div>
                </div>

                <button
                    type="submit"
                    disabled={isProcessing || (mode === 'url' && !url) || (mode === 'file' && !file)}
                    className="w-full btn-primary mt-6 flex items-center justify-center gap-2"
                >
                    {isProcessing ? (
                        <>
                            <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                            Processing Video...
                        </>
                    ) : (
                        <>
                            Generate Clips
                        </>
                    )}
                </button>
            </form>
        </div>
    );
}
