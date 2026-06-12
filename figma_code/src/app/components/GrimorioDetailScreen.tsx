import { ArrowLeft, Star, Zap, Lock, CheckCircle2, Circle, Clock, Trophy, ChevronRight, BookOpen } from "lucide-react";
import { AppHeader } from "./AppHeader";
import { MagicCard, MagicBadge, MagicProgress, MagicButton } from "./ui/MagicCard";

const FEITICOS = [
  {
    id: 1,
    title: "O que é um algoritmo?",
    desc: "Entenda como computadores seguem instruções passo a passo.",
    difficulty: "fácil",
    required: true,
    mana: 20,
    status: "concluido",
    badge: null,
    estimativa: "10 min",
  },
  {
    id: 2,
    title: "Sequências de passos",
    desc: "Aprenda a ordenar instruções para criar soluções corretas.",
    difficulty: "fácil",
    required: true,
    mana: 20,
    status: "concluido",
    badge: null,
    estimativa: "12 min",
  },
  {
    id: 3,
    title: "Seu primeiro feitiço",
    desc: "Monte um programa simples usando blocos de comando.",
    difficulty: "fácil",
    required: true,
    mana: 30,
    status: "concluido",
    badge: { label: "Iniciante Arcano", icon: "⭐" },
    estimativa: "15 min",
  },
  {
    id: 4,
    title: "Condicionais: se... então",
    desc: "Faça seu feitiço tomar decisões baseadas em condições.",
    difficulty: "médio",
    required: true,
    mana: 40,
    status: "em_progresso",
    badge: null,
    estimativa: "20 min",
  },
  {
    id: 5,
    title: "Laços simples",
    desc: "Repita ações com eficiência usando estruturas de repetição.",
    difficulty: "médio",
    required: true,
    mana: 40,
    status: "disponivel",
    badge: null,
    estimativa: "20 min",
  },
  {
    id: 6,
    title: "Depuração de feitiços",
    desc: "Encontre e corrija os erros nos seus programas como um mago experiente.",
    difficulty: "médio",
    required: false,
    mana: 35,
    status: "disponivel",
    badge: null,
    estimativa: "18 min",
  },
  {
    id: 7,
    title: "Desafio: Labirinto Arcano",
    desc: "Resolva o labirinto programando os movimentos do mago.",
    difficulty: "difícil",
    required: false,
    mana: 60,
    status: "bloqueado",
    badge: { label: "Explorador do Labirinto", icon: "🏆" },
    estimativa: "30 min",
  },
  {
    id: 8,
    title: "Missão Final: A Torre Sombria",
    desc: "Use tudo que aprendeu para superar o desafio final do grimório.",
    difficulty: "difícil",
    required: true,
    mana: 80,
    status: "bloqueado",
    badge: { label: "Mestre dos Algoritmos", icon: "🔮" },
    estimativa: "40 min",
  },
];

const DIFF_CONFIG: Record<string, { label: string; variant: "green" | "gold" | "red" }> = {
  "fácil":   { label: "Fácil",   variant: "green" },
  "médio":   { label: "Médio",   variant: "gold"  },
  "difícil": { label: "Difícil", variant: "red"   },
};

interface GrimorioDetailScreenProps {
  onNavigate: (screen: string) => void;
}

export function GrimorioDetailScreen({ onNavigate }: GrimorioDetailScreenProps) {
  const done = FEITICOS.filter((f) => f.status === "concluido").length;
  const total = FEITICOS.length;
  const pct = Math.round((done / total) * 100);
  const xpGanho = FEITICOS.filter((f) => f.status === "concluido").reduce((a, f) => a + f.mana, 0);
  const xpTotal = FEITICOS.reduce((a, f) => a + f.mana, 0);

  return (
    <div className="min-h-screen bg-[#0d0a1e]">
      <AppHeader onNavigate={onNavigate} />

      <div className="pt-16">
        {/* Hero do grimório */}
        <div className="relative bg-[#100d24] border-b border-[rgba(124,58,237,0.2)] overflow-hidden">
          {/* Decoração de fundo */}
          <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_70%_50%,rgba(124,58,237,0.12)_0%,transparent_65%)]" />
          <div className="absolute right-0 top-0 bottom-0 w-64 opacity-5 flex items-center justify-center text-[180px] select-none pointer-events-none">
            📖
          </div>

          <div className="relative z-10 max-w-5xl mx-auto px-6 py-8">
            {/* Breadcrumb */}
            <button
              onClick={() => onNavigate("home")}
              className="flex items-center gap-1.5 text-sm text-[#8b7db8] hover:text-[#c4b5fd] transition-colors mb-5 cursor-pointer group"
            >
              <ArrowLeft size={15} className="group-hover:-translate-x-0.5 transition-transform" />
              <span style={{ fontFamily: 'var(--font-body)' }}>Voltar aos grimórios</span>
            </button>

            <div className="flex items-start gap-5 flex-wrap">
              {/* Ícone */}
              <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-[rgba(124,58,237,0.3)] to-[rgba(76,29,149,0.4)] border border-[rgba(124,58,237,0.4)] flex items-center justify-center text-3xl flex-shrink-0 shadow-[0_0_20px_rgba(124,58,237,0.25)]">
                📖
              </div>

              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-3 flex-wrap mb-1">
                  <h1 className="text-2xl text-[#e8e0f8]" style={{ fontFamily: 'var(--font-display)' }}>
                    Fundamentos de Algoritmos
                  </h1>
                  <MagicBadge variant="purple" size="md">Obrigatório</MagicBadge>
                </div>
                <p className="text-[#8b7db8] text-sm mb-4 max-w-xl" style={{ fontFamily: 'var(--font-body)' }}>
                  Aprenda os blocos básicos do pensamento computacional: sequências, loops e condicionais. Domine os fundamentos para criar seus primeiros feitiços de programação.
                </p>

                {/* Métricas em linha */}
                <div className="flex items-center gap-5 flex-wrap text-sm">
                  <div className="flex items-center gap-1.5 text-[#c4b5fd]">
                    <BookOpen size={14} />
                    <span style={{ fontFamily: 'var(--font-body)' }}>{done}/{total} feitiços</span>
                  </div>
                  <div className="flex items-center gap-1.5 text-[#d4a017]">
                    <Star size={14} />
                    <span style={{ fontFamily: 'var(--font-body)' }}>{xpGanho}/{xpTotal} XP</span>
                  </div>
                  <div className="flex items-center gap-1.5 text-[#67e8f9]">
                    <Zap size={14} />
                    <span style={{ fontFamily: 'var(--font-body)' }}>~{Math.round(FEITICOS.reduce((a, f) => a + parseInt(f.estimativa), 0) / 60 * 10) / 10}h no total</span>
                  </div>
                  <div className="flex items-center gap-1.5 text-[#86efac]">
                    <Trophy size={14} />
                    <span style={{ fontFamily: 'var(--font-body)' }}>2 badges disponíveis</span>
                  </div>
                </div>
              </div>

              {/* Progresso circular e CTA */}
              <div className="flex flex-col items-end gap-3">
                <div className="text-right">
                  <div className="text-3xl font-bold text-[#e8e0f8]" style={{ fontFamily: 'var(--font-display)' }}>
                    {pct}%
                  </div>
                  <div className="text-xs text-[#8b7db8]" style={{ fontFamily: 'var(--font-body)' }}>concluído</div>
                </div>
                <div className="w-40">
                  <MagicProgress value={pct} color="purple" size="md" />
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Lista de feitiços */}
        <div className="max-w-5xl mx-auto px-6 py-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-base text-[#e8e0f8]" style={{ fontFamily: 'var(--font-display)' }}>
              Feitiços do Grimório
            </h2>
            <div className="flex items-center gap-2 text-xs text-[#8b7db8]" style={{ fontFamily: 'var(--font-body)' }}>
              <span className="flex items-center gap-1"><CheckCircle2 size={12} className="text-[#86efac]" /> Concluído</span>
              <span className="flex items-center gap-1"><Circle size={12} className="text-[#7c3aed]" /> Em progresso</span>
              <span className="flex items-center gap-1"><Lock size={12} className="text-[#4a3d7a]" /> Bloqueado</span>
            </div>
          </div>

          <div className="space-y-2">
            {FEITICOS.map((feitico, idx) => (
              <FeiticoRow
                key={feitico.id}
                feitico={feitico}
                index={idx + 1}
                onOpen={() => onNavigate("feitico")}
              />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

function FeiticoRow({
  feitico,
  index,
  onOpen,
}: {
  feitico: typeof FEITICOS[0];
  index: number;
  onOpen: () => void;
}) {
  const isBlocked = feitico.status === "bloqueado";
  const isDone = feitico.status === "concluido";
  const isProgress = feitico.status === "em_progresso";
  const diff = DIFF_CONFIG[feitico.difficulty];

  return (
    <div
      onClick={isBlocked ? undefined : onOpen}
      className={`group flex items-center gap-4 rounded-xl border px-4 py-3.5 transition-all duration-150 ${
        isBlocked
          ? "bg-[#0c0a1c] border-[rgba(74,61,122,0.2)] opacity-55 cursor-not-allowed"
          : isDone
          ? "bg-[#0f1e14] border-[rgba(34,197,94,0.2)] hover:border-[rgba(34,197,94,0.4)] cursor-pointer"
          : isProgress
          ? "bg-[rgba(124,58,237,0.08)] border-[rgba(124,58,237,0.35)] hover:border-[rgba(124,58,237,0.5)] cursor-pointer shadow-[0_0_12px_rgba(124,58,237,0.08)]"
          : "bg-[#16112e] border-[rgba(124,58,237,0.15)] hover:border-[rgba(124,58,237,0.35)] cursor-pointer hover:bg-[rgba(124,58,237,0.05)]"
      }`}
    >
      {/* Número / Status */}
      <div className="flex-shrink-0 w-8 h-8 rounded-lg flex items-center justify-center">
        {isDone ? (
          <CheckCircle2 size={20} className="text-[#22c55e]" />
        ) : isBlocked ? (
          <Lock size={16} className="text-[#4a3d7a]" />
        ) : isProgress ? (
          <div className="w-6 h-6 rounded-full border-2 border-[#7c3aed] flex items-center justify-center">
            <div className="w-2 h-2 rounded-full bg-[#7c3aed]" />
          </div>
        ) : (
          <span className="text-sm text-[#8b7db8] font-mono font-medium">{String(index).padStart(2, "0")}</span>
        )}
      </div>

      {/* Conteúdo principal */}
      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-2 mb-0.5 flex-wrap">
          <span
            className={`font-semibold text-sm ${isBlocked ? "text-[#4a3d7a]" : isDone ? "text-[#86efac]" : "text-[#e8e0f8]"}`}
            style={{ fontFamily: 'var(--font-body)' }}
          >
            {feitico.title}
          </span>
          {isProgress && (
            <MagicBadge variant="purple">Em andamento</MagicBadge>
          )}
          {feitico.badge && !isBlocked && (
            <span className="flex items-center gap-1 text-xs text-[#d4a017] bg-[rgba(212,160,23,0.1)] border border-[rgba(212,160,23,0.25)] px-2 py-0.5 rounded-full" style={{ fontFamily: 'var(--font-body)' }}>
              {feitico.badge.icon} {feitico.badge.label}
            </span>
          )}
        </div>
        <p className={`text-xs truncate ${isBlocked ? "text-[#2e2550]" : "text-[#8b7db8]"}`} style={{ fontFamily: 'var(--font-body)' }}>
          {feitico.desc}
        </p>
      </div>

      {/* Metadados */}
      <div className="flex items-center gap-3 flex-shrink-0">
        <MagicBadge variant={diff.variant}>{diff.label}</MagicBadge>

        <div className={`hidden sm:flex items-center gap-1 text-xs ${isBlocked ? "text-[#2e2550]" : "text-[#8b7db8]"}`} style={{ fontFamily: 'var(--font-body)' }}>
          <Clock size={11} />
          <span>{feitico.estimativa}</span>
        </div>

        <div className={`flex items-center gap-1 text-xs font-semibold ${isBlocked ? "text-[#2e2550]" : "text-[#67e8f9]"}`} style={{ fontFamily: 'var(--font-body)' }}>
          <Zap size={11} />
          <span>+{feitico.mana}</span>
        </div>

        <MagicBadge variant={feitico.required ? "purple" : "gray"}>
          {feitico.required ? "Obrigatório" : "Opcional"}
        </MagicBadge>

        {!isBlocked && (
          <ChevronRight
            size={16}
            className="text-[#4a3d7a] group-hover:text-[#a78bfa] transition-colors"
          />
        )}
      </div>
    </div>
  );
}
