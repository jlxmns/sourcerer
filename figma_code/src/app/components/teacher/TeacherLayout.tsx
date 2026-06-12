import { ReactNode, useState } from "react";
import {
  LayoutDashboard, Users, BookOpen, TrendingUp, Bell, Settings,
  ChevronDown, LogOut, Menu, X, Sparkles,
} from "lucide-react";

const NAV_ITEMS = [
  { id: "dashboard", label: "Dashboard",    icon: LayoutDashboard },
  { id: "guildas",   label: "Guildas",      icon: Users           },
  { id: "progresso", label: "Progresso",    icon: TrendingUp      },
  { id: "grimorios", label: "Grimórios",    icon: BookOpen        },
];

interface TeacherLayoutProps {
  children: ReactNode;
  activeScreen: string;
  onNavigate: (screen: string) => void;
}

export function TeacherLayout({ children, activeScreen, onNavigate }: TeacherLayoutProps) {
  const [sidebarOpen, setSidebarOpen] = useState(true);

  return (
    <div className="min-h-screen bg-[#0d0a1e] flex">
      {/* Sidebar de navegação */}
      <aside
        className={`flex-shrink-0 flex flex-col bg-[#100d24] border-r border-[rgba(124,58,237,0.18)] transition-all duration-200 ${
          sidebarOpen ? "w-56" : "w-16"
        }`}
      >
        {/* Logo */}
        <div className="h-16 flex items-center gap-3 px-4 border-b border-[rgba(124,58,237,0.15)]">
          <div className="w-8 h-8 rounded-lg bg-[#7c3aed] flex items-center justify-center text-lg flex-shrink-0 shadow-[0_0_10px_rgba(124,58,237,0.45)]">
            🧙
          </div>
          {sidebarOpen && (
            <span className="text-white text-base" style={{ fontFamily: "var(--font-display)", letterSpacing: "0.05em" }}>
              Sourcerer
            </span>
          )}
          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="ml-auto text-[#8b7db8] hover:text-[#c4b5fd] transition-colors cursor-pointer"
          >
            {sidebarOpen ? <X size={16} /> : <Menu size={16} />}
          </button>
        </div>

        {/* Perfil do professor */}
        {sidebarOpen && (
          <div className="px-3 py-4 border-b border-[rgba(124,58,237,0.12)]">
            <div className="flex items-center gap-2.5 px-2 py-2 rounded-lg bg-[rgba(124,58,237,0.07)]">
              <div className="w-8 h-8 rounded-full bg-gradient-to-br from-[#7c3aed] to-[#4c1d95] flex items-center justify-center text-sm flex-shrink-0">
                👩‍🏫
              </div>
              <div className="min-w-0">
                <p className="text-xs font-semibold text-[#e8e0f8] truncate" style={{ fontFamily: "var(--font-body)" }}>
                  Profa. Camila Ramos
                </p>
                <p className="text-[10px] text-[#8b7db8]" style={{ fontFamily: "var(--font-body)" }}>
                  Professora
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Itens de navegação */}
        <nav className="flex-1 px-2 py-3 space-y-0.5">
          {NAV_ITEMS.map(({ id, label, icon: Icon }) => {
            const isActive = activeScreen === id;
            return (
              <button
                key={id}
                onClick={() => onNavigate(id)}
                className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-150 cursor-pointer group ${
                  isActive
                    ? "bg-[rgba(124,58,237,0.2)] text-[#c4b5fd] border border-[rgba(124,58,237,0.3)]"
                    : "text-[#8b7db8] hover:bg-[rgba(124,58,237,0.08)] hover:text-[#c4b5fd]"
                }`}
                style={{ fontFamily: "var(--font-body)" }}
                title={!sidebarOpen ? label : undefined}
              >
                <Icon size={16} className="flex-shrink-0" />
                {sidebarOpen && <span>{label}</span>}
                {isActive && sidebarOpen && (
                  <span className="ml-auto w-1.5 h-1.5 rounded-full bg-[#7c3aed]" />
                )}
              </button>
            );
          })}
        </nav>

        {/* Rodapé da sidebar */}
        <div className="px-2 pb-4 space-y-0.5 border-t border-[rgba(124,58,237,0.12)] pt-3">
          <button
            className="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm text-[#8b7db8] hover:bg-[rgba(124,58,237,0.08)] hover:text-[#c4b5fd] transition-colors cursor-pointer"
            style={{ fontFamily: "var(--font-body)" }}
          >
            <Settings size={16} className="flex-shrink-0" />
            {sidebarOpen && <span>Configurações</span>}
          </button>
          <button
            className="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm text-[#8b7db8] hover:bg-[rgba(239,68,68,0.08)] hover:text-[#fca5a5] transition-colors cursor-pointer"
            style={{ fontFamily: "var(--font-body)" }}
          >
            <LogOut size={16} className="flex-shrink-0" />
            {sidebarOpen && <span>Sair</span>}
          </button>
        </div>
      </aside>

      {/* Conteúdo principal */}
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
        {/* Header superior */}
        <header className="h-16 flex items-center gap-4 px-6 bg-[#100d24] border-b border-[rgba(124,58,237,0.18)] flex-shrink-0">
          <div>
            <h1 className="text-base text-[#e8e0f8]" style={{ fontFamily: "var(--font-display)", fontSize: "0.9rem" }}>
              {NAV_ITEMS.find((n) => n.id === activeScreen)?.label ?? "Dashboard"}
            </h1>
            <p className="text-xs text-[#8b7db8]" style={{ fontFamily: "var(--font-body)" }}>
              Ano letivo 2025 · EMEF Monteiro Lobato
            </p>
          </div>

          <div className="ml-auto flex items-center gap-3">
            {/* Notificações */}
            <button className="relative w-9 h-9 rounded-lg hover:bg-[rgba(124,58,237,0.1)] flex items-center justify-center text-[#8b7db8] hover:text-[#c4b5fd] transition-colors cursor-pointer">
              <Bell size={17} />
              <span className="absolute top-1.5 right-1.5 w-2 h-2 rounded-full bg-[#7c3aed]" />
            </button>

            {/* Usuário */}
            <button className="flex items-center gap-2 px-3 py-1.5 rounded-lg hover:bg-[rgba(124,58,237,0.08)] transition-colors cursor-pointer group">
              <div className="w-7 h-7 rounded-full bg-gradient-to-br from-[#7c3aed] to-[#4c1d95] flex items-center justify-center text-sm">
                👩‍🏫
              </div>
              <span className="text-sm text-[#e8e0f8] hidden sm:block" style={{ fontFamily: "var(--font-body)" }}>
                Camila Ramos
              </span>
              <ChevronDown size={13} className="text-[#8b7db8] group-hover:text-[#c4b5fd] transition-colors" />
            </button>
          </div>
        </header>

        {/* Área de conteúdo */}
        <div className="flex-1 overflow-y-auto">
          {children}
        </div>
      </div>
    </div>
  );
}
