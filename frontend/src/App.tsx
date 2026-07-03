import { useState, type ChangeEvent, type FormEvent } from 'react';
import {
  ArrowUpTrayIcon,
  CheckCircleIcon,
  ClipboardDocumentIcon,
  DocumentTextIcon,
  PaperAirplaneIcon,
  SparklesIcon,
} from '@heroicons/react/24/outline';
import Layout from './components/Layout';

const API_BASE = import.meta.env.VITE_API_BASE || '/api/v1';

type ChatResponse = { answer: string };
type SourceResponse = { document_id: string; filename?: string };
type SourceStatus = { kind: 'success' | 'error'; message: string; name?: string };
type BusyAction = 'file' | 'text' | 'chat' | null;

async function getErrorMessage(response: Response, fallback: string) {
  try {
    const body = (await response.json()) as { detail?: string };
    return body.detail || fallback;
  } catch {
    return fallback;
  }
}

function App() {
  const [mode, setMode] = useState<'upload' | 'direct'>('upload');
  const [uploadFile, setUploadFile] = useState<File | null>(null);
  const [sourceText, setSourceText] = useState('');
  const [sourceStatus, setSourceStatus] = useState<SourceStatus | null>(null);
  const [activeDocumentId, setActiveDocumentId] = useState<string | null>(null);
  const [query, setQuery] = useState('');
  const [chatResult, setChatResult] = useState<ChatResponse | null>(null);
  const [chatError, setChatError] = useState<string | null>(null);
  const [lastAnswer, setLastAnswer] = useState<string | null>(null);
  const [busyAction, setBusyAction] = useState<BusyAction>(null);

  const resetConversation = () => {
    setChatResult(null);
    setChatError(null);
    setLastAnswer(null);
  };

  const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0] ?? null;
    setUploadFile(file);
    setSourceStatus(null);
    setActiveDocumentId(null);
    resetConversation();
  };

  const handleUploadSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!uploadFile) return;

    setBusyAction('file');
    setSourceStatus(null);
    try {
      const formData = new FormData();
      formData.append('file', uploadFile);
      const response = await fetch(`${API_BASE}/documents/upload`, { method: 'POST', body: formData });
      if (!response.ok) throw new Error(await getErrorMessage(response, 'Could not add this document.'));

      const data = (await response.json()) as SourceResponse;
      setActiveDocumentId(data.document_id);
      setSourceStatus({ kind: 'success', message: 'Document ready for questions', name: uploadFile.name });
      resetConversation();
    } catch (error) {
      setSourceStatus({
        kind: 'error',
        message: error instanceof Error ? error.message : 'Could not add this document.',
      });
    } finally {
      setBusyAction(null);
    }
  };

  const handleTextSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!sourceText.trim()) {
      setSourceStatus({ kind: 'error', message: 'Paste some text before continuing.' });
      return;
    }

    setBusyAction('text');
    setSourceStatus(null);
    try {
      const response = await fetch(`${API_BASE}/documents/ingest`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content: sourceText, title: 'Pasted text' }),
      });
      if (!response.ok) throw new Error(await getErrorMessage(response, 'Could not add this text.'));

      const data = (await response.json()) as SourceResponse;
      setActiveDocumentId(data.document_id);
      setSourceStatus({ kind: 'success', message: 'Text ready for questions', name: 'Pasted text' });
      setSourceText('');
      resetConversation();
    } catch (error) {
      setSourceStatus({
        kind: 'error',
        message: error instanceof Error ? error.message : 'Could not add this text.',
      });
    } finally {
      setBusyAction(null);
    }
  };

  const handleQuerySubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setChatError(null);
    if (!query.trim()) {
      setChatError('Enter a question about your document.');
      return;
    }
    if (!activeDocumentId) {
      setChatError('Add a document or paste text before asking a question.');
      return;
    }

    setBusyAction('chat');
    setChatResult(null);
    try {
      const response = await fetch(`${API_BASE}/chat/query`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query,
          session_id: 'frontend-session',
          document_id: activeDocumentId,
          previous_answer: lastAnswer,
        }),
      });
      if (!response.ok) throw new Error(await getErrorMessage(response, 'Could not answer that question.'));

      const data = (await response.json()) as ChatResponse;
      setChatResult(data);
      setLastAnswer(data.answer);
    } catch (error) {
      setChatError(error instanceof Error ? error.message : 'Could not answer that question.');
    } finally {
      setBusyAction(null);
    }
  };

  return (
    <Layout>
      <section className="mb-8 overflow-hidden rounded-[2rem] border border-white/10 bg-slate-900/70 px-6 py-8 shadow-panel backdrop-blur sm:px-10 sm:py-10">
        <div className="max-w-3xl">
          <div className="mb-5 inline-flex items-center gap-2 rounded-full border border-cyan-400/20 bg-cyan-400/10 px-3 py-1.5 text-xs font-semibold uppercase tracking-[0.16em] text-cyan-300">
            <SparklesIcon className="h-4 w-4" />
            AI document workspace
          </div>
          <h1 className="text-3xl font-semibold tracking-tight text-white sm:text-5xl">
            Ask better questions of your documents.
          </h1>
          <p className="mt-4 max-w-2xl text-base leading-7 text-slate-400 sm:text-lg">
            Add a PDF, text file, or pasted passage and get focused answers from that source.
          </p>
        </div>
      </section>

      <div className="grid items-start gap-6 lg:grid-cols-[minmax(0,0.88fr)_minmax(0,1.12fr)]">
        <section className="rounded-[1.75rem] border border-white/10 bg-slate-900/75 p-5 shadow-panel sm:p-7">
          <div className="flex items-start gap-4">
            <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-cyan-400 text-sm font-bold text-slate-950">1</span>
            <div>
              <h2 className="text-xl font-semibold text-white">Add a source</h2>
              <p className="mt-1 text-sm leading-6 text-slate-400">Choose the material you want to explore.</p>
            </div>
          </div>

          <div className="mt-6 grid grid-cols-2 rounded-xl bg-slate-950/80 p-1" role="tablist" aria-label="Source type">
            <button
              type="button"
              role="tab"
              aria-selected={mode === 'upload'}
              onClick={() => { setMode('upload'); setSourceStatus(null); }}
              className={`flex items-center justify-center gap-2 rounded-lg px-3 py-2.5 text-sm font-medium transition ${mode === 'upload' ? 'bg-slate-800 text-white shadow-sm' : 'text-slate-400 hover:text-slate-200'}`}
            >
              <DocumentTextIcon className="h-4 w-4" /> File
            </button>
            <button
              type="button"
              role="tab"
              aria-selected={mode === 'direct'}
              onClick={() => { setMode('direct'); setSourceStatus(null); }}
              className={`flex items-center justify-center gap-2 rounded-lg px-3 py-2.5 text-sm font-medium transition ${mode === 'direct' ? 'bg-slate-800 text-white shadow-sm' : 'text-slate-400 hover:text-slate-200'}`}
            >
              <ClipboardDocumentIcon className="h-4 w-4" /> Paste text
            </button>
          </div>

          {mode === 'upload' ? (
            <form className="mt-5" onSubmit={handleUploadSubmit}>
              <label className="group flex min-h-44 cursor-pointer flex-col items-center justify-center rounded-2xl border border-dashed border-slate-700 bg-slate-950/50 px-5 py-7 text-center transition hover:border-cyan-400/60 hover:bg-cyan-400/[0.04]">
                <span className="flex h-12 w-12 items-center justify-center rounded-2xl bg-slate-800 text-cyan-300 transition group-hover:bg-cyan-400/10">
                  <ArrowUpTrayIcon className="h-6 w-6" />
                </span>
                <span className="mt-4 text-sm font-semibold text-slate-200">{uploadFile ? uploadFile.name : 'Choose a PDF or text file'}</span>
                <span className="mt-1 text-xs text-slate-500">PDF or TXT, up to 10 MB</span>
                <input type="file" accept="text/plain,application/pdf" onChange={handleFileChange} className="sr-only" />
              </label>
              <button type="submit" className="primary-button mt-4 w-full" disabled={busyAction !== null || !uploadFile}>
                {busyAction === 'file' ? 'Preparing document...' : 'Add document'}
              </button>
            </form>
          ) : (
            <form className="mt-5" onSubmit={handleTextSubmit}>
              <label htmlFor="source-text" className="mb-2 block text-sm font-medium text-slate-300">Source text</label>
              <textarea
                id="source-text"
                value={sourceText}
                onChange={(event) => setSourceText(event.target.value)}
                rows={7}
                className="field resize-y"
                placeholder="Paste an article, note, or passage here..."
              />
              <button type="submit" className="primary-button mt-4 w-full" disabled={busyAction !== null}>
                {busyAction === 'text' ? 'Preparing text...' : 'Add text'}
              </button>
            </form>
          )}

          {sourceStatus ? (
            <div className={`mt-4 rounded-xl border p-4 text-sm ${sourceStatus.kind === 'success' ? 'border-emerald-400/20 bg-emerald-400/[0.07] text-emerald-200' : 'border-rose-400/20 bg-rose-400/[0.07] text-rose-200'}`}>
              <div className="flex items-start gap-3">
                {sourceStatus.kind === 'success' ? <CheckCircleIcon className="mt-0.5 h-5 w-5 shrink-0" /> : null}
                <div>
                  <p className="font-medium">{sourceStatus.message}</p>
                  {sourceStatus.name ? <p className="mt-1 truncate text-xs opacity-70">{sourceStatus.name}</p> : null}
                </div>
              </div>
            </div>
          ) : null}
        </section>

        <section className="rounded-[1.75rem] border border-white/10 bg-slate-900/75 p-5 shadow-panel sm:p-7">
          <div className="flex items-start justify-between gap-4">
            <div className="flex items-start gap-4">
              <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-indigo-400 text-sm font-bold text-slate-950">2</span>
              <div>
                <h2 className="text-xl font-semibold text-white">Ask your document</h2>
                <p className="mt-1 text-sm leading-6 text-slate-400">Answers stay focused on your active source.</p>
              </div>
            </div>
            <span className={`hidden items-center gap-1.5 rounded-full px-2.5 py-1 text-xs font-medium sm:flex ${activeDocumentId ? 'bg-emerald-400/10 text-emerald-300' : 'bg-slate-800 text-slate-500'}`}>
              <span className={`h-1.5 w-1.5 rounded-full ${activeDocumentId ? 'bg-emerald-400' : 'bg-slate-600'}`} />
              {activeDocumentId ? 'Ready' : 'Waiting for source'}
            </span>
          </div>

          <form className="mt-6" onSubmit={handleQuerySubmit}>
            <label htmlFor="research-question" className="mb-2 block text-sm font-medium text-slate-300">Your question</label>
            <textarea
              id="research-question"
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              rows={5}
              className="field resize-none"
              placeholder={activeDocumentId ? 'What would you like to know?' : 'Add a source to begin...'}
            />
            <div className="mt-4 flex justify-end">
              <button type="submit" className="primary-button min-w-36 bg-indigo-400 hover:bg-indigo-300" disabled={busyAction !== null || !activeDocumentId}>
                {busyAction === 'chat' ? 'Finding answer...' : <><PaperAirplaneIcon className="h-4 w-4" /> Ask question</>}
              </button>
            </div>
          </form>

          {chatError ? <p className="mt-4 rounded-xl border border-rose-400/20 bg-rose-400/[0.07] p-4 text-sm text-rose-200">{chatError}</p> : null}

          {chatResult ? (
            <article className="mt-6 rounded-2xl border border-indigo-300/15 bg-gradient-to-br from-indigo-400/[0.08] to-cyan-400/[0.04] p-5 sm:p-6">
              <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-[0.14em] text-indigo-300">
                <SparklesIcon className="h-4 w-4" /> Answer
              </div>
              <p className="mt-4 text-[15px] leading-7 text-slate-100 sm:text-base">{chatResult.answer}</p>
            </article>
          ) : (
            <div className="mt-6 flex min-h-36 items-center justify-center rounded-2xl border border-dashed border-slate-800 bg-slate-950/30 p-6 text-center">
              <div>
                <SparklesIcon className="mx-auto h-6 w-6 text-slate-600" />
                <p className="mt-3 text-sm text-slate-500">Your answer will appear here.</p>
              </div>
            </div>
          )}
        </section>
      </div>
    </Layout>
  );
}

export default App;
