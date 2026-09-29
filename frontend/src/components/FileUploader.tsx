import { useState, useRef } from "react";
import type { DragEvent, ChangeEvent } from "react";
import type { IngestionState } from "../types";

interface FileUploaderProps {
    onUpload: (file: File) => void;
    ingestionState: IngestionState | null;
    isUploading: boolean;
}

export function FileUploader( {onUpload, ingestionState, isUploading}: FileUploaderProps ) {
    const [dragActive, setDragActive] = useState(false);
    const inputRef = useRef<HTMLInputElement>(null);

    const handleDrag = (e: DragEvent<HTMLDivElement>) => {
        e.preventDefault();
        e.stopPropagation();
        if (e.type === 'dragenter' || e.type === 'dragover') {
            setDragActive(true);
        } else if (e.type === 'dragleave') {
            setDragActive(false);
        }
    };

    const handleDrop = (e: DragEvent<HTMLDivElement>) => {
        e.preventDefault();
        e.stopPropagation();
        setDragActive(false);

        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            validateAndUpload(e.dataTransfer.files[0]);
        }
    };

    const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
        e.preventDefault();
        if (e.target.files && e.target.files[0]) {
            validateAndUpload(e.target.files[0]);
        }
    };

    const validateAndUpload = (file: File) => {
        const allowedTypes = ['application/pdf', 'text/plain', 'text/markdown', 'text/csv'];
        if (!allowedTypes.includes(file.type) && !file.name.endsWith('.md') && !file.name.endsWith('.csv')) {
            alert("File format not supported. Please use PDF, TXT, MD, or CSV.");
            return;
        }
        onUpload(file);
    };

    return (
        <div className="flex flex-col gap-4 bg-gray-900 p-4 rounded-xl border border-gray-800">
            <h2 className="text-lg font-semibold text-gray-100">Knowledge Base</h2>
            <p className="text-sm text-gray-400 mb-2">
                Add documents for analysis.
            </p>

            <div
                className={`relative flex flex-col items-center justify-center p-6 border-2 bourder-dashed rounded-lg transition-colors
                    ${dragActive ? 'border-blue-500 bg-blue-500/10' : 'border-gray-700 hover:border-gray-500 bg-gray-800/50'}
                    ${isUploading ? 'opacity-50 pointer-events-none' : 'cursor-pointer'}`}
                onDragEnter={handleDrag}
                onDragLeave={handleDrag}
                onDragOver={handleDrag}
                onDrop={handleDrop}
                onClick={() => inputRef.current?.click()}
            >
                <input
                    ref={inputRef}
                    type="file"
                    accept=".pdf,.txt,.md,.csv"
                    onChange={handleChange}
                    disabled={isUploading}
                    className="hidden"
                />

                <svg className="w-8 h-8 text-gray-400 mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
                </svg>
                <p className="text-sm text-gray-300 text-center">
                    <span className="font-semibold text-blue-400">Click here to pick</span> or drag a file.
                </p>
            </div>

            {ingestionState && (
                <div className="mt-4 flex flex-col gap-2">
                    <div className="flex justify-between text-xs font-medium">
                        <span className={ingestionState.step === 'error' ? 'text-red-400' : 'text.blue-400'}>
                            {ingestionState.status}
                        </span>
                        <span className="text-gray-400">{ingestionState.progress}%</span>
                    </div>
                    <div className="w-full bg-gray-700 rounded-full h-2 overflow-hidden">
                        <div 
                            className={`h-2 rounded-full transition-all duration-300 ease-out ${
                                ingestionState.step === 'error' ? 'bg-red-500' : 'bg-blue-500'
                            }`}
                            style={{width: `${ingestionState.progress}%`}}
                        />
                    </div>
                </div>
            )}
                
        </div>
    );
}