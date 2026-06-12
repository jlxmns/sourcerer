import {
  ArrowLeft, Users, Zap, Star, Trophy, BookOpen,
  TrendingUp, Shield, Swords, ChevronRight,
  CheckCircle2, AlertTriangle, MinusCircle,
} from "lucide-react";
import { MagicBadge, MagicButton, MagicProgress } from "../ui/MagicCard";

const ALUNOS_GUILDA = [
  { id: 1,  nome: "Vitória Mendes",   nivel: 9, mana: 980, grimorios: 5, feiticos: 48, progresso: 95, status: "avancando", badge: "🏆"  },
  { id: 2,  nome: "Lucas Pereira",    nivel: 8, mana: 840, grimorios: 4, feiticos: 42, progresso: 88, status: "avancando", badge: "⚡"  },
  { id: 3,  nome: "Mariana Lima",     nivel: 8, mana: 810, grimorios: 4, feiticos: 40, progresso: 84, status: "avancando", badge: "🔮"  },
  { id: 4,  nome: "Felipe Costa",     nivel: 7, mana: 710, grimorios: 4, feiticos: 36, progresso: 79, status: "avancando", badge: null   },
  { id: 5,  nome: "Beatriz Alves",    nivel: 6, mana: 590, grimorios: 3, feiticos: 30, progresso: 68, status: "avancando", badge: null   },
  { id: 6,  nome: "Diego Martins",    nivel: 6, mana: 540, grimorios: 3, feiticos: 27, progresso: 60, status: "avancando", badge: null   },
  { id: 7,  nome: "Júlia Ferreira",   nivel: 5, mana: 410, grimorios: 2, feiticos: 19, progresso: 43, status: "risco",     badge: null   },
  { id: 8,  nome: "Henrique Duarte",  nivel: 4, mana: 280, grimorios: 2, feiticos: 14, progresso: 32, status: "risco",     badge: null   },
  { id: 9,  nome: "Sophia Ramos",     nivel: 3, mana: 160, grimorios: 1, feiticos:  8, progresso: 17, status: "inativo",   badge: null   },
];

const STATUS_CONFIG: Record<string, { label: string; variant: "green" | "gold" | "red" | "gray" }> = {
  avancando: { label: "Avançando",     variant: "green" },
  risco:     { label: "Em risco",      variant: "red"   },
  inativo:   { label: "Sem atividade", variant: "gray"  },
};

interface TeacherGuildDetailProps {
  onNavigate: (screen: string) => void;
}

export function TeacherGuildDetail({ onNavigate }: TeacherGuildDetailProps) {
  const totalMana   = ALUNOS_GUILDA.reduce((s, a) => s + a.mana, 0);
  const totalFeit   = ALUNOS_GUILDA.reduce((s, a) => s + a.feiticos, 0);
  const totalGrim   = ALUNOS_GUILDA.reduce((s, a) => s + a.grimorios, 0);
  const nivelMedio  = Math.round(ALUNOS_GUILDA.reduce((s, a) => s + a.nivel, 0) / ALUNOS_GUILDA.length);
  const progMedio   = Math.round(ALUNOS_GUILDA.reduce((s, a) => s + a.progresso, 0) / ALUNOS_GUILDA.length);

  return (
    <div className="p-6 space-y-6">

      {/* Breadcrumb */}
      <button
        onClick={() => onNavigate("dashboard")}
        className="flex items-center gap-1.5 text-sm text-[#8b7db8] hover:text-[#c4b5fd] transition-colors cursor-pointer group"
      >
        <ArrowLeft size={14} className="group-hover:-translate-x-0.5 transition-transform" />
        <span style={{ fontFamily: "var(--font-body)" }}>Voltar ao Dashboard</span>
      </button>

      {/* Hero da guilda */}
      <div className="rounded-xl border border-[rgba(6,182,212,0.25)] bg-[#16112e] overflow-hidden">
        <div className="relative p-6">
          <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_80%_50%,rgba(6,182,212,0.07)_0%,transparent_60%)]" />
          <div className="absolute right-6 top-1/2 -translate-y-1/2 text-[80px] opacity-[0.06] select-none pointer-events-none">⚔️</div>

          <div className="relative z-10 flex items-start gap-5 flex-wrap">
            {/* Ícone */}
            <div className="w-14 h-14 rounded-xl bg-[rgba(6,182,212,0.12)] border border-[rgba(6,182,212,0.3)] flex items-center justify-center text-3xl flex-shrink-0">
              ⚔️
            </div>

            {/* Info principal */}
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-3 flex-wrap mb-1">
                <h1 className="text-xl text-[#e8e0f8]" style={{ fontFamily: "var(--font-display)" }}>
                  Corvinal
                </h1>
                <MagicBadge variant="cyan" size="md">22 alunos</MagicBadge>
                <MagicBadge variant="purple" size="md">Nível médio {nivelMedio}</MagicBadge>
              </div>
              <p className="text-xs text-[#8b7db8] mb-4" style={{ fontFamily: "var(--font-body)" }}>
                Responsável: Profa. Camila Ramos · Ano letivo 2025 · EMEF Monteiro Lobato
              </p>
              <div className="flex items-center gap-5 flex-wrap text-xs">
                {[
                  { icon: Zap,       val: `${(totalMana/1000).toFixed(1)}k`, label: "mana total",      color: "text-[#67e8f9]" },
                  { icon: BookOpen,  val: totalGrim,                          label: "grimórios",        color: "text-[#c4b5fd]" },
                  { icon: Star,      val: totalFeit,                          label: "feitiços",         color: "text-[#d4a017]" },
                  { icon: TrendingUp,val: `${progMedio}%`,                   label: "progresso médio",  color: "text-[#86efac]" },
                ].map(({ icon: Icon, val, label, color }) => (
                  <div key={label} className={`flex items-center gap-1.5 ${color}`} style={{ fontFamily: "var(--font-body)" }}>
                    <Icon size={13} />
                    <span className="font-semibold">{val}</span>
                    <span className="text-[#8b7db8]">{label}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Ações */}
            <div className="flex items-center gap-2 flex-shrink-0">
              <MagicButton variant="secondary" size="sm">
                <Shield size={13} />
                Editar guilda
              </MagicButton>
              <MagicButton variant="primary" size="sm" onClick={() => onNavigate("teacher-progresso")}>
                <TrendingUp size={13} />
                Ver progresso
              </MagicButton>
            </div>
          </div>
        </div>
      </div>

      {/* Linha com ranking + inimigo coletivo */}
      <div className="grid grid-cols-1 lg:grid-cols-[1fr_300px] gap-5">

        {/* Ranking por mana */}
        <div className="rounded-xl border border-[rgba(124,58,237,0.18)] bg-[#16112e] overflow-hidden">
          <div className="px-5 py-3.5 border-b border-[rgba(124,58,237,0.12)] flex items-center gap-2">
            <Trophy size={14} className="text-[#d4a017]" />
            <span className="text-xs font-semibold text-[#e8e0f8]" style={{ fontFamily: "var(--font-display)", fontSize: "0.78rem" }}>
              Ranking interno — por Mana
            </span>
          </div>
          <div className="divide-y divide-[rgba(124,58,237,0.08)]">
            {[...ALUNOS_GUILDA]
              .sort((a, b) => b.mana - a.mana)
              .slice(0, 5)
              .map((a, i) => (
                <div key={a.id} className="flex items-center gap-3 px-5 py-3 hover:bg-[rgba(124,58,237,0.04)] transition-colors">
                  <span
                    className="w-6 text-center text-xs font-bold flex-shrink-0"
                    style={{ fontFamily: "var(--font-mono)", color: i === 0 ? "#d4a017" : i === 1 ? "#9ca3af" : i === 2 ? "#b87333" : "#4a3d7a" }}
                  >
                    {i === 0 ? "🥇" : i === 1 ? "🥈" : i === 2 ? "🥉" : `#${i + 1}`}
                  </span>
                  <div className="w-7 h-7 rounded-full bg-gradient-to-br from-[#7c3aed] to-[#4c1d95] flex items-center justify-center text-xs flex-shrink-0">
                    {a.nome[0]}
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm text-[#e8e0f8] truncate" style={{ fontFamily: "var(--font-body)" }}>{a.nome}</p>
                    <div className="flex items-center gap-2 mt-0.5">
                      <MagicProgress value={a.progresso} color="purple" size="xs" />
                      <span className="text-[10px] text-[#8b7db8] flex-shrink-0" style={{ fontFamily: "var(--font-mono)" }}>{a.progresso}%</span>
                    </div>
                  </div>
                  <div className="flex items-center gap-1.5 flex-shrink-0">
                    {a.badge && <span className="text-base">{a.badge}</span>}
                    <div className="text-right">
                      <p className="text-sm font-semibold text-[#67e8f9]" style={{ fontFamily: "var(--font-mono)" }}>{a.mana}</p>
                      <p className="text-[9px] text-[#4a3d7a]" style={{ fontFamily: "var(--font-body)" }}>mana</p>
                    </div>
                  </div>
                </div>
              ))}
          </div>
        </div>

        {/* Inimigo coletivo */}
        <div className="rounded-xl border border-[rgba(212,160,23,0.25)] bg-[#16112e] p-5 flex flex-col gap-4">
          <div className="flex items-center gap-2">
            <span className="text-2xl">🐉</span>
            <div>
              <p className="text-sm font-semibold text-[#f0c040]" style={{ fontFamily: "var(--font-display)", fontSize: "0.82rem" }}>
                Inimigo da Guilda
              </p>
              <p className="text-xs text-[#8b7db8]" style={{ fontFamily: "var(--font-body)" }}>
                Dragão de Gelo — Semana 23
              </p>
            </div>
          </div>

          <div className="space-y-2">
            <MagicProgress value={63} color="gold" showLabel label="Dano total acumulado" size="md" />
            <p className="text-xs text-[#8b7db8]" style={{ fontFamily: "var(--font-body)" }}>
              <span className="text-[#f0c040] font-semibold">19 alunos</span> contribuíram · 3 restantes
            </p>
          </div>

          {/* Contribuições recentes */}
          <div className="space-y-1.5">
            <p className="text-[10px] uppercase tracking-wider text-[#4a3d7a]" style={{ fontFamily: "var(--font-mono)" }}>
              Contribuições recentes
            </p>
            {ALUNOS_GUILDA.slice(0, 4).map((a) => (
              <div key={a.id} className="flex items-center justify-between text-xs" style={{ fontFamily: "var(--font-body)" }}>
                <span className="text-[#8b7db8] truncate">{a.nome}</span>
                <span className="text-[#d4a017] font-semibold flex-shrink-0">+{Math.round(a.mana * 0.05)} dano</span>
              </div>
            ))}
          </div>

          <div className="pt-2 border-t border-[rgba(212,160,23,0.15)]">
            <p className="text-xs text-[#8b7db8]" style={{ fontFamily: "var(--font-body)" }}>
              Prazo para derrotar: <span className="text-[#f0c040] font-semibold">6 dias</span>
            </p>
          </div>
        </div>
      </div>

      {/* Lista completa de alunos */}
      <div className="rounded-xl border border-[rgba(124,58,237,0.18)] bg-[#16112e] overflow-hidden">
        <div className="px-5 py-3.5 border-b border-[rgba(124,58,237,0.12)] flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Users size={14} className="text-[#7c3aed]" />
            <span className="text-xs font-semibold text-[#e8e0f8]" style={{ fontFamily: "var(--font-display)", fontSize: "0.78rem" }}>
              Todos os alunos da guilda
            </span>
          </div>
          <span className="text-xs text-[#8b7db8]" style={{ fontFamily: "var(--font-body)" }}>
            {ALUNOS_GUILDA.length} alunos
          </span>
        </div>

        {/* Header da tabela */}
        <div
          className="grid px-5 py-2 text-[10px] uppercase tracking-wider text-[#4a3d7a] border-b border-[rgba(124,58,237,0.08)]"
          style={{ gridTemplateColumns: "2fr 60px 80px 80px 80px 120px 110px", fontFamily: "var(--font-mono)" }}
        >
          <span>Aluno</span>
          <span>Nível</span>
          <span>Mana</span>
          <span>Grimórios</span>
          <span>Feitiços</span>
          <span>Progresso</span>
          <span>Status</span>
        </div>

        <div className="divide-y divide-[rgba(124,58,237,0.07)]">
          {ALUNOS_GUILDA.map((a) => {
            const st = STATUS_CONFIG[a.status];
            return (
              <div
                key={a.id}
                className="grid items-center px-5 py-3 hover:bg-[rgba(124,58,237,0.04)] transition-colors cursor-pointer"
                style={{ gridTemplateColumns: "2fr 60px 80px 80px 80px 120px 110px" }}
              >
                <div className="flex items-center gap-2.5 min-w-0">
                  <div className="w-7 h-7 rounded-full bg-gradient-to-br from-[#7c3aed] to-[#4c1d95] flex items-center justify-center text-xs flex-shrink-0">
                    {a.nome[0]}
                  </div>
                  <div className="min-w-0">
                    <p className="text-sm text-[#e8e0f8] truncate" style={{ fontFamily: "var(--font-body)" }}>{a.nome}</p>
                    {a.badge && <span className="text-[10px] text-[#d4a017]">{a.badge} Badge</span>}
                  </div>
                </div>
                <span className="text-xs text-[#c4b5fd] font-semibold" style={{ fontFamily: "var(--font-mono)" }}>{a.nivel}</span>
                <span className="text-xs text-[#67e8f9]" style={{ fontFamily: "var(--font-mono)" }}>{a.mana}</span>
                <span className="text-xs text-[#8b7db8]" style={{ fontFamily: "var(--font-mono)" }}>{a.grimorios}</span>
                <span className="text-xs text-[#8b7db8]" style={{ fontFamily: "var(--font-mono)" }}>{a.feiticos}</span>
                <div className="pr-4">
                  <MagicProgress value={a.progresso} color={a.progresso >= 70 ? "purple" : a.progresso >= 40 ? "gold" : "cyan"} size="xs" showLabel />
                </div>
                <MagicBadge variant={st.variant}>{st.label}</MagicBadge>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
