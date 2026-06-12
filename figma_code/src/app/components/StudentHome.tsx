import { BookOpen, Lock, CheckCircle2, Clock, ChevronRight, Flame, Star } from "lucide-react";
import { AppHeader } from "./AppHeader";
import { ProfileSidebar } from "./ProfileSidebar";
import { MagicCard, MagicBadge, MagicProgress, MagicButton } from "./ui/MagicCard";

const GRIMORIOS = [
  {
    id: 1,
    title: "Fundamentos de Algoritmos",
    description: "Aprenda os blocos básicos do pensamento computacional: sequências, loops e condicionais.",
    icon: "📖",
    progress: 75,
    totalSpells: 12,
    doneSpells: 9,
    status: "em_progresso",
    xpTotal: 480,
    xpGanho: 360,
    tags: ["Obrigatório"],
    color: "#7c3aed",
  },
  {
    id: 2,
    title: "Lógica Condicional",
    description: "Domine o poder das decisões: if/else, comparações e fluxos de controle.",
    icon: "🔀",
    progress: 33,
    totalSpells: 9,
    doneSpells: 3,
    status: "em_progresso",
    xpTotal: 360,
    xpGanho: 120,
    tags: ["Obrigatório"],
    color: "#06b6d4",
  },
  {
    id: 3,
    title: "Repetição e Laços",
    description: "Aprenda a fazer o computador repetir tarefas com maestria arcana.",
    icon: "🔄",
    progress: 0,
    totalSpells: 10,
    doneSpells: 0,
    status: "disponivel",
    xpTotal: 400,
    xpGanho: 0,
    tags: [],
    color: "#a855f7",
  },
  {
    id: 4,
    title: "Variáveis e Dados",
    description: "Descubra como guardar e manipular informações nos seus feitiços.",
    icon: "🧪",
    progress: 100,
    totalSpells: 8,
    doneSpells: 8,
    status: "concluido",
    xpTotal: 320,
    xpGanho: 320,
    tags: ["Concluído"],
    color: "#22c55e",
  },
  {
    id: 5,
    title: "Funções e Feitiços",
    description: "Crie seus próprios feitiços reutilizáveis com funções personalizadas.",
    icon: "✨",
    progress: 0,
    totalSpells: 14,
    doneSpells: 0,
    status: "bloqueado",
    xpTotal: 560,
    xpGanho: 0,
    tags: ["Bloqueado"],
    color: "#4a3d7a",
  },
  {
    id: 6,
    title: "Estruturas de Dados",
    description: "Listas, pilhas e filas: organize sua magia com eficiência.",
    icon: "📦",
    progress: 0,
    totalSpells: 11,
    doneSpells: 0,
    status: "bloqueado",
    xpTotal: 440,
    xpGanho: 0,
    tags: ["Bloqueado"],
    color: "#4a3d7a",
  },
];

interface StudentHomeProps {
  onNavigate: (screen: string) => void;
}

export function StudentHome({ onNavigate }: StudentHomeProps) {
  return (
    <div className="min-h-screen bg-[#0d0a1e]">
      <AppHeader onNavigate={onNavigate} />

      <div className="pt-16 flex min-h-[calc(100vh-4rem)]">
        {/* Sidebar */}
        <div className="hidden lg:flex w-64 flex-shrink-0 border-r border-[rgba(124,58,237,0.15)] flex-col">
          <div className="px-4 overflow-y-auto flex-1">
            <ProfileSidebar />
          </div>
        </div>

        {/* Conteúdo principal */}
        <main className="flex-1 min-w-0 px-6 py-6">
          {/* Saudação */}
          <div className="mb-6">
            <h1 className="text-2xl text-[#e8e0f8] mb-1" style={{ fontFamily: 'var(--font-display)' }}>
              Olá, Ana Beatriz! ✨
            </h1>
            <p className="text-[#8b7db8] text-sm" style={{ fontFamily: 'var(--font-body)' }}>
              Você tem <span className="text-[#c4b5fd] font-semibold">3 feitiços</span> pendentes. Continue sua jornada!
            </p>
          </div>

          {/* Barra de atividade diária */}
          <MagicCard className="mb-6 p-4 flex items-center gap-4">
            <div className="flex items-center gap-2">
              <Flame size={20} className="text-[#d4a017]" />
              <div>
                <p className="text-sm font-semibold text-[#e8e0f8]" style={{ fontFamily: 'var(--font-body)' }}>Sequência de 7 dias</p>
                <p className="text-xs text-[#8b7db8]" style={{ fontFamily: 'var(--font-body)' }}>Continue sua magia diária!</p>
              </div>
            </div>
            <div className="flex gap-1.5 mx-4">
              {["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"].map((d, i) => (
                <div key={d} className="flex flex-col items-center gap-1">
                  <div
                    className={`w-7 h-7 rounded-lg flex items-center justify-center text-xs ${
                      i < 7
                        ? i < 5
                          ? "bg-[#7c3aed] shadow-[0_0_8px_rgba(124,58,237,0.4)]"
                          : i === 5
                          ? "bg-[#d4a017] shadow-[0_0_8px_rgba(212,160,23,0.4)]"
                          : "bg-[#1e1540] border border-[rgba(124,58,237,0.2)]"
                        : "bg-[#1e1540] border border-[rgba(124,58,237,0.2)]"
                    }`}
                  >
                    {i < 5 ? "✓" : i === 5 ? "★" : "·"}
                  </div>
                  <span className="text-[10px] text-[#4a3d7a]" style={{ fontFamily: 'var(--font-body)' }}>{d}</span>
                </div>
              ))}
            </div>
            <div className="ml-auto text-right hidden sm:block">
              <p className="text-xs text-[#8b7db8]" style={{ fontFamily: 'var(--font-body)' }}>Mana de hoje</p>
              <p className="text-sm text-[#67e8f9] font-semibold" style={{ fontFamily: 'var(--font-body)' }}>+15 ⚡</p>
            </div>
          </MagicCard>

          {/* Grid de Grimórios */}
          <div className="mb-4 flex items-center justify-between">
            <h2 className="text-lg text-[#e8e0f8]" style={{ fontFamily: 'var(--font-display)' }}>
              Meus Grimórios
            </h2>
            <span className="text-sm text-[#8b7db8]" style={{ fontFamily: 'var(--font-body)' }}>
              {GRIMORIOS.filter((g) => g.status === "concluido").length} de {GRIMORIOS.length} concluídos
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
            {GRIMORIOS.map((g) => (
              <GrimorioCard key={g.id} grimorio={g} onOpen={() => onNavigate("grimorio")} />
            ))}
          </div>
        </main>
      </div>
    </div>
  );
}

function GrimorioCard({ grimorio, onOpen }: { grimorio: typeof GRIMORIOS[0]; onOpen: () => void }) {
  const isBlocked = grimorio.status === "bloqueado";
  const isDone = grimorio.status === "concluido";

  return (
    <div
      className={`relative rounded-xl border p-5 flex flex-col gap-4 transition-all duration-200 ${
        isBlocked
          ? "bg-[#0f0c22] border-[rgba(74,61,122,0.3)] opacity-60 cursor-not-allowed"
          : isDone
          ? "bg-[#0f1e14] border-[rgba(34,197,94,0.25)] hover:border-[rgba(34,197,94,0.45)] cursor-pointer"
          : "bg-[#16112e] border-[rgba(124,58,237,0.2)] hover:border-[rgba(124,58,237,0.45)] hover:shadow-[0_0_20px_rgba(124,58,237,0.12)] cursor-pointer"
      }`}
      onClick={isBlocked ? undefined : onOpen}
    >
      {/* Cabeçalho */}
      <div className="flex items-start gap-3">
        <div
          className="w-11 h-11 rounded-xl flex items-center justify-center text-2xl flex-shrink-0"
          style={{
            background: isBlocked
              ? "rgba(74,61,122,0.2)"
              : `${grimorio.color}22`,
            border: `1px solid ${isBlocked ? "rgba(74,61,122,0.3)" : grimorio.color + "44"}`,
          }}
        >
          {isBlocked ? <Lock size={18} className="text-[#4a3d7a]" /> : grimorio.icon}
        </div>
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 flex-wrap mb-0.5">
            <h3
              className={`truncate ${isBlocked ? "text-[#4a3d7a]" : "text-[#e8e0f8]"}`}
              style={{ fontFamily: 'var(--font-display)', fontSize: '0.85rem' }}
            >
              {grimorio.title}
            </h3>
          </div>
          <div className="flex items-center gap-1.5 flex-wrap">
            {isDone && <MagicBadge variant="green">✓ Concluído</MagicBadge>}
            {isBlocked && <MagicBadge variant="gray">🔒 Bloqueado</MagicBadge>}
            {grimorio.tags.includes("Obrigatório") && <MagicBadge variant="purple">Obrigatório</MagicBadge>}
          </div>
        </div>
      </div>

      {/* Descrição */}
      <p
        className={`text-xs leading-relaxed line-clamp-2 ${isBlocked ? "text-[#3a2d5a]" : "text-[#8b7db8]"}`}
        style={{ fontFamily: 'var(--font-body)' }}
      >
        {grimorio.description}
      </p>

      {/* Progresso */}
      <div className="space-y-2">
        <MagicProgress
          value={grimorio.progress}
          color={isDone ? "green" : "purple"}
          showLabel
          label={`${grimorio.doneSpells}/${grimorio.totalSpells} feitiços`}
          size="sm"
        />
      </div>

      {/* Rodapé */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-1 text-xs text-[#d4a017]" style={{ fontFamily: 'var(--font-body)' }}>
          <Star size={12} />
          <span>{grimorio.xpGanho} / {grimorio.xpTotal} XP</span>
        </div>
        {!isBlocked && (
          <button
            className={`flex items-center gap-1 text-xs font-semibold transition-colors cursor-pointer ${
              isDone ? "text-[#86efac]" : "text-[#a78bfa] hover:text-[#c4b5fd]"
            }`}
            style={{ fontFamily: 'var(--font-body)' }}
          >
            {isDone ? (
              <>
                <CheckCircle2 size={14} />
                Rever
              </>
            ) : grimorio.progress > 0 ? (
              <>
                Continuar
                <ChevronRight size={14} />
              </>
            ) : (
              <>
                Começar
                <ChevronRight size={14} />
              </>
            )}
          </button>
        )}
      </div>
    </div>
  );
}
