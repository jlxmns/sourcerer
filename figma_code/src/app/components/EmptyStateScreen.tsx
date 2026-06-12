import { useState } from "react";
import { Hash, ArrowRight, Sparkles, BookOpen, Users } from "lucide-react";
import { AppHeader } from "./AppHeader";
import { ProfileSidebar } from "./ProfileSidebar";
import { MagicCard, MagicButton, MagicInput } from "./ui/MagicCard";

interface EmptyStateScreenProps {
  onNavigate: (screen: string) => void;
}

export function EmptyStateScreen({ onNavigate }: EmptyStateScreenProps) {
  const [code, setCode] = useState("");

  return (
    <div className="min-h-screen bg-[#0d0a1e]">
      <AppHeader onNavigate={onNavigate} />
      <div className="pt-16 flex">
        {/* Sidebar com estado sem turma */}
        <div className="hidden lg:flex w-64 flex-shrink-0 border-r border-[rgba(124,58,237,0.15)] flex-col">
          <div className="px-4 overflow-y-auto flex-1">
            <ProfileSidebar noClass />
          </div>
        </div>

        {/* Área principal */}
        <main className="flex-1 flex items-center justify-center px-6 py-12">
          <div className="w-full max-w-lg">
            {/* Ilustração */}
            <div className="relative flex items-center justify-center mb-10">
              {/* Círculo de fundo */}
              <div className="absolute w-56 h-56 rounded-full bg-[radial-gradient(circle,rgba(124,58,237,0.12)_0%,transparent_70%)]" />
              {/* Círculo mágico SVG */}
              <svg width="220" height="220" viewBox="0 0 220 220" className="opacity-20 absolute">
                <circle cx="110" cy="110" r="100" fill="none" stroke="#7c3aed" strokeWidth="1" strokeDasharray="6 10" />
                <circle cx="110" cy="110" r="75" fill="none" stroke="#06b6d4" strokeWidth="0.5" />
                <polygon points="110,20 195,170 25,170" fill="none" stroke="#7c3aed" strokeWidth="0.5" />
              </svg>
              <div className="relative z-10 w-28 h-28 rounded-2xl bg-gradient-to-br from-[#2d1f5e] to-[#1a0e3d] border border-[rgba(124,58,237,0.3)] flex items-center justify-center shadow-[0_0_30px_rgba(124,58,237,0.2)]">
                <span className="text-5xl">📜</span>
              </div>
            </div>

            {/* Texto */}
            <div className="text-center mb-8">
              <h2 className="text-2xl text-[#e8e0f8] mb-3" style={{ fontFamily: 'var(--font-display)' }}>
                Sua jornada começa aqui
              </h2>
              <p className="text-[#8b7db8] leading-relaxed text-sm mx-auto max-w-sm" style={{ fontFamily: 'var(--font-body)' }}>
                Você ainda não faz parte de nenhuma turma. Aguarde um professor adicionar você ou insira um código de turma para começar sua aventura arcana.
              </p>
            </div>

            {/* Card para inserir código */}
            <MagicCard glow className="p-6 mb-4">
              <div className="flex items-center gap-2 mb-4">
                <Hash size={16} className="text-[#7c3aed]" />
                <span className="text-sm font-semibold text-[#e8e0f8]" style={{ fontFamily: 'var(--font-display)', fontSize: '0.85rem' }}>
                  Entrar com código de turma
                </span>
              </div>
              <div className="flex gap-3">
                <div className="flex-1">
                  <input
                    type="text"
                    value={code}
                    onChange={(e) => setCode(e.target.value.toUpperCase())}
                    placeholder="Ex.: MAGIA-7A-2024"
                    maxLength={16}
                    className="w-full bg-[#1e1540] border border-[rgba(124,58,237,0.3)] rounded-lg text-[#e8e0f8] placeholder-[#4a3d7a] px-4 py-3 focus:outline-none focus:border-[#7c3aed] focus:ring-2 focus:ring-[rgba(124,58,237,0.25)] transition-all duration-200"
                    style={{ fontFamily: 'var(--font-mono)', letterSpacing: '0.08em' }}
                  />
                </div>
                <MagicButton
                  variant="primary"
                  onClick={() => code && onNavigate("home")}
                  disabled={!code}
                >
                  <ArrowRight size={18} />
                  Entrar
                </MagicButton>
              </div>
              <p className="text-xs text-[#4a3d7a] mt-2" style={{ fontFamily: 'var(--font-body)' }}>
                O código é fornecido pelo seu professor. Exemplo: <span className="text-[#8b7db8]">FEITICO-8B</span>
              </p>
            </MagicCard>

            {/* Divisor */}
            <div className="flex items-center gap-4 my-5">
              <div className="flex-1 h-px bg-[rgba(124,58,237,0.15)]" />
              <span className="text-xs text-[#4a3d7a]" style={{ fontFamily: 'var(--font-body)' }}>ou</span>
              <div className="flex-1 h-px bg-[rgba(124,58,237,0.15)]" />
            </div>

            {/* Aguardar professor */}
            <MagicCard className="p-5 flex items-center gap-4">
              <div className="w-11 h-11 rounded-xl bg-[rgba(6,182,212,0.1)] border border-[rgba(6,182,212,0.2)] flex items-center justify-center flex-shrink-0">
                <Users size={20} className="text-[#06b6d4]" />
              </div>
              <div className="flex-1">
                <p className="text-sm font-semibold text-[#e8e0f8] mb-0.5" style={{ fontFamily: 'var(--font-body)' }}>
                  Aguardar convite do professor
                </p>
                <p className="text-xs text-[#8b7db8]" style={{ fontFamily: 'var(--font-body)' }}>
                  Seu professor pode adicionar você à turma pelo e-mail cadastrado.
                </p>
              </div>
              <div className="flex-shrink-0">
                <span className="text-xl">⏳</span>
              </div>
            </MagicCard>

            {/* Dica enquanto espera */}
            <div className="mt-6 p-4 rounded-xl bg-[rgba(212,160,23,0.07)] border border-[rgba(212,160,23,0.18)] flex items-start gap-3">
              <span className="text-xl flex-shrink-0">💡</span>
              <div>
                <p className="text-sm font-semibold text-[#f0c040] mb-1" style={{ fontFamily: 'var(--font-body)' }}>
                  Enquanto você espera…
                </p>
                <p className="text-xs text-[#8b7db8] leading-relaxed" style={{ fontFamily: 'var(--font-body)' }}>
                  Explore o glossário de feitiços ou assista a uma demonstração gratuita para se preparar para sua primeira aula mágica!
                </p>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
