import type { Message } from "../types";

interface MesssageBubbleProps {
    message: Message;
}

export function MessageBubble( {message}: MesssageBubbleProps ) {
    const isUser = message.role === 'user';

    return (
        <div className={`flex w-full mb-4 ${isUser ? 'justify-end' : 'justify-start'}`}>
            <div
                className={`max-w-[75%] px-4 py-3 rounded-2xl ${
                    isUser
                        ? 'bg-blue-600 text-white rounded-br-none'
                        : 'bg-gray-800 text-gray-100 rounded-bl-none shadow-md'
                }`}
            >
                <p className="whitespace-pre-wrap text-sm leading-relaxed">
                    {message.content}
                </p>
            </div>
        </div>
    );
}