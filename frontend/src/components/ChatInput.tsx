import { useState } from "react";
import type { KeyboardEvent } from "react";

interface ChatInputProps {
    onSend: (message: string) => void;
    disabled: boolean;
}

export function ChatInput( {onSend, disabled}: ChatInputProps ) {
    const [text, setText] = useState('');

    const handleSend = () => {
        if (text.trim() && !disabled) {
            onSend(text.trim());
            setText('');
        }
    };

    const handleKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };

    return (
        <div className="flex items-center gap-2 bg-gray-900 p-2 rounded-xl shadow-inner border border-gray-800">
            <input
                type="text"
                value={text}
                onChange={(e) => setText(e.target.value)}
                onKeyDown={handleKeyDown}
                disabled={disabled}
                placeholder={disabled ? "Waiting for response..." : "Ask a question..."}
                className="flex-1 bg-transparent px-4 py-2 text-gray-100 focus:outline-none disabled:opacity-50"
            />
            <button
                onClick={handleSend}
                disabled={disabled || !text.trim()}
                className="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
                Send
            </button>
        </div>
    );
}