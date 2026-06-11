import React, { useState } from 'react';

export default function Nav() {
  const [open, setOpen] = useState(false);

  return (
    <nav className="w-full border-b border-slate-800 bg-slate-900/90">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-3">
        <div className="flex items-center gap-3">
          <div className="h-10 w-10 rounded-lg bg-cyan-500" />
          <div>
            <div className="text-lg font-semibold text-white">Research Assistant</div>
            <div className="text-xs text-slate-400">Multi-Agent RAG</div>
          </div>
        </div>

        <div className="hidden md:flex items-center gap-4">
          <a className="text-sm text-slate-300 hover:text-white" href="#upload">Upload</a>
          <a className="text-sm text-slate-300 hover:text-white" href="#ingest">Ingest</a>
          <a className="text-sm text-slate-300 hover:text-white" href="#chat">Chat</a>
        </div>

        <div className="md:hidden">
          <button
            aria-label="Toggle menu"
            onClick={() => setOpen((v) => !v)}
            className="inline-flex h-10 w-10 items-center justify-center rounded-lg bg-slate-800 text-slate-200"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              {open ? (
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              ) : (
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              )}
            </svg>
          </button>
        </div>
      </div>

      {/* Mobile menu */}
      {open ? (
        <div className="md:hidden border-t border-slate-800 bg-slate-900/95">
          <div className="mx-auto flex max-w-6xl flex-col gap-2 px-4 py-3">
            <a className="block rounded-lg px-3 py-2 text-sm text-slate-300 hover:bg-slate-800 hover:text-white" href="#upload" onClick={() => setOpen(false)}>Upload</a>
            <a className="block rounded-lg px-3 py-2 text-sm text-slate-300 hover:bg-slate-800 hover:text-white" href="#ingest" onClick={() => setOpen(false)}>Ingest</a>
            <a className="block rounded-lg px-3 py-2 text-sm text-slate-300 hover:bg-slate-800 hover:text-white" href="#chat" onClick={() => setOpen(false)}>Chat</a>
          </div>
        </div>
      ) : null}
    </nav>
  );
}
