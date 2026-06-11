import { useState, type ChangeEvent, type FormEvent } from 'react';

const API_BASE = import.meta.env.VITE_API_BASE || '/api/v1';

type ChatResponse = {
  answer: string;
  summary: string;
  sources: string[];
  confidence: number;
  session_id: string;
};

type UploadResponse = {
  filename: string;
  message: string;
  document_id: string;
  ingested: boolean;
};

type IngestResponse = {
  document_id: string;
  message: string;
};

function App() {
  const [query, setQuery] = useState('');
  const [chatResult, setChatResult] = useState<ChatResponse | null>(null);
  const [chatError, setChatError] = useState<string | null>(null);
  const [uploadFile, setUploadFile] = useState<File | null>(null);
  const [uploadStatus, setUploadStatus] = useState<UploadResponse | null>(null);
  const [ingestText, setIngestText] = useState('');
  const [ingestStatus, setIngestStatus] = useState<IngestResponse | null>(null);
  const [loading, setLoading] = useState(false);

  const handleQuerySubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setChatError(null);
    setChatResult(null);
    if (!query.trim()) {
      setChatError('Please enter a question.');
      return;
    }

    setLoading(true);
    try {
      const response = await fetch(`${API_BASE}/chat/query`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query, session_id: 'frontend-session', context: {} }),
      });

      if (!response.ok) {
        throw new Error(`Request failed with status ${response.status}`);
      }

      const data = (await response.json()) as ChatResponse;
      setChatResult(data);
    } catch (error) {
      setChatError(error instanceof Error ? error.message : String(error));
    } finally {
      setLoading(false);
    }
  };

  const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
    setUploadFile(event.target.files?.[0] ?? null);
  };

  const handleUploadSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!uploadFile) {
      setUploadStatus(null);
      return;
    }

    setLoading(true);
    setUploadStatus(null);
    try {
      const formData = new FormData();
      formData.append('file', uploadFile);

      const response = await fetch(`${API_BASE}/documents/upload`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const error = await response.text();
        throw new Error(error || `Upload failed with status ${response.status}`);
      }

      const data = (await response.json()) as UploadResponse;
      setUploadStatus(data);
    } catch (error) {
      setUploadStatus({ filename: uploadFile.name, message: error instanceof Error ? error.message : String(error), document_id: '', ingested: false });
    } finally {
      setLoading(false);
    }
  };

  const handleIngestSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setIngestStatus(null);

    if (!ingestText.trim()) {
      setIngestStatus({ document_id: '', message: 'Please provide text to ingest.' });
      return;
    }

    setLoading(true);
    try {
      const response = await fetch(`${API_BASE}/documents/ingest`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content: ingestText, title: 'Frontend ingest' }),
      });

      if (!response.ok) {
        const error = await response.text();
        throw new Error(error || `Ingest failed with status ${response.status}`);
      }

      const data = (await response.json()) as IngestResponse;
      setIngestStatus(data);
      setIngestText('');
    } catch (error) {
      setIngestStatus({ document_id: '', message: error instanceof Error ? error.message : String(error) });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 px-4 py-8">
      <div className="mx-auto max-w-6xl space-y-10">
        <header className="rounded-3xl border border-slate-800 bg-slate-900/80 p-8 shadow-panel">
          <h1 className="text-4xl font-semibold text-white">Multi-Agent AI Research Assistant</h1>
          <p className="mt-3 text-slate-400">Upload documents, ingest text, then ask questions against your Chroma-backed knowledge base.</p>
        </header>

        <section className="grid gap-8 lg:grid-cols-2">
          <article className="rounded-3xl border border-slate-800 bg-slate-900/80 p-6 shadow-panel">
            <h2 className="text-2xl font-semibold">Upload &amp; Ingest</h2>
            <p className="mt-2 text-slate-400">Upload a text or PDF file and ingest its content into the Chroma retriever.</p>

            <form className="mt-6 space-y-4" onSubmit={handleUploadSubmit}>
              <label className="block text-sm font-medium text-slate-200">Select a file</label>
              <input
                type="file"
                accept="text/plain,application/pdf"
                onChange={handleFileChange}
                className="block w-full rounded-2xl border border-slate-700 bg-slate-950 p-3 text-slate-100"
              />
              <button
                type="submit"
                className="inline-flex items-center justify-center rounded-2xl bg-cyan-500 px-5 py-3 text-sm font-semibold text-slate-950 transition hover:bg-cyan-400 disabled:cursor-not-allowed disabled:opacity-60"
                disabled={loading || !uploadFile}
              >
                Upload &amp; Ingest
              </button>
            </form>

            {uploadStatus ? (
              <div className="mt-5 rounded-2xl border border-slate-700 bg-slate-950/90 p-4 text-sm text-slate-200">
                <p className="font-medium">{uploadStatus.message}</p>
                <p className="mt-2 text-slate-500">File: {uploadStatus.filename}</p>
                <p className="text-slate-500">Ingested: {uploadStatus.ingested ? 'Yes' : 'No'}</p>
              </div>
            ) : null}
          </article>

          <article className="rounded-3xl border border-slate-800 bg-slate-900/80 p-6 shadow-panel">
            <h2 className="text-2xl font-semibold">Direct Text Ingestion</h2>
            <p className="mt-2 text-slate-400">Paste text here and ingest it directly into the retriever.</p>

            <form className="mt-6 space-y-4" onSubmit={handleIngestSubmit}>
              <textarea
                value={ingestText}
                onChange={(event) => setIngestText(event.target.value)}
                rows={6}
                className="w-full rounded-3xl border border-slate-700 bg-slate-950 p-4 text-slate-100 outline-none focus:border-cyan-400"
                placeholder="Paste text to ingest into the knowledge base..."
              />
              <button
                type="submit"
                className="inline-flex items-center justify-center rounded-2xl bg-cyan-500 px-5 py-3 text-sm font-semibold text-slate-950 transition hover:bg-cyan-400 disabled:cursor-not-allowed disabled:opacity-60"
                disabled={loading}
              >
                Ingest Text
              </button>
            </form>

            {ingestStatus ? (
              <div className="mt-5 rounded-2xl border border-slate-700 bg-slate-950/90 p-4 text-sm text-slate-200">
                <p className="font-medium">{ingestStatus.message}</p>
                {ingestStatus.document_id ? <p className="mt-2 text-slate-500">ID: {ingestStatus.document_id}</p> : null}
              </div>
            ) : null}
          </article>
        </section>

        <section className="rounded-3xl border border-slate-800 bg-slate-900/80 p-6 shadow-panel">
          <h2 className="text-2xl font-semibold">Research Chat</h2>
          <p className="mt-2 text-slate-400">Ask a question and retrieve answers from the ingested documents.</p>

          <form className="mt-6 space-y-4" onSubmit={handleQuerySubmit}>
            <textarea
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              rows={4}
              className="w-full rounded-3xl border border-slate-700 bg-slate-950 p-4 text-slate-100 outline-none focus:border-cyan-400"
              placeholder="Ask a question based on the ingested documents..."
            />
            <button
              type="submit"
              className="inline-flex items-center justify-center rounded-2xl bg-indigo-500 px-5 py-3 text-sm font-semibold text-white transition hover:bg-indigo-400 disabled:cursor-not-allowed disabled:opacity-60"
              disabled={loading}
            >
              Ask Research Agent
            </button>
          </form>

          {chatError ? (
            <p className="mt-4 rounded-2xl border border-red-600 bg-red-950/80 p-4 text-sm text-red-200">{chatError}</p>
          ) : null}

          {chatResult ? (
            <article className="mt-6 space-y-4 rounded-3xl border border-slate-700 bg-slate-950/90 p-5">
              <div>
                <h3 className="text-lg font-semibold text-white">Answer</h3>
                <p className="mt-2 text-slate-200">{chatResult.answer}</p>
              </div>
              <div>
                <h3 className="text-lg font-semibold text-white">Sources</h3>
                <ul className="mt-2 list-disc space-y-1 pl-5 text-slate-300">
                  {chatResult.sources.map((source, index) => (
                    <li key={index}>{source}</li>
                  ))}
                </ul>
              </div>
              <div className="grid gap-3 sm:grid-cols-2">
                <div className="rounded-2xl bg-slate-900 p-4 text-sm text-slate-400">
                  <p className="font-semibold text-slate-200">Summary</p>
                  <p className="mt-2">{chatResult.summary}</p>
                </div>
                <div className="rounded-2xl bg-slate-900 p-4 text-sm text-slate-400">
                  <p className="font-semibold text-slate-200">Confidence</p>
                  <p className="mt-2">{chatResult.confidence.toFixed(2)}</p>
                  <p className="mt-1 text-slate-500">Session: {chatResult.session_id}</p>
                </div>
              </div>
            </article>
          ) : null}
        </section>
      </div>
    </div>
  );
}

export default App;
