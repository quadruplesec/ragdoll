export type Role = 'user' | 'assistant';

export interface Message {
    id: string;
    role: Role;
    content: string;
}

export type IngestionStep = 'idle' | 'upload' | 'parse' | 'chunk' | 'embed' | 'complete' | 'error';

export interface IngestionState {
    step: IngestionStep;
    status: string;
    progress: number;
}