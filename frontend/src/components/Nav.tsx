import { BeakerIcon } from '@heroicons/react/24/outline';

export default function Nav() {
  return (
    <nav className="sticky top-0 z-20 w-full border-b border-white/10 bg-slate-950/80 backdrop-blur-xl">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-3.5 sm:px-6 lg:px-8">
        <div className="flex items-center gap-3">
          <span className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-cyan-300 to-indigo-400 text-slate-950 shadow-lg shadow-cyan-950/30">
            <BeakerIcon className="h-5 w-5" />
          </span>
          <div>
            <div className="text-sm font-semibold tracking-wide text-white sm:text-base">Research Assistant</div>
            <div className="text-xs text-slate-500">Document intelligence</div>
          </div>
        </div>
        <div className="flex items-center gap-2 rounded-full border border-white/10 bg-white/[0.04] px-3 py-1.5 text-xs font-medium text-slate-400">
          <span className="h-1.5 w-1.5 rounded-full bg-emerald-400 shadow-[0_0_8px_rgba(52,211,153,0.8)]" />
          Local workspace
        </div>
      </div>
    </nav>
  );
}
