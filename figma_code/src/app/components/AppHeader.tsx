import { Zap, Star, Award, ChevronUp, Bell, Settings } from "lucide-react";
import { MagicProgress } from "./ui/MagicCard";

interface AppHeaderProps {
  onNavigate: (screen: string) => void;
}

export function AppHeader({ onNavigate }: AppHeaderProps) {
  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-[#100d24] border-b border-[rgba(124,58,237,0.2)] px-6 h-16 flex items-center gap-6">
      {/* Logo + Nome */}
      <button
        onClick={() => onNavigate("home")}
        className="flex items-center gap-3 flex-shrink-0 hover:opacity-90 transition-opacity cursor-pointer"
      >
        <div className="w-9 h-9 rounded-lg bg-[#7c3aed] flex items-center justify-center shadow-[0_0_12px_rgba(124,58,237,0.5)]">
          <span className="text-xl">🧙</span>
        </div>
        <span
          className="text-lg text-white hidden sm:block"
          style={{ fontFamily: 'var(--font-display)', letterSpacing: '0.05em' }}
        >
          Sourcerer
        </span>
      </button>

      {/* XP e nível */}
      <div className="flex-1 max-w-xs hidden md:flex flex-col gap-0.5">
        <div className="flex items-center gap-2">
          <span className="text-xs text-[#8b7db8]" style={{ fontFamily: 'var(--font-body)' }}>
            Nível 7 — Aprendiz Arcano
          </span>
          <span className="text-xs text-[#d4a017] font-semibold" style={{ fontFamily: 'var(--font-body)' }}>
            3.240 / 5.000 XP
          </span>
        </div>
        <MagicProgress value={3240} max={5000} color="purple" size="xs" />
      </div>

      {/* Mana */}
      <div className="hidden md:flex items-center gap-1.5 px-3 py-1.5 bg-[#1a1438] rounded-lg border border-[rgba(6,182,212,0.2)]">
        <Zap size={14} className="text-[#06b6d4]" />
        <span className="text-sm text-[#67e8f9] font-semibold" style={{ fontFamily: 'var(--font-body)' }}>
          80 / 100
        </span>
        <span className="text-xs text-[#8b7db8]" style={{ fontFamily: 'var(--font-body)' }}>mana</span>
      </div>

      {/* Badges */}
      <div className="hidden lg:flex items-center gap-2">
        {[
          { icon: "⚡", label: "Velocista", color: "rgba(212,160,23,0.2)", border: "rgba(212,160,23,0.4)" },
          { icon: "🔮", label: "Explorador", color: "rgba(124,58,237,0.2)", border: "rgba(124,58,237,0.4)" },
          { icon: "🌟", label: "Dedicado", color: "rgba(6,182,212,0.2)", border: "rgba(6,182,212,0.4)" },
        ].map((b) => (
          <div
            key={b.label}
            title={b.label}
            className="w-8 h-8 rounded-full flex items-center justify-center text-base cursor-pointer hover:scale-110 transition-transform"
            style={{ background: b.color, border: `1px solid ${b.border}` }}
          >
            {b.icon}
          </div>
        ))}
      </div>

      <div className="ml-auto flex items-center gap-3">
        <button className="w-9 h-9 rounded-lg hover:bg-[#1e1540] transition-colors flex items-center justify-center cursor-pointer relative">
          <Bell size={18} className="text-[#8b7db8]" />
          <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-[#7c3aed] rounded-full" />
        </button>
        <button className="w-9 h-9 rounded-lg hover:bg-[#1e1540] transition-colors flex items-center justify-center cursor-pointer">
          <Settings size={18} className="text-[#8b7db8]" />
        </button>
        <div
          className="w-9 h-9 rounded-full bg-gradient-to-br from-[#7c3aed] to-[#4c1d95] flex items-center justify-center text-base cursor-pointer hover:ring-2 hover:ring-[#7c3aed] transition-all"
        >
          🧙
        </div>
      </div>
    </header>
  );
}
