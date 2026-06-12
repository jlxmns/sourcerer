import { useState } from "react";
import {
  Filter, Search, TrendingUp, TrendingDown, Minus,
  BookOpen, Zap, Star, AlertTriangle, CheckCircle2,
  MinusCircle, ChevronDown,
} from "lucide-react";
import { MagicBadge, MagicButton, MagicProgress } from "../ui/MagicCard";

const TODOS_ALUNOS = [
  { id:  1, nome: "Vitória Mendes",   guilda: "Corvinal",   nivel: 9, mana: 980, grimorios: 5, feiticos: 48, progresso: 95, status: "avancando", tendencia: "up",   ultimaAtiv: "Hoje"        },
  { id:  2, nome: "Lucas Pereira",    guilda: "Corvinal",   nivel: 8, mana: 840, grimorios: 4, feiticos: 42, progresso: 88, status: "avancando", tendencia: "up",   ultimaAtiv: "Hoje"        },
  { id:  3, nome: "Mariana Lima",     guilda: "Corvinal",   nivel: 8, mana: 810, grimorios: 4, feiticos: 40, progresso: 84, status: "avancando", tendencia: "up",   ultimaAtiv: "Ontem"       },
  { id:  4, nome: "Ana Beatriz",      guilda: "Grifinória", nivel: 7, mana: 720, grimorios: 4, feiticos: 38, progresso: 76, status: "avancando", tendencia: "up",   ultimaAtiv: "Ontem"       },
  { id:  5, nome: "Felipe Costa",     guilda: "Corvinal",   nivel: 7, mana: 710, grimorios: 4, feiticos: 36, progresso: 79, status: "avancando", tendencia: "flat", ultimaAtiv: "2 dias"      },
  { id:  6, nome: "Rafael Torres",    guilda: "Grifinória", nivel: 6, mana: 580, grimorios: 3, feiticos: 31, progresso: 65, status: "avancando", tendencia: "up",   ultimaAtiv: "2 dias"      },
  { id:  7, nome: "Beatriz Alves",    guilda: "Corvinal",   nivel: 6, mana: 590, grimorios: 3, feiticos: 30, progresso: 68, status: "avancando", tendencia: "flat", ultimaAtiv: "3 dias"      },
  { id:  8, nome: "Gabriel Nunes",    guilda: "Sonserina",  nivel: 6, mana: 560, grimorios: 3, feiticos: 28, progresso: 59, status: "avancando", tendencia: "up",   ultimaAtiv: "Hoje"        },
  { id:  9, nome: "Diego Martins",    guilda: "Corvinal",   nivel: 6, mana: 540, grimorios: 3, feiticos: 27, progresso: 60, status: "avancando", tendencia: "flat", ultimaAtiv: "4 dias"      },
  { id: 10, nome: "Camila Souza",     guilda: "Lufa-Lufa",  nivel: 5, mana: 380, grimorios: 2, feiticos: 18, progresso: 40, status: "risco",     tendencia: "down", ultimaAtiv: "5 dias"      },
  { id: 11, nome: "Pedro Alves",      guilda: "Sonserina",  nivel: 5, mana: 420, grimorios: 3, feiticos: 22, progresso: 48, status: "risco",     tendencia: "down", ultimaAtiv: "5 dias"      },
  { id: 12, nome: "Júlia Ferreira",   guilda: "Corvinal",   nivel: 5, mana: 410, grimorios: 2, feiticos: 19, progresso: 43, status: "risco",     tendencia: "flat", ultimaAtiv: "7 dias"      },
  { id: 13, nome: "Henrique Duarte",  guilda: "Corvinal",   nivel: 4, mana: 280, grimorios: 2, feiticos: 14, progresso: 32, status: "risco",     tendencia: "down", ultimaAtiv: "8 dias"      },
  { id: 14, nome: "Isabela Castro",   guilda: "Lufa-Lufa",  nivel: 3, mana: 160, grimorios: 1, feiticos:  8, progresso: 17, status: "inativo",   tendencia: "down", ultimaAtiv: "12 dias"     },
  { id: 15, nome: "Sophia Ramos",     guilda: "Lufa-Lufa",  nivel: 3, mana: 140, grimorios: 1, feiticos:  7, progresso: 15, status: "inativo",   tendencia: "down", ultimaAtiv: "14 dias"     },
];

const GUILDAS_FILTRO = ["Todas", "Corvinal", "Grifinória", "Lufa-Lufa", "Sonserina"];
const STATUS_FILTRO  = ["Todos", "Avançando", "Em risco", "Sem atividade"];
const NIVEL_FILTRO   = ["Todos", "1–3", "4–6", "7–9"];

const STATUS_CONFIG: Record<string, { label: string; variant: "green" | "gold" | "red" | "gray" }> = {
  avancando: { label: "Avançando",     variant: "green" },
  risco:     { label: "Em risco",      variant: "red"   },
  inativo:   { label: "Sem atividade", variant: "gray"  },
};

interface TeacherProgressProps {
  onNavigate: (screen: string) => void;
}

export function TeacherProgress({ onNavigate }: TeacherProgressProps) {
  const [guildaFiltro, setGuildaFiltro]   = useState("Todas");
  const [statusFiltro, setStatusFiltro]   = useState("Todos");
  const [nivelFiltro,  setNivelFiltro]    = useState("Todos");
  const [busca,        setBusca]          = useState("");

  const filtrados = TODOS_ALUNOS.filter((a) => {
    if (guildaFiltro !== "Todas" && a.guilda !== guildaFiltro) return false;
    if (statusFiltro === "Avançando"     && a.status !== "avancando") return false;
    if (statusFiltro === "Em risco"      && a.status !== "risco")     return false;
    if (statusFiltro === "Sem atividade" && a.status !== "inativo")   return false;
    if (nivelFiltro === "1–3" && (a.nivel < 1 || a.nivel > 3)) return false;
    if (nivelFiltro === "4–6" && (a.nivel < 4 || a.nivel > 6)) return false;
    if (nivelFiltro === "7–9" && (a.nivel < 7 || a.nivel > 9)) return false;
    if (busca && !a.nome.toLowerCase().includes(busca.toLowerCase())) return false;
    return true;
  });

  const avancando = filtrados.filter((a) => a.status === "avancando").length;
  const risco     = filtrados.filter((a) => a.status === "risco").length;
  const inativo   = filtrados.filter((a) => a.status === "inativo").length;

  return (
    <div className="p-6 space-y-5">

      {/* Cabeçalho com resumo */}
      <div className="flex items-start justify-between flex-wrap gap-4">
        <div>
          <h2 className="text-base text-[#e8e0f8] mb-0.5" style={{ fontFamily: "var(--font-display)", fontSize: "0.9rem" }}>
            Acompanhamento de Progresso
          </h2>
          <p className="text-xs text-[#8b7db8]" style={{ fontFamily: "var(--font-body)" }}>
            Visão detalhada de todos os alunos · {TODOS_ALUNOS.length} alunos no total
          </p>
        </div>
        <MagicButton variant="secondary" size="sm">
          <TrendingUp size={13} />
          Exportar relatório
        </MagicButton>
      </div>

      {/* Cards de resumo rápido */}
      <div className="grid grid-cols-3 gap-3">
        {[
          { label: "Avançando bem",    val: avancando, color: "#22c55e", bg: "rgba(34,197,94,0.08)",   border: "rgba(34,197,94,0.2)",   icon: CheckCircle2  },
          { label: "Em risco",         val: risco,     color: "#d4a017", bg: "rgba(212,160,23,0.08)",  border: "rgba(212,160,23,0.2)",  icon: AlertTriangle },
          { label: "Sem atividade",    val: inativo,   color: "#8b7db8", bg: "rgba(139,125,184,0.08)", border: "rgba(139,125,184,0.2)", icon: MinusCircle   },
        ].map(({ label, val, color, bg, border, icon: Icon }) => (
          <div key={label} className="rounded-xl border p-4 flex items-center gap-3" style={{ background: bg, borderColor: border }}>
            <Icon size={18} style={{ color }} />
            <div>
              <p className="text-xl font-bold" style={{ fontFamily: "var(--font-display)", color }}>{val}</p>
              <p className="text-xs text-[#8b7db8]" style={{ fontFamily: "var(--font-body)" }}>{label}</p>
            </div>
          </div>
        ))}
      </div>

      {/* Filtros */}
      <div className="flex items-center gap-3 flex-wrap">
        {/* Busca */}
        <div className="relative">
          <Search size={13} className="absolute left-3 top-1/2 -translate-y-1/2 text-[#4a3d7a]" />
          <input
            value={busca}
            onChange={(e) => setBusca(e.target.value)}
            placeholder="Buscar aluno…"
            className="bg-[#16112e] border border-[rgba(124,58,237,0.25)] rounded-lg pl-8 pr-4 py-2 text-sm text-[#e8e0f8] placeholder-[#4a3d7a] focus:outline-none focus:border-[#7c3aed] transition-colors w-44"
            style={{ fontFamily: "var(--font-body)" }}
          />
        </div>

        {/* Filtro guilda */}
        <FilterSelect label="Guilda" options={GUILDAS_FILTRO} value={guildaFiltro} onChange={setGuildaFiltro} />
        <FilterSelect label="Status" options={STATUS_FILTRO}  value={statusFiltro} onChange={setStatusFiltro} />
        <FilterSelect label="Nível"  options={NIVEL_FILTRO}   value={nivelFiltro}  onChange={setNivelFiltro}  />

        {(guildaFiltro !== "Todas" || statusFiltro !== "Todos" || nivelFiltro !== "Todos" || busca) && (
          <button
            onClick={() => { setGuildaFiltro("Todas"); setStatusFiltro("Todos"); setNivelFiltro("Todos"); setBusca(""); }}
            className="text-xs text-[#8b7db8] hover:text-[#c4b5fd] transition-colors cursor-pointer px-2"
            style={{ fontFamily: "var(--font-body)" }}
          >
            Limpar filtros
          </button>
        )}

        <span className="ml-auto text-xs text-[#8b7db8]" style={{ fontFamily: "var(--font-body)" }}>
          {filtrados.length} aluno{filtrados.length !== 1 ? "s" : ""}
        </span>
      </div>

      {/* Tabela de progresso */}
      <div className="rounded-xl border border-[rgba(124,58,237,0.18)] bg-[#16112e] overflow-hidden">
        {/* Cabeçalho */}
        <div
          className="grid px-5 py-2.5 text-[10px] uppercase tracking-wider text-[#4a3d7a] border-b border-[rgba(124,58,237,0.12)]"
          style={{ gridTemplateColumns: "2fr 1fr 60px 80px 90px 90px 130px 110px 90px", fontFamily: "var(--font-mono)" }}
        >
          <span>Aluno</span>
          <span>Guilda</span>
          <span>Nível</span>
          <span>Mana</span>
          <span>Grimórios</span>
          <span>Feitiços</span>
          <span>Progresso</span>
          <span>Status</span>
          <span>Últ. atividade</span>
        </div>

        {filtrados.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-16 gap-3">
            <span className="text-4xl opacity-30">🔍</span>
            <p className="text-sm text-[#4a3d7a]" style={{ fontFamily: "var(--font-body)" }}>
              Nenhum aluno encontrado com esses filtros.
            </p>
          </div>
        ) : (
          <div className="divide-y divide-[rgba(124,58,237,0.07)]">
            {filtrados.map((a) => {
              const st = STATUS_CONFIG[a.status];
              const TendIcon = a.tendencia === "up" ? TrendingUp : a.tendencia === "down" ? TrendingDown : Minus;
              const tendColor = a.tendencia === "up" ? "#22c55e" : a.tendencia === "down" ? "#f87171" : "#8b7db8";

              return (
                <div
                  key={a.id}
                  className="grid items-center px-5 py-3 hover:bg-[rgba(124,58,237,0.04)] transition-colors cursor-pointer"
                  style={{ gridTemplateColumns: "2fr 1fr 60px 80px 90px 90px 130px 110px 90px" }}
                >
                  <div className="flex items-center gap-2.5 min-w-0">
                    <div className="w-7 h-7 rounded-full bg-gradient-to-br from-[#7c3aed] to-[#4c1d95] flex items-center justify-center text-xs flex-shrink-0">
                      {a.nome[0]}
                    </div>
                    <div className="flex items-center gap-1.5 min-w-0">
                      <span className="text-sm text-[#e8e0f8] truncate" style={{ fontFamily: "var(--font-body)" }}>
                        {a.nome}
                      </span>
                      <TendIcon size={12} style={{ color: tendColor }} className="flex-shrink-0" />
                    </div>
                  </div>
                  <span className="text-xs text-[#8b7db8] truncate" style={{ fontFamily: "var(--font-body)" }}>{a.guilda}</span>
                  <span className="text-xs text-[#c4b5fd] font-semibold" style={{ fontFamily: "var(--font-mono)" }}>{a.nivel}</span>
                  <span className="text-xs text-[#67e8f9]" style={{ fontFamily: "var(--font-mono)" }}>{a.mana}</span>
                  <span className="text-xs text-[#8b7db8]" style={{ fontFamily: "var(--font-mono)" }}>{a.grimorios}</span>
                  <span className="text-xs text-[#8b7db8]" style={{ fontFamily: "var(--font-mono)" }}>{a.feiticos}</span>
                  <div className="pr-3">
                    <MagicProgress
                      value={a.progresso}
                      color={a.progresso >= 70 ? "purple" : a.progresso >= 40 ? "gold" : "cyan"}
                      size="xs"
                      showLabel
                    />
                  </div>
                  <MagicBadge variant={st.variant}>{st.label}</MagicBadge>
                  <span
                    className={`text-xs ${a.status === "inativo" ? "text-[#f87171]" : a.status === "risco" ? "text-[#d4a017]" : "text-[#8b7db8]"}`}
                    style={{ fontFamily: "var(--font-body)" }}
                  >
                    {a.ultimaAtiv}
                  </span>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}

/* Componente select de filtro */
function FilterSelect({ label, options, value, onChange }: {
  label: string; options: string[]; value: string; onChange: (v: string) => void;
}) {
  return (
    <div className="relative">
      <select
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="appearance-none bg-[#16112e] border border-[rgba(124,58,237,0.25)] rounded-lg pl-3 pr-7 py-2 text-sm text-[#c4b5fd] focus:outline-none focus:border-[#7c3aed] transition-colors cursor-pointer"
        style={{ fontFamily: "var(--font-body)" }}
      >
        {options.map((o) => (
          <option key={o} value={o} style={{ background: "#16112e" }}>{o === options[0] ? `${label}: ${o}` : o}</option>
        ))}
      </select>
      <ChevronDown size={12} className="absolute right-2.5 top-1/2 -translate-y-1/2 text-[#4a3d7a] pointer-events-none" />
    </div>
  );
}
