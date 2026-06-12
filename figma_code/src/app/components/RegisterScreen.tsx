import { useState } from "react";
import { Mail, Lock, User, Eye, EyeOff, Sparkles } from "lucide-react";
import { MagicButton, MagicInput } from "./ui/MagicCard";

interface RegisterScreenProps {
  onNavigate: (screen: string) => void;
}

export function RegisterScreen({ onNavigate }: RegisterScreenProps) {
  const [showPass, setShowPass] = useState(false);

  return (
    <div className="min-h-screen bg-[#0d0a1e] flex items-stretch overflow-hidden">
      {/* Painel esquerdo */}
      <div className="hidden lg:flex lg:w-[40%] relative flex-col items-center justify-center p-12 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-[#1a0e3d] via-[#0d0a1e] to-[#0a0818]" />
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_40%_50%,rgba(124,58,237,0.2)_0%,transparent_65%)]" />
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_80%_80%,rgba(6,182,212,0.07)_0%,transparent_50%)]" />

        {/* Partículas decorativas */}
        {[...Array(8)].map((_, i) => (
          <div
            key={i}
            className="absolute w-1 h-1 rounded-full bg-[#7c3aed] opacity-40"
            style={{
              top: `${15 + i * 10}%`,
              left: `${10 + (i % 3) * 25}%`,
              boxShadow: '0 0 6px rgba(124,58,237,0.8)',
            }}
          />
        ))}

        <div className="relative z-10 text-center">
          <div className="w-20 h-20 mx-auto mb-5 rounded-2xl bg-gradient-to-br from-[#7c3aed] to-[#4c1d95] flex items-center justify-center text-4xl shadow-[0_0_36px_rgba(124,58,237,0.4)]">
            🧙
          </div>
          <h1 className="text-3xl text-white mb-3" style={{ fontFamily: 'var(--font-display)', letterSpacing: '0.08em' }}>
            Sourcerer
          </h1>
          <p className="text-[#8b7db8] max-w-xs mx-auto text-sm leading-relaxed" style={{ fontFamily: 'var(--font-body)' }}>
            Junte-se a milhares de estudantes que aprendem programação através da magia.
          </p>

          <div className="mt-8 space-y-3 max-w-xs mx-auto text-left">
            {[
              { icon: "🎓", title: "Aprenda enquanto joga", desc: "Exercícios transformados em feitiços" },
              { icon: "🏆", title: "Compete com sua turma", desc: "Rankings, badges e recompensas" },
              { icon: "🔮", title: "Progresso real", desc: "Pensamento computacional de verdade" },
            ].map((f) => (
              <div key={f.title} className="flex items-start gap-3 p-3 rounded-xl bg-[rgba(124,58,237,0.07)] border border-[rgba(124,58,237,0.12)]">
                <span className="text-xl flex-shrink-0">{f.icon}</span>
                <div>
                  <p className="text-sm text-[#e8e0f8] font-semibold" style={{ fontFamily: 'var(--font-body)' }}>{f.title}</p>
                  <p className="text-xs text-[#8b7db8]" style={{ fontFamily: 'var(--font-body)' }}>{f.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Painel direito — formulário */}
      <div className="flex-1 flex flex-col items-center justify-center px-6 py-10 bg-[#100d24] relative overflow-y-auto">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_50%_0%,rgba(124,58,237,0.07)_0%,transparent_60%)]" />
        <div className="relative z-10 w-full max-w-sm">
          <div className="flex items-center gap-3 mb-6 lg:hidden">
            <div className="w-9 h-9 rounded-xl bg-[#7c3aed] flex items-center justify-center text-xl">🧙</div>
            <span className="text-lg text-white" style={{ fontFamily: 'var(--font-display)', letterSpacing: '0.06em' }}>Sourcerer</span>
          </div>

          <h2 className="text-2xl text-[#e8e0f8] mb-1" style={{ fontFamily: 'var(--font-display)' }}>
            Criar sua conta
          </h2>
          <p className="text-sm text-[#8b7db8] mb-6" style={{ fontFamily: 'var(--font-body)' }}>
            Preencha seus dados para começar a jornada.
          </p>

          <div className="space-y-4">
            <MagicInput
              label="Nome completo"
              type="text"
              placeholder="Seu nome"
              icon={<User size={16} />}
            />
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
                placeholder="Crie uma senha segura"
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
            {/* Força da senha */}
            <div className="space-y-1">
              <div className="flex gap-1">
                {[1, 2, 3, 4].map((i) => (
                  <div
                    key={i}
                    className={`flex-1 h-1 rounded-full ${i <= 2 ? "bg-[#7c3aed]" : "bg-[#1e1540]"}`}
                  />
                ))}
              </div>
              <p className="text-xs text-[#8b7db8]" style={{ fontFamily: 'var(--font-body)' }}>Senha moderada</p>
            </div>

            <label className="flex items-start gap-2 cursor-pointer group">
              <input
                type="checkbox"
                className="w-4 h-4 mt-0.5 rounded border border-[rgba(124,58,237,0.4)] bg-[#1e1540] accent-[#7c3aed] cursor-pointer flex-shrink-0"
              />
              <span className="text-sm text-[#8b7db8] group-hover:text-[#c4b5fd] transition-colors leading-relaxed" style={{ fontFamily: 'var(--font-body)' }}>
                Concordo com os{" "}
                <span className="text-[#7c3aed] hover:text-[#a78bfa] cursor-pointer">Termos de Uso</span>{" "}
                e a{" "}
                <span className="text-[#7c3aed] hover:text-[#a78bfa] cursor-pointer">Política de Privacidade</span>
              </span>
            </label>

            <MagicButton variant="primary" size="lg" fullWidth onClick={() => onNavigate("home")}>
              <Sparkles size={18} />
              Criar Conta
            </MagicButton>
          </div>

          <div className="mt-5 text-center">
            <p className="text-sm text-[#8b7db8]" style={{ fontFamily: 'var(--font-body)' }}>
              Já tem uma conta?{" "}
              <button
                onClick={() => onNavigate("login")}
                className="text-[#7c3aed] hover:text-[#a78bfa] font-semibold transition-colors cursor-pointer"
              >
                Entrar
              </button>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
