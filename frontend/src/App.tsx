import { useState, useRef, useEffect } from "react";
import { MessageBubble } from "./components/MessageBubble";
import { ChatInput } from "./components/ChatInput";
import { FileUploader } from "./components/FileUploader";
import type { Message, IngestionState } from "./types";
import { streamChat, uploadFileStream } from "./services/api";

export default function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isChatting, setIsChatting] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const [ingestionState, setIngestionState] = useState<IngestionState | null>(null);
  const [isUploading, setIsUploading] = useState(false);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView( {behavior: 'smooth'} );
  }, [messages]);

  const handleSendMessage = async (text: string) => {
    if (!text.trim()) return;

    const userMessage: Message = { id: crypto.randomUUID(), role: 'user', content: text};
    setMessages((prev) => [...prev, userMessage]);
    setIsChatting(true);

    const assistantMessageId = crypto.randomUUID();
    setMessages((prev) => [
      ...prev,
      {id: assistantMessageId, role: 'assistant', content:''},
    ]);

    try {
      for await (const chunk of streamChat(text)) {
        setMessages((prev) => 
          prev.map((msg) =>
            msg.id === assistantMessageId
              ? {...msg, content: msg.content + chunk}
              : msg
          )
        );
      }
    } catch (error) {
      console.error('Error in chat:', error);
      setMessages((prev) => [
        ...prev,
        {id: crypto.randomUUID(), role: 'assistant', content: 'There was an error communicating with the server.'},
      ]);
    } finally {
      setIsChatting(false);
    }
  };

  const handleUpload = async (file: File) => {
    setIsUploading(true);
    setIngestionState({step: 'upload', status: 'Starting upload...', progress: 0});

    try {
      for await (const state of uploadFileStream(file)) {
        setIngestionState(state);
      }
    } catch (error) {
      console.error('Error during upload:', error);
      setIngestionState({step: 'error', status: 'Error during upload.', progress: 0});
    } finally {
      setIsUploading(false);
      setTimeout(() => {
        setIngestionState((current) => 
          current?.step === 'complete' ? null : current
        );
      }, 5000);
    }
  };

  return (
    <div className="flex h-screen bg-gray-950">
      <aside className="w-80 border-r border-gray-800 bg-gray-900/50 flex flex-col p-4">
        <div className="mb-8">
          <h1 className="text-2xl font-bold bg-linear-to-r from-blue-400 to-indigo-500 bg-clip-text text-transparent">
            Ragdoll
          </h1>
          <p className="text-sm text-gray-500 mt-1">AI Assistant with RAG Engine</p>
        </div>

        <FileUploader
          onUpload={handleUpload}
          ingestionState={ingestionState}
          isUploading={isUploading}
        />
      </aside>

      <main className="flex-1 flex flex-col">
        <div className="flex-1 overflow-y-auto p-6">
          {messages.length === 0 ? (
            <div className="h-full flex flex-col items-center justify-center text-gray-500 space-y-4">
              <svg className="w-16 h-16 opacity-20" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-1-13h2v6h-2zm0 8h2v2h-2z" />
              </svg>
              <p>Send a document or ask a question to get started.</p>
            </div>
          ) : (
            <div className="max-w-3xl mx-auto flex flex-col">
              {messages.map((msg) => (
                <MessageBubble key={msg.id} message={msg} />
              ))}
              <div ref={messagesEndRef} />
            </div>
          )}
        </div>

        <div className="p-4 bg-gray-900/80 border-t border-gray-800 backdrop-blur-sm">
          <ChatInput onSend={handleSendMessage} disabled={isChatting} />
        </div>
      </main>
    </div>
  );
}