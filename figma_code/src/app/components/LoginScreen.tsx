import { useState } from "react";
import { Mail, Lock, Eye, EyeOff, Sparkles } from "lucide-react";
import { MagicButton, MagicInput } from "./ui/MagicCard";

interface LoginScreenProps {
  onNavigate: (screen: string) => void;
}

export function LoginScreen({ onNavigate }: LoginScreenProps) {
  const [showPass, setShowPass] = useState(false);

  return (
    <div className="min-h-screen bg-[#0d0a1e] flex items-stretch overflow-hidden">
      {/* Painel esquerdo — visual mágico */}
      <div className="hidden lg:flex lg:w-1/2 xl:w-[55%] relative flex-col items-center justify-center p-12 overflow-hidden">
        {/* Fundo com gradiente */}
        <div className="absolute inset-0 bg-gradient-to-br from-[#1a0e3d] via-[#0d0a1e] to-[#0a0818]" />
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_60%_40%,rgba(124,58,237,0.22)_0%,transparent_60%)]" />
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_20%_80%,rgba(6,182,212,0.08)_0%,transparent_50%)]" />

        {/* Runas decorativas */}
        <div className="absolute top-12 left-12 text-5xl opacity-10 select-none" style={{ fontFamily: 'var(--font-display)' }}>ᚠ</div>
        <div className="absolute top-32 right-20 text-3xl opacity-8 select-none" style={{ fontFamily: 'var(--font-display)' }}>ᚢ</div>
        <div className="absolute bottom-24 left-24 text-4xl opacity-10 select-none" style={{ fontFamily: 'var(--font-display)' }}>ᚱ</div>
        <div className="absolute bottom-16 right-16 text-5xl opacity-8 select-none" style={{ fontFamily: 'var(--font-display)' }}>ᚦ</div>

        {/* Círculo mágico SVG */}
        <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
          <svg width="500" height="500" viewBox="0 0 500 500" className="opacity-[0.06]">
            <circle cx="250" cy="250" r="220" fill="none" stroke="#7c3aed" strokeWidth="1" />
            <circle cx="250" cy="250" r="180" fill="none" stroke="#7c3aed" strokeWidth="0.5" strokeDasharray="4 8" />
            <circle cx="250" cy="250" r="140" fill="none" stroke="#06b6d4" strokeWidth="0.5" />
            <polygon points="250,50 460,370 40,370" fill="none" stroke="#7c3aed" strokeWidth="0.5" />
            <polygon points="250,450 40,130 460,130" fill="none" stroke="#7c3aed" strokeWidth="0.5" />
          </svg>
        </div>

        {/* Conteúdo central */}
        <div className="relative z-10 text-center">
          <div className="w-24 h-24 mx-auto mb-6 rounded-2xl bg-gradient-to-br from-[#7c3aed] to-[#4c1d95] flex items-center justify-center text-5xl shadow-[0_0_40px_rgba(124,58,237,0.45)]">
            🧙
          </div>
          <h1 className="text-4xl text-white mb-3" style={{ fontFamily: 'var(--font-display)', letterSpacing: '0.08em' }}>
            Sourcerer
          </h1>
          <p className="text-[#8b7db8] max-w-xs mx-auto text-base leading-relaxed" style={{ fontFamily: 'var(--font-body)' }}>
            A plataforma de pensamento computacional que transforma código em magia.
          </p>

          <div className="mt-10 grid grid-cols-3 gap-4 max-w-sm mx-auto">
            {[
              { icon: "📚", label: "Grimórios de aprendizado" },
              { icon: "✨", label: "Feitiços de código" },
              { icon: "🏆", label: "Competição e ranking" },
            ].map((f) => (
              <div key={f.label} className="flex flex-col items-center gap-2 p-3 rounded-xl bg-[rgba(124,58,237,0.08)] border border-[rgba(124,58,237,0.15)]">
                <span className="text-2xl">{f.icon}</span>
                <span className="text-xs text-[#8b7db8] text-center leading-tight" style={{ fontFamily: 'var(--font-body)' }}>{f.label}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Painel direito — formulário */}
      <div className="flex-1 flex flex-col items-center justify-center px-6 py-12 bg-[#100d24] relative">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_50%_0%,rgba(124,58,237,0.08)_0%,transparent_60%)]" />
        <div className="relative z-10 w-full max-w-sm">
          {/* Logo mobile */}
          <div className="flex items-center gap-3 mb-8 lg:hidden">
            <div className="w-10 h-10 rounded-xl bg-[#7c3aed] flex items-center justify-center text-2xl shadow-[0_0_14px_rgba(124,58,237,0.5)]">
              🧙
            </div>
            <span className="text-xl text-white" style={{ fontFamily: 'var(--font-display)', letterSpacing: '0.06em' }}>
              Sourcerer
            </span>
          </div>

          <h2 className="text-2xl text-[#e8e0f8] mb-1" style={{ fontFamily: 'var(--font-display)' }}>
            Bem-vindo de volta
          </h2>
          <p className="text-sm text-[#8b7db8] mb-8" style={{ fontFamily: 'var(--font-body)' }}>
            Entre na sua conta para continuar sua jornada arcana.
          </p>

          <div className="space-y-5">
            <MagicInput
              label="E-mail"
              type="email"
              placeholder="seu@email.com"
              icon={<Mail size={16} />}
            />
            <div className="relative">
              <MagicInput
                label="Senha"
                type={showPass ? "text" : "password"}
                placeholder="Sua senha secreta"
                icon={<Lock size={16} />}
              />
              <button
                type="button"
                onClick={() => setShowPass(!showPass)}
                className="absolute right-3 bottom-3 text-[#8b7db8] hover:text-[#c4b5fd] transition-colors cursor-pointer"
              >
                {showPass ? <EyeOff size={16} /> : <Eye size={16} />}
              </button>
            </div>

            <div className="flex items-center justify-between">
              <label className="flex items-center gap-2 cursor-pointer group">
                <input
                  type="checkbox"
                  className="w-4 h-4 rounded border border-[rgba(124,58,237,0.4)] bg-[#1e1540] accent-[#7c3aed] cursor-pointer"
                />
                <span className="text-sm text-[#8b7db8] group-hover:text-[#c4b5fd] transition-colors" style={{ fontFamily: 'var(--font-body)' }}>
                  Lembrar de mim
                </span>
              </label>
              <button className="text-sm text-[#7c3aed] hover:text-[#a78bfa] transition-colors cursor-pointer" style={{ fontFamily: 'var(--font-body)' }}>
                Esqueci a senha
              </button>
            </div>

            <MagicButton
              variant="primary"
              size="lg"
              fullWidth
              onClick={() => onNavigate("home")}
            >
              <Sparkles size={18} />
              Entrar
            </MagicButton>
          </div>

          <div className="mt-6 text-center">
            <p className="text-sm text-[#8b7db8]" style={{ fontFamily: 'var(--font-body)' }}>
              Ainda não tem conta?{" "}
              <button
                onClick={() => onNavigate("register")}
                className="text-[#7c3aed] hover:text-[#a78bfa] font-semibold transition-colors cursor-pointer"
              >
                Criar conta
              </button>
            </p>
          </div>

          <div className="mt-8 pt-6 border-t border-[rgba(124,58,237,0.15)] text-center">
            <p className="text-xs text-[#4a3d7a]" style={{ fontFamily: 'var(--font-body)' }}>
              Sourcerer — Plataforma educacional para escolas públicas brasileiras
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
