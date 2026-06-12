import { useState } from "react";
import { ArrowLeft, Play, CheckCircle, RotateCcw, Zap, Star, Info, ChevronDown, ChevronUp, Lightbulb, Trophy, AlertCircle, CheckCircle2 } from "lucide-react";
import { AppHeader } from "./AppHeader";
import { MagicCard, MagicBadge, MagicButton } from "./ui/MagicCard";

type FeedbackState = "idle" | "success" | "error" | "running";

interface SpellExerciseScreenProps {
  onNavigate: (screen: string) => void;
}

export function SpellExerciseScreen({ onNavigate }: SpellExerciseScreenProps) {
  const [feedback, setFeedback] = useState<FeedbackState>("idle");
  const [showHint, setShowHint] = useState(false);
  const [showInstructions, setShowInstructions] = useState(true);

  function handleRun() {
    setFeedback("running");
    setTimeout(() => setFeedback("success"), 1800);
  }

  function handleVerify() {
    setFeedback("success");
  }

  function handleReset() {
    setFeedback("idle");
  }

  return (
    <div className="min-h-screen bg-[#0d0a1e] flex flex-col">
      <AppHeader onNavigate={onNavigate} />

      <div className="pt-16 flex-1 flex flex-col">
        {/* Barra de contexto do exercício */}
        <div className="bg-[#100d24] border-b border-[rgba(124,58,237,0.2)] px-6 py-3 flex items-center gap-4 flex-wrap">
          <button
            onClick={() => onNavigate("grimorio")}
            className="flex items-center gap-1.5 text-sm text-[#8b7db8] hover:text-[#c4b5fd] transition-colors cursor-pointer group"
          >
            <ArrowLeft size={14} className="group-hover:-translate-x-0.5 transition-transform" />
            <span style={{ fontFamily: 'var(--font-body)' }}>Fundamentos de Algoritmos</span>
          </button>
          <span className="text-[#4a3d7a]">/</span>
          <span className="text-sm text-[#e8e0f8]" style={{ fontFamily: 'var(--font-body)' }}>
            Condicionais: se... então
          </span>

          <div className="ml-auto flex items-center gap-3 flex-wrap">
            <MagicBadge variant="gold">Médio</MagicBadge>
            <div className="flex items-center gap-1 text-sm text-[#67e8f9]" style={{ fontFamily: 'var(--font-body)' }}>
              <Zap size={13} />
              <span>+40 mana</span>
            </div>
            <div className="flex items-center gap-1 text-sm text-[#d4a017]" style={{ fontFamily: 'var(--font-body)' }}>
              <Star size={13} />
              <span>+40 XP</span>
            </div>
            <div className="flex items-center gap-1 text-xs text-[#8b7db8]" style={{ fontFamily: 'var(--font-body)' }}>
              Feitiço 4 de 8
            </div>
          </div>
        </div>

        {/* Layout principal em duas colunas */}
        <div className="flex-1 flex overflow-hidden" style={{ height: 'calc(100vh - 4rem - 49px)' }}>

          {/* Painel esquerdo — Descrição + Instruções + Feedback */}
          <div className="w-[340px] xl:w-[380px] flex-shrink-0 border-r border-[rgba(124,58,237,0.15)] flex flex-col overflow-y-auto bg-[#0d0a1e]">

            {/* Descrição do problema */}
            <div className="p-5 border-b border-[rgba(124,58,237,0.12)]">
              <div className="flex items-center gap-2 mb-3">
                <div className="w-7 h-7 rounded-lg bg-[rgba(124,58,237,0.2)] flex items-center justify-center">
                  <span className="text-base">🔀</span>
                </div>
                <h2 className="text-base text-[#e8e0f8]" style={{ fontFamily: 'var(--font-display)', fontSize: '0.95rem' }}>
                  Condicionais: se... então
                </h2>
              </div>
              <p className="text-sm text-[#c4b5fd] leading-relaxed mb-3" style={{ fontFamily: 'var(--font-body)' }}>
                O mago precisa atravessar uma ponte, mas ela só abre se a senha mágica for correta.
              </p>
              <p className="text-sm text-[#8b7db8] leading-relaxed" style={{ fontFamily: 'var(--font-body)' }}>
                Use uma estrutura condicional para verificar se a senha é <span className="text-[#c4b5fd] font-mono bg-[rgba(124,58,237,0.15)] px-1 rounded">ARCANO</span> e, se for, abrir a ponte. Se não for, mostre a mensagem <span className="text-[#c4b5fd] font-mono bg-[rgba(124,58,237,0.15)] px-1 rounded">"Acesso negado!"</span>.
              </p>
            </div>

            {/* Instruções colapsáveis */}
            <div className="border-b border-[rgba(124,58,237,0.12)]">
              <button
                onClick={() => setShowInstructions(!showInstructions)}
                className="w-full flex items-center justify-between px-5 py-3 hover:bg-[rgba(124,58,237,0.05)] transition-colors cursor-pointer"
              >
                <div className="flex items-center gap-2">
                  <Info size={14} className="text-[#7c3aed]" />
                  <span className="text-sm font-semibold text-[#e8e0f8]" style={{ fontFamily: 'var(--font-body)' }}>
                    Instruções passo a passo
                  </span>
                </div>
                {showInstructions ? <ChevronUp size={15} className="text-[#8b7db8]" /> : <ChevronDown size={15} className="text-[#8b7db8]" />}
              </button>
              {showInstructions && (
                <div className="px-5 pb-4 space-y-2">
                  {[
                    "Use o bloco de variável para guardar a senha digitada.",
                    "Use o bloco \"se... então\" para comparar a senha com \"ARCANO\".",
                    "Se a condição for verdadeira, conecte o bloco \"Abrir ponte\".",
                    "Na parte \"senão\", conecte o bloco \"Mostrar mensagem\" com o texto \"Acesso negado!\".",
                    "Execute o feitiço e teste com senhas diferentes.",
                  ].map((step, i) => (
                    <div key={i} className="flex items-start gap-2.5">
                      <span
                        className="w-5 h-5 rounded-full bg-[rgba(124,58,237,0.2)] flex items-center justify-center text-xs text-[#a78bfa] font-bold flex-shrink-0 mt-0.5"
                        style={{ fontFamily: 'var(--font-mono)' }}
                      >
                        {i + 1}
                      </span>
                      <p className="text-xs text-[#8b7db8] leading-relaxed" style={{ fontFamily: 'var(--font-body)' }}>
                        {step}
                      </p>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Dica */}
            <div className="p-4 border-b border-[rgba(124,58,237,0.12)]">
              <button
                onClick={() => setShowHint(!showHint)}
                className="flex items-center gap-2 text-sm text-[#d4a017] hover:text-[#f0c040] transition-colors cursor-pointer"
                style={{ fontFamily: 'var(--font-body)' }}
              >
                <Lightbulb size={14} />
                {showHint ? "Esconder dica" : "Mostrar dica (−5 mana)"}
              </button>
              {showHint && (
                <div className="mt-2 p-3 rounded-lg bg-[rgba(212,160,23,0.08)] border border-[rgba(212,160,23,0.2)] text-xs text-[#c4b5fd] leading-relaxed" style={{ fontFamily: 'var(--font-body)' }}>
                  Lembre-se: a comparação entre textos é sensível a maiúsculas e minúsculas. Certifique-se que "ARCANO" está todo em letras maiúsculas no bloco de comparação.
                </div>
              )}
            </div>

            {/* Recompensa */}
            <div className="p-4 border-b border-[rgba(124,58,237,0.12)]">
              <p className="text-xs text-[#8b7db8] uppercase tracking-wider mb-2" style={{ fontFamily: 'var(--font-mono)' }}>
                Recompensa ao concluir
              </p>
              <div className="flex items-center gap-3">
                <div className="flex items-center gap-1.5 text-sm text-[#67e8f9]" style={{ fontFamily: 'var(--font-body)' }}>
                  <Zap size={14} /> +40 mana
                </div>
                <div className="flex items-center gap-1.5 text-sm text-[#d4a017]" style={{ fontFamily: 'var(--font-body)' }}>
                  <Star size={14} /> +40 XP
                </div>
              </div>
            </div>

            {/* Feedback de resultado */}
            <div className="p-4 flex-1 flex flex-col justify-end">
              {feedback === "idle" && (
                <div className="rounded-xl border border-[rgba(124,58,237,0.15)] bg-[#16112e] p-4 text-center">
                  <p className="text-xs text-[#4a3d7a]" style={{ fontFamily: 'var(--font-body)' }}>
                    Execute seu feitiço para ver o resultado aqui.
                  </p>
                </div>
              )}

              {feedback === "running" && (
                <div className="rounded-xl border border-[rgba(124,58,237,0.3)] bg-[rgba(124,58,237,0.08)] p-4 text-center">
                  <div className="flex items-center justify-center gap-2 text-[#c4b5fd]">
                    <div className="w-4 h-4 border-2 border-[#7c3aed] border-t-transparent rounded-full animate-spin" />
                    <span className="text-sm" style={{ fontFamily: 'var(--font-body)' }}>Executando feitiço…</span>
                  </div>
                </div>
              )}

              {feedback === "success" && (
                <div className="rounded-xl border border-[rgba(34,197,94,0.3)] bg-[rgba(34,197,94,0.07)] p-4">
                  <div className="flex items-center gap-2 mb-2">
                    <CheckCircle2 size={18} className="text-[#22c55e]" />
                    <span className="text-sm font-semibold text-[#86efac]" style={{ fontFamily: 'var(--font-body)' }}>
                      Feitiço correto! ✨
                    </span>
                  </div>
                  <p className="text-xs text-[#8b7db8] mb-3" style={{ fontFamily: 'var(--font-body)' }}>
                    Saída: <span className="text-[#86efac] font-mono">"Ponte aberta! Bem-vindo, mago."</span>
                  </p>
                  <div className="flex items-center gap-3">
                    <span className="text-xs text-[#67e8f9] font-semibold" style={{ fontFamily: 'var(--font-body)' }}>+40 mana</span>
                    <span className="text-xs text-[#d4a017] font-semibold" style={{ fontFamily: 'var(--font-body)' }}>+40 XP</span>
                  </div>
                </div>
              )}

              {feedback === "error" && (
                <div className="rounded-xl border border-[rgba(239,68,68,0.3)] bg-[rgba(239,68,68,0.07)] p-4">
                  <div className="flex items-center gap-2 mb-2">
                    <AlertCircle size={18} className="text-[#f87171]" />
                    <span className="text-sm font-semibold text-[#fca5a5]" style={{ fontFamily: 'var(--font-body)' }}>
                      Feitiço com erro
                    </span>
                  </div>
                  <p className="text-xs text-[#8b7db8]" style={{ fontFamily: 'var(--font-body)' }}>
                    A ponte não abriu. Verifique sua estrutura condicional e tente novamente.
                  </p>
                </div>
              )}
            </div>
          </div>

          {/* Painel direito — Área Blockly + Botões */}
          <div className="flex-1 flex flex-col overflow-hidden">
            {/* Toolbar de ações */}
            <div className="flex items-center gap-3 px-4 py-3 bg-[#100d24] border-b border-[rgba(124,58,237,0.15)]">
              <MagicButton variant="primary" size="sm" onClick={handleRun}>
                <Play size={14} fill="currentColor" />
                Executar
              </MagicButton>
              <MagicButton variant="gold" size="sm" onClick={handleVerify}>
                <CheckCircle size={14} />
                Verificar resposta
              </MagicButton>
              <MagicButton variant="ghost" size="sm" onClick={handleReset}>
                <RotateCcw size={14} />
                Reiniciar
              </MagicButton>
              <div className="ml-auto flex items-center gap-2 text-xs text-[#4a3d7a]" style={{ fontFamily: 'var(--font-body)' }}>
                <span>Tentativas: 2</span>
              </div>
            </div>

            {/* Área reservada para Blockly */}
            <div className="flex-1 flex flex-col items-center justify-center bg-[#0b0919] relative overflow-hidden">
              {/* Grade de fundo estilo editor */}
              <div
                className="absolute inset-0 opacity-[0.04]"
                style={{
                  backgroundImage: `
                    linear-gradient(rgba(124,58,237,1) 1px, transparent 1px),
                    linear-gradient(90deg, rgba(124,58,237,1) 1px, transparent 1px)
                  `,
                  backgroundSize: '32px 32px',
                }}
              />

              {/* Placeholder visual do Blockly */}
              <div className="relative z-10 flex flex-col items-center gap-5 max-w-md text-center px-8">
                <div className="w-16 h-16 rounded-2xl bg-[rgba(124,58,237,0.12)] border border-[rgba(124,58,237,0.2)] flex items-center justify-center">
                  <span className="text-3xl">🧩</span>
                </div>
                <div>
                  <p className="text-sm font-semibold text-[#4a3d7a] mb-1" style={{ fontFamily: 'var(--font-display)', fontSize: '0.8rem' }}>
                    Área de Blocos — Blockly
                  </p>
                  <p className="text-xs text-[#2e2550] leading-relaxed" style={{ fontFamily: 'var(--font-body)' }}>
                    O editor de blocos Blockly será carregado aqui. Arraste e encaixe os blocos para montar seu feitiço.
                  </p>
                </div>

                {/* Blocos ilustrativos decorativos */}
                <div className="flex flex-col gap-1.5 w-64 pointer-events-none select-none">
                  {/* Bloco SE */}
                  <div className="flex items-center gap-0">
                    <div className="h-10 w-3 rounded-l-md bg-[rgba(124,58,237,0.18)] border border-[rgba(124,58,237,0.2)] border-r-0" />
                    <div className="flex-1 h-10 flex items-center px-3 bg-[rgba(124,58,237,0.12)] border border-[rgba(124,58,237,0.2)] rounded-r-md">
                      <span className="text-xs text-[#4a3d7a]" style={{ fontFamily: 'var(--font-mono)' }}>🔀 se … então</span>
                    </div>
                  </div>
                  {/* Bloco condição */}
                  <div className="ml-5 flex items-center gap-0">
                    <div className="h-8 w-3 rounded-l-md bg-[rgba(6,182,212,0.15)] border border-[rgba(6,182,212,0.2)] border-r-0" />
                    <div className="flex-1 h-8 flex items-center px-3 bg-[rgba(6,182,212,0.08)] border border-[rgba(6,182,212,0.2)] rounded-r-md">
                      <span className="text-xs text-[#2e4a5a]" style={{ fontFamily: 'var(--font-mono)' }}>= senha "ARCANO"</span>
                    </div>
                  </div>
                  {/* Bloco ação */}
                  <div className="ml-5 flex items-center gap-0">
                    <div className="h-8 w-3 rounded-l-md bg-[rgba(34,197,94,0.15)] border border-[rgba(34,197,94,0.2)] border-r-0" />
                    <div className="flex-1 h-8 flex items-center px-3 bg-[rgba(34,197,94,0.08)] border border-[rgba(34,197,94,0.2)] rounded-r-md">
                      <span className="text-xs text-[#1a3d28]" style={{ fontFamily: 'var(--font-mono)' }}>▶ abrir ponte</span>
                    </div>
                  </div>
                  {/* Bloco senão */}
                  <div className="flex items-center gap-0">
                    <div className="h-8 w-3 rounded-l-md bg-[rgba(239,68,68,0.15)] border border-[rgba(239,68,68,0.2)] border-r-0" />
                    <div className="flex-1 h-8 flex items-center px-3 bg-[rgba(239,68,68,0.08)] border border-[rgba(239,68,68,0.2)] rounded-r-md">
                      <span className="text-xs text-[#3d1a1a]" style={{ fontFamily: 'var(--font-mono)' }}>senão: mostrar "Acesso negado!"</span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Label de canto */}
              <div className="absolute bottom-3 right-4 text-xs text-[#2e2550]" style={{ fontFamily: 'var(--font-mono)' }}>
                Blockly Workspace
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
