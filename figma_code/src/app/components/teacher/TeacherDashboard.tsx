import {
  Users, BookOpen, Zap, Award, Swords, AlertTriangle,
  Plus, ArrowRight, TrendingUp, Clock, ChevronRight,
  CheckCircle2, Circle, MinusCircle,
} from "lucide-react";
import { MagicBadge, MagicButton, MagicProgress } from "../ui/MagicCard";

/* ─── Dados simulados ─── */
const METRICS = [
  { label: "Alunos ativos",       value: "87",  delta: "+3 esta semana", icon: Users,    color: "#7c3aed", bg: "rgba(124,58,237,0.12)"  },
  { label: "Guildas",             value: "4",   delta: "2 em andamento",  icon: Swords,   color: "#06b6d4", bg: "rgba(6,182,212,0.10)"   },
  { label: "Grimórios concluídos",value: "142", delta: "+18 esta semana", icon: BookOpen, color: "#a855f7", bg: "rgba(168,85,247,0.12)"  },
  { label: "Feitiços concluídos", value: "934", delta: "+76 esta semana", icon: Zap,      color: "#d4a017", bg: "rgba(212,160,23,0.12)"  },
  { label: "Badges conquistadas", value: "211", delta: "+22 esta semana", icon: Award,    color: "#22c55e", bg: "rgba(34,197,94,0.10)"   },
];

const GUILDAS = [
  { id: 1, name: "Grifinória",  alunos: 24, nivel_medio: 6, mana_total: 14280, grimorios: 68,  feiticos: 420, progresso: 72, cor: "#7c3aed" },
  { id: 2, name: "Corvinal",    alunos: 22, nivel_medio: 7, mana_total: 15840, grimorios: 74,  feiticos: 468, progresso: 81, cor: "#06b6d4" },
  { id: 3, name: "Lufa-Lufa",   alunos: 21, nivel_medio: 5, mana_total: 10920, grimorios: 52,  feiticos: 315, progresso: 58, cor: "#d4a017" },
  { id: 4, name: "Sonserina",   alunos: 20, nivel_medio: 6, mana_total: 12800, grimorios: 61,  feiticos: 380, progresso: 67, cor: "#a855f7" },
];

const ALUNOS = [
  { id: 1,  nome: "Vitória Mendes",   guilda: "Corvinal",   nivel: 9, mana: 980, grimorios: 5, feiticos: 48, progresso: 95, status: "avancando"  },
  { id: 2,  nome: "Lucas Pereira",    guilda: "Corvinal",   nivel: 8, mana: 840, grimorios: 4, feiticos: 42, progresso: 88, status: "avancando"  },
  { id: 3,  nome: "Ana Beatriz",      guilda: "Grifinória", nivel: 7, mana: 720, grimorios: 4, feiticos: 38, progresso: 76, status: "avancando"  },
  { id: 4,  nome: "Rafael Torres",    guilda: "Grifinória", nivel: 6, mana: 580, grimorios: 3, feiticos: 31, progresso: 65, status: "avancando"  },
  { id: 5,  nome: "Camila Souza",     guilda: "Lufa-Lufa",  nivel: 5, mana: 380, grimorios: 2, feiticos: 18, progresso: 40, status: "risco"      },
  { id: 6,  nome: "Pedro Alves",      guilda: "Sonserina",  nivel: 5, mana: 420, grimorios: 3, feiticos: 22, progresso: 48, status: "risco"      },
  { id: 7,  nome: "Isabela Castro",   guilda: "Lufa-Lufa",  nivel: 3, mana: 180, grimorios: 1, feiticos: 9,  progresso: 18, status: "inativo"    },
  { id: 8,  nome: "Gabriel Nunes",    guilda: "Sonserina",  nivel: 6, mana: 560, grimorios: 3, feiticos: 28, progresso: 59, status: "avancando"  },
];

const ALERTAS = [
  { tipo: "risco",    aluno: "Camila Souza",   msg: "Sem atividade há 5 dias",        guilda: "Lufa-Lufa"  },
  { tipo: "risco",    aluno: "Pedro Alves",    msg: "Progresso abaixo de 50%",        guilda: "Sonserina"  },
  { tipo: "inativo",  aluno: "Isabela Castro", msg: "Sem atividade há 12 dias",       guilda: "Lufa-Lufa"  },
  { tipo: "tarefa",   aluno: null,             msg: "4 feitiços aguardam revisão",    guilda: null         },
  { tipo: "tarefa",   aluno: null,             msg: "Grimório novo disponível para publicar", guilda: null  },
];

const STATUS_CONFIG: Record<string, { label: string; variant: "green" | "gold" | "red" | "gray"; icon: typeof CheckCircle2 }> = {
  avancando: { label: "Avançando",     variant: "green", icon: CheckCircle2  },
  risco:     { label: "Em risco",      variant: "red",   icon: AlertTriangle },
  inativo:   { label: "Sem atividade", variant: "gray",  icon: MinusCircle   },
};

interface TeacherDashboardProps {
  onNavigate: (screen: string) => void;
}

export function TeacherDashboard({ onNavigate }: TeacherDashboardProps) {
  return (
    <div className="p-6 space-y-6">

      {/* ── Métricas ── */}
      <div className="grid grid-cols-2 lg:grid-cols-5 gap-3">
        {METRICS.map((m) => {
          const Icon = m.icon;
          return (
            <div
              key={m.label}
              className="rounded-xl border border-[rgba(124,58,237,0.18)] bg-[#16112e] p-4 flex flex-col gap-3"
            >
              <div className="flex items-center justify-between">
                <span className="text-xs text-[#8b7db8]" style={{ fontFamily: "var(--font-body)" }}>
                  {m.label}
                </span>
                <div
                  className="w-7 h-7 rounded-lg flex items-center justify-center"
                  style={{ background: m.bg }}
                >
                  <Icon size={14} style={{ color: m.color }} />
                </div>
              </div>
              <div>
                <p className="text-2xl font-bold text-[#e8e0f8]" style={{ fontFamily: "var(--font-display)" }}>
                  {m.value}
                </p>
                <p className="text-[10px] text-[#8b7db8] mt-0.5" style={{ fontFamily: "var(--font-body)" }}>
                  {m.delta}
                </p>
              </div>
            </div>
          );
        })}
      </div>

      {/* ── Linha principal: tabela de alunos + sidebar de alertas ── */}
      <div className="grid grid-cols-1 xl:grid-cols-[1fr_280px] gap-5">

        {/* Bloco esquerdo */}
        <div className="space-y-5">

          {/* Visão geral das guildas */}
          <section>
            <div className="flex items-center justify-between mb-3">
              <h2 className="text-sm text-[#e8e0f8]" style={{ fontFamily: "var(--font-display)", fontSize: "0.82rem" }}>
                Visão geral das Guildas
              </h2>
              <MagicButton variant="primary" size="sm" onClick={() => {}}>
                <Plus size={13} />
                Nova Guilda
              </MagicButton>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              {GUILDAS.map((g) => (
                <button
                  key={g.id}
                  onClick={() => onNavigate("teacher-guilda")}
                  className="text-left rounded-xl border border-[rgba(124,58,237,0.18)] bg-[#16112e] p-4 hover:border-[rgba(124,58,237,0.4)] hover:bg-[rgba(124,58,237,0.05)] transition-all duration-150 cursor-pointer group"
                >
                  <div className="flex items-start justify-between mb-3">
                    <div className="flex items-center gap-2.5">
                      <div
                        className="w-8 h-8 rounded-lg flex items-center justify-center text-base"
                        style={{ background: `${g.cor}1a`, border: `1px solid ${g.cor}44` }}
                      >
                        ⚔️
                      </div>
                      <div>
                        <p className="text-sm font-semibold text-[#e8e0f8]" style={{ fontFamily: "var(--font-body)" }}>
                          {g.name}
                        </p>
                        <p className="text-[10px] text-[#8b7db8]" style={{ fontFamily: "var(--font-body)" }}>
                          {g.alunos} alunos · Nível médio {g.nivel_medio}
                        </p>
                      </div>
                    </div>
                    <ChevronRight size={14} className="text-[#4a3d7a] group-hover:text-[#a78bfa] transition-colors mt-1" />
                  </div>
                  <MagicProgress value={g.progresso} color="purple" showLabel label="Progresso" size="sm" />
                  <div className="flex items-center gap-3 mt-2.5 text-xs text-[#8b7db8]" style={{ fontFamily: "var(--font-body)" }}>
                    <span className="flex items-center gap-1"><BookOpen size={10} /> {g.grimorios} grimórios</span>
                    <span className="flex items-center gap-1"><Zap size={10} /> {g.feiticos} feitiços</span>
                    <span className="flex items-center gap-1 text-[#d4a017]">
                      ✦ {(g.mana_total / 1000).toFixed(1)}k mana
                    </span>
                  </div>
                </button>
              ))}
            </div>
          </section>

          {/* Tabela de alunos */}
          <section>
            <div className="flex items-center justify-between mb-3">
              <h2 className="text-sm text-[#e8e0f8]" style={{ fontFamily: "var(--font-display)", fontSize: "0.82rem" }}>
                Alunos — visão geral
              </h2>
              <button
                onClick={() => onNavigate("teacher-progresso")}
                className="flex items-center gap-1.5 text-xs text-[#7c3aed] hover:text-[#a78bfa] transition-colors cursor-pointer"
                style={{ fontFamily: "var(--font-body)" }}
              >
                Ver progresso completo <ArrowRight size={12} />
              </button>
            </div>

            <div className="rounded-xl border border-[rgba(124,58,237,0.18)] bg-[#16112e] overflow-hidden">
              {/* Cabeçalho da tabela */}
              <div
                className="grid px-4 py-2.5 text-[10px] uppercase tracking-wider text-[#4a3d7a] border-b border-[rgba(124,58,237,0.12)]"
                style={{
                  gridTemplateColumns: "2fr 1fr 60px 80px 80px 80px 110px 110px",
                  fontFamily: "var(--font-mono)",
                }}
              >
                <span>Aluno</span>
                <span>Guilda</span>
                <span>Nível</span>
                <span>Mana</span>
                <span>Grimórios</span>
                <span>Feitiços</span>
                <span>Progresso</span>
                <span>Status</span>
              </div>

              {/* Linhas */}
              {ALUNOS.map((a, i) => {
                const st = STATUS_CONFIG[a.status];
                const StatusIcon = st.icon;
                return (
                  <div
                    key={a.id}
                    className={`grid items-center px-4 py-3 hover:bg-[rgba(124,58,237,0.05)] transition-colors cursor-pointer ${
                      i < ALUNOS.length - 1 ? "border-b border-[rgba(124,58,237,0.08)]" : ""
                    }`}
                    style={{ gridTemplateColumns: "2fr 1fr 60px 80px 80px 80px 110px 110px" }}
                  >
                    <div className="flex items-center gap-2.5 min-w-0">
                      <div className="w-7 h-7 rounded-full bg-gradient-to-br from-[#7c3aed] to-[#4c1d95] flex items-center justify-center text-xs flex-shrink-0">
                        {a.nome[0]}
                      </div>
                      <span className="text-sm text-[#e8e0f8] truncate" style={{ fontFamily: "var(--font-body)" }}>
                        {a.nome}
                      </span>
                    </div>
                    <span className="text-xs text-[#8b7db8]" style={{ fontFamily: "var(--font-body)" }}>
                      {a.guilda}
                    </span>
                    <span className="text-xs text-[#c4b5fd] font-semibold" style={{ fontFamily: "var(--font-mono)" }}>
                      {a.nivel}
                    </span>
                    <span className="text-xs text-[#67e8f9]" style={{ fontFamily: "var(--font-mono)" }}>
                      {a.mana}
                    </span>
                    <span className="text-xs text-[#8b7db8]" style={{ fontFamily: "var(--font-mono)" }}>
                      {a.grimorios}
                    </span>
                    <span className="text-xs text-[#8b7db8]" style={{ fontFamily: "var(--font-mono)" }}>
                      {a.feiticos}
                    </span>
                    <div className="pr-3">
                      <MagicProgress value={a.progresso} color={a.progresso >= 70 ? "purple" : a.progresso >= 40 ? "gold" : "cyan"} size="xs" />
                    </div>
                    <div>
                      <MagicBadge variant={st.variant}>
                        <StatusIcon size={10} />
                        {st.label}
                      </MagicBadge>
                    </div>
                  </div>
                );
              })}
            </div>
          </section>
        </div>

        {/* ── Sidebar de alertas ── */}
        <aside className="space-y-4">

          {/* Alertas e atenção */}
          <div className="rounded-xl border border-[rgba(124,58,237,0.18)] bg-[#16112e] overflow-hidden">
            <div className="px-4 py-3 border-b border-[rgba(124,58,237,0.12)] flex items-center gap-2">
              <AlertTriangle size={13} className="text-[#d4a017]" />
              <span className="text-xs font-semibold text-[#e8e0f8]" style={{ fontFamily: "var(--font-display)", fontSize: "0.78rem" }}>
                Atenção necessária
              </span>
              <span className="ml-auto text-xs bg-[rgba(212,160,23,0.15)] text-[#d4a017] border border-[rgba(212,160,23,0.3)] px-1.5 py-0.5 rounded-full" style={{ fontFamily: "var(--font-mono)" }}>
                {ALERTAS.filter(a => a.tipo !== "tarefa").length}
              </span>
            </div>
            <div className="divide-y divide-[rgba(124,58,237,0.08)]">
              {ALERTAS.filter(a => a.tipo !== "tarefa").map((a, i) => (
                <div key={i} className="px-4 py-3 flex items-start gap-2.5 hover:bg-[rgba(124,58,237,0.04)] transition-colors cursor-pointer">
                  <div className={`w-1.5 h-1.5 rounded-full mt-1.5 flex-shrink-0 ${a.tipo === "risco" ? "bg-[#d4a017]" : "bg-[#4a3d7a]"}`} />
                  <div className="min-w-0">
                    <p className="text-xs font-semibold text-[#e8e0f8] truncate" style={{ fontFamily: "var(--font-body)" }}>
                      {a.aluno}
                    </p>
                    <p className="text-[10px] text-[#8b7db8]" style={{ fontFamily: "var(--font-body)" }}>
                      {a.msg}
                    </p>
                    {a.guilda && (
                      <p className="text-[10px] text-[#4a3d7a] mt-0.5" style={{ fontFamily: "var(--font-body)" }}>
                        {a.guilda}
                      </p>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Tarefas pendentes */}
          <div className="rounded-xl border border-[rgba(124,58,237,0.18)] bg-[#16112e] overflow-hidden">
            <div className="px-4 py-3 border-b border-[rgba(124,58,237,0.12)] flex items-center gap-2">
              <Clock size={13} className="text-[#7c3aed]" />
              <span className="text-xs font-semibold text-[#e8e0f8]" style={{ fontFamily: "var(--font-display)", fontSize: "0.78rem" }}>
                Tarefas pendentes
              </span>
              <span className="ml-auto text-xs bg-[rgba(124,58,237,0.15)] text-[#c4b5fd] border border-[rgba(124,58,237,0.3)] px-1.5 py-0.5 rounded-full" style={{ fontFamily: "var(--font-mono)" }}>
                {ALERTAS.filter(a => a.tipo === "tarefa").length}
              </span>
            </div>
            <div className="divide-y divide-[rgba(124,58,237,0.08)]">
              {ALERTAS.filter(a => a.tipo === "tarefa").map((a, i) => (
                <div key={i} className="px-4 py-3 flex items-center gap-2.5 hover:bg-[rgba(124,58,237,0.04)] transition-colors cursor-pointer">
                  <Circle size={13} className="text-[#4a3d7a] flex-shrink-0" />
                  <p className="text-xs text-[#c4b5fd] flex-1" style={{ fontFamily: "var(--font-body)" }}>
                    {a.msg}
                  </p>
                  <ChevronRight size={12} className="text-[#4a3d7a]" />
                </div>
              ))}
            </div>
          </div>

          {/* Ações rápidas */}
          <div className="rounded-xl border border-[rgba(124,58,237,0.18)] bg-[#16112e] p-4 space-y-2">
            <p className="text-[10px] uppercase tracking-wider text-[#4a3d7a] mb-3" style={{ fontFamily: "var(--font-mono)" }}>
              Ações rápidas
            </p>
            {[
              { label: "Criar nova guilda",        icon: Plus,       action: () => {} },
              { label: "Ver progresso da guilda",  icon: TrendingUp, action: () => onNavigate("teacher-progresso") },
              { label: "Revisar atividades",       icon: BookOpen,   action: () => {} },
            ].map(({ label, icon: Icon, action }) => (
              <button
                key={label}
                onClick={action}
                className="w-full flex items-center gap-2.5 px-3 py-2 rounded-lg text-xs text-[#c4b5fd] hover:bg-[rgba(124,58,237,0.12)] border border-[rgba(124,58,237,0.15)] hover:border-[rgba(124,58,237,0.3)] transition-all cursor-pointer"
                style={{ fontFamily: "var(--font-body)" }}
              >
                <Icon size={13} className="text-[#7c3aed]" />
                {label}
              </button>
            ))}
          </div>
        </aside>
      </div>
    </div>
  );
}
