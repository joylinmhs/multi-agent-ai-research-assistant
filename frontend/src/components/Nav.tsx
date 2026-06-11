import React from 'react';

export default function Nav() {
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

        <div className="flex items-center gap-4">
          <a className="text-sm text-slate-300 hover:text-white" href="#upload">Upload</a>
          <a className="text-sm text-slate-300 hover:text-white" href="#ingest">Ingest</a>
          <a className="text-sm text-slate-300 hover:text-white" href="#chat">Chat</a>
        </div>
      </div>
    </nav>
  );
}
