import Navigation from "./Navigation";

export default function Layout({ title, children }: { children: React.ReactNode }) {
  return (
    <div className="flex h-screen bg-slate-950 text-slate-100">
      <aside className="w-64 border-r border-slate-800 bg-slate-950/80 backdrop-blur">
        <div className="px-6 py-4 text-lg font-semibold tracking-tight">
          BaselayerOS Inspector
        </div>
        <nav className="mt-4 space-y-2 text-sm">
          <a href="/">Home</a>
          <a href="/demo">Demo</a>
          <a href="/state">State</a>
          <a href="/audit">Audit</a>
          <a href="/envelopes">Envelopes</a>
          <a href="/invariants">Invariants</a>
          <a href="/modules">Modules</a>
          <a href="/summary">Summary</a>
        </nav>
      </aside>
      <main className="flex-1 overflow-y-auto">{children}</main>
    </div>
  );
}
