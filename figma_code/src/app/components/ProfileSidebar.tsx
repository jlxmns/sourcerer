import { Zap, Trophy, Star, Users, ChevronRight } from "lucide-react";
import { MagicCard, MagicBadge, MagicProgress } from "./ui/MagicCard";

const LEADERBOARD = [
  { rank: 1, name: "Vitória M.", xp: 5200, avatar: "🧝", isMe: false },
  { rank: 2, name: "Lucas P.", xp: 4800, avatar: "🧙", isMe: false },
  { rank: 3, name: "Ana Beatriz", xp: 4350, avatar: "🧚", isMe: true },
  { rank: 4, name: "Rafael T.", xp: 3900, avatar: "🧌", isMe: false },
  { rank: 5, name: "Camila S.", xp: 3240, avatar: "🦸", isMe: false },
];

interface ProfileSidebarProps {
  noClass?: boolean;
}

export function ProfileSidebar({ noClass = false }: ProfileSidebarProps) {
  return (
    <aside className="flex flex-col gap-3 pt-4 pb-6 w-full">
      {/* Card de perfil */}
      <MagicCard glow className="p-4">
        <div className="flex flex-col items-center gap-2.5 text-center">
          <div className="relative">
            <div className="w-14 h-14 rounded-full bg-gradient-to-br from-[#7c3aed] to-[#4c1d95] flex items-center justify-center text-2xl shadow-[0_0_16px_rgba(124,58,237,0.4)]">
              🧙
            </div>
            <div className="absolute -bottom-1 -right-1 w-5 h-5 bg-[#d4a017] rounded-full flex items-center justify-center text-[10px] font-bold text-[#0d0a1e]"
              style={{ fontFamily: 'var(--font-body)' }}>
              7
            </div>
          </div>
          <div>
            <p className="text-[#e8e0f8] font-semibold" style={{ fontFamily: 'var(--font-display)', fontSize: '0.85rem' }}>
              Ana Beatriz
            </p>
            <p className="text-xs text-[#8b7db8] mt-0.5" style={{ fontFamily: 'var(--font-body)' }}>
              {noClass ? "Sem turma" : "Turma 8ºA — Grifinória"}
            </p>
          </div>

          <div className="w-full space-y-1.5">
            <MagicProgress value={3240} max={5000} color="purple" label="XP" showLabel size="sm" />
            <div className="flex items-center justify-between text-xs" style={{ fontFamily: 'var(--font-body)' }}>
              <div className="flex items-center gap-1 text-[#67e8f9]">
                <Zap size={11} />
                <span>80 mana</span>
              </div>
              <div className="flex items-center gap-1 text-[#d4a017]">
                <Star size={11} />
                <span>Nível 7</span>
              </div>
            </div>
          </div>

          {/* Badges */}
          <div className="flex flex-wrap gap-1 justify-center">
            {["⚡ Velocista", "🔮 Explorador", "🌟 Dedicado"].map((b) => (
              <MagicBadge key={b} variant="purple">{b}</MagicBadge>
            ))}
          </div>
        </div>
      </MagicCard>

      {/* Leaderboard */}
      {!noClass && (
        <MagicCard className="p-4">
          <div className="flex items-center gap-2 mb-3">
            <Trophy size={15} className="text-[#d4a017]" />
            <span className="text-sm font-semibold text-[#e8e0f8]" style={{ fontFamily: 'var(--font-display)', fontSize: '0.8rem' }}>
              Ranking da Guilda
            </span>
          </div>
          <div className="space-y-2">
            {LEADERBOARD.map((p) => (
              <div
                key={p.rank}
                className={`flex items-center gap-2.5 px-2 py-1.5 rounded-lg transition-colors ${
                  p.isMe
                    ? "bg-[rgba(124,58,237,0.2)] border border-[rgba(124,58,237,0.3)]"
                    : "hover:bg-[#1e1540]"
                }`}
              >
                <span
                  className={`w-5 text-center text-xs font-bold ${
                    p.rank === 1 ? "text-[#d4a017]" : p.rank === 2 ? "text-[#9ca3af]" : p.rank === 3 ? "text-[#b87333]" : "text-[#8b7db8]"
                  }`}
                  style={{ fontFamily: 'var(--font-mono)' }}
                >
                  {p.rank === 1 ? "🥇" : p.rank === 2 ? "🥈" : p.rank === 3 ? "🥉" : `#${p.rank}`}
                </span>
                <span className="text-base">{p.avatar}</span>
                <span className="flex-1 text-xs text-[#e8e0f8] truncate" style={{ fontFamily: 'var(--font-body)' }}>
                  {p.isMe ? <strong>{p.name} (você)</strong> : p.name}
                </span>
                <span className="text-xs text-[#d4a017] font-semibold" style={{ fontFamily: 'var(--font-mono)' }}>
                  {p.xp.toLocaleString('pt-BR')}
                </span>
              </div>
            ))}
          </div>
        </MagicCard>
      )}

      {/* Progresso coletivo */}
      {!noClass && (
        <MagicCard gold className="p-4">
          <div className="flex items-center gap-2 mb-2">
            <span className="text-lg">🐉</span>
            <span className="text-sm font-semibold text-[#f0c040]" style={{ fontFamily: 'var(--font-display)', fontSize: '0.8rem' }}>
              Inimigo da Guilda
            </span>
          </div>
          <p className="text-xs text-[#8b7db8] mb-2" style={{ fontFamily: 'var(--font-body)' }}>
            Dragão das Sombras — derrotem juntos!
          </p>
          <MagicProgress value={68} color="gold" showLabel label="Vida do inimigo" size="sm" />
          <p className="text-xs text-[#8b7db8] mt-2" style={{ fontFamily: 'var(--font-body)' }}>
            <span className="text-[#f0c040] font-semibold">23 alunos</span> contribuíram esta semana
          </p>
        </MagicCard>
      )}
    </aside>
  );
}
