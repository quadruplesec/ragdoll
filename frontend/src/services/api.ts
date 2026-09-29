import { IngestionState } from "../types";

export async function* streamChat(query: string): AsyncGenerator<string, void, unknown> {
    const response = await fetch('/api/ask', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({query}),
    });

    if (!response.ok || !response.body) {
        throw new Error('Error communicating with server.');
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder('utf-8');

    while (true) {
        const {done, value} = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value, {stream: true});
        const lines = chunk.split('\n');

        for (const line of lines) {
            if (line.startsWith('data: ')) {
                const data = line.slice(6);
                if (data) yield data;
            }
        }
    }
}

export async function* uploadFileStream(file: File): AsyncGenerator<IngestionState, void, unknown> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch('/api/ingest/file', {
        method: 'POST',
        body: formData,
    });

    if (!response.ok || !response.body) {
        throw new Error('Error uploading file.');
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder('utf-8');

    while (true) {
        const {done, value} = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value, {stream: true});
        const lines = chunk.split('\n');

        for (const line of lines) {
            if (line.startsWith('data: ')) {
                try {
                    const data: IngestionState = JSON.parse(line.slice(6));
                    yield data;
                } catch (error) {
                    console.error('Error analyzing ingestion progress:', line, error); 
                }
            }
        }
    }
}