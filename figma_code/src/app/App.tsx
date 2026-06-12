import { useState } from "react";
import { LoginScreen } from "./components/LoginScreen";
import { RegisterScreen } from "./components/RegisterScreen";
import { StudentHome } from "./components/StudentHome";
import { EmptyStateScreen } from "./components/EmptyStateScreen";
import { GrimorioDetailScreen } from "./components/GrimorioDetailScreen";
import { SpellExerciseScreen } from "./components/SpellExerciseScreen";
import { TeacherLayout } from "./components/teacher/TeacherLayout";
import { TeacherDashboard } from "./components/teacher/TeacherDashboard";
import { TeacherGuildDetail } from "./components/teacher/TeacherGuildDetail";
import { TeacherProgress } from "./components/teacher/TeacherProgress";

type Screen =
  | "login" | "register"
  | "home" | "empty" | "grimorio" | "feitico"
  | "teacher-dashboard" | "teacher-guilda" | "teacher-progresso";

const STUDENT_SCREENS = [
  { id: "login"    as Screen, label: "1 Login"     },
  { id: "register" as Screen, label: "2 Registro"  },
  { id: "home"     as Screen, label: "3 Início"    },
  { id: "empty"    as Screen, label: "4 Sem turma" },
  { id: "grimorio" as Screen, label: "5 Grimório"  },
  { id: "feitico"  as Screen, label: "6 Feitiço"   },
];

const TEACHER_SCREENS = [
  { id: "teacher-dashboard" as Screen, label: "7 Dashboard Prof." },
  { id: "teacher-guilda"    as Screen, label: "8 Guilda"          },
  { id: "teacher-progresso" as Screen, label: "9 Progresso"       },
];

const TEACHER_NAV_MAP: Record<string, Screen> = {
  dashboard: "teacher-dashboard",
  guildas:   "teacher-guilda",
  progresso: "teacher-progresso",
  grimorios: "teacher-dashboard",
};

export default function App() {
  const [screen, setScreen] = useState<Screen>("login");

  function navigate(target: string) {
    const all = [...STUDENT_SCREENS, ...TEACHER_SCREENS];
    if (all.find((s) => s.id === target)) {
      setScreen(target as Screen);
    } else if (TEACHER_NAV_MAP[target]) {
      setScreen(TEACHER_NAV_MAP[target]);
    }
  }

  const isTeacher = screen.startsWith("teacher-");

  const activeTeacherTab =
    screen === "teacher-dashboard" ? "dashboard"
    : screen === "teacher-guilda"  ? "guildas"
    : screen === "teacher-progresso" ? "progresso"
    : "dashboard";

  return (
    <div className="relative">
      {/* Pill de navegação entre telas */}
      <div
        className="fixed bottom-4 left-1/2 -translate-x-1/2 z-[9999] flex items-center gap-0.5 px-2 py-1.5 rounded-2xl shadow-2xl"
        style={{
          background: "rgba(13, 10, 30, 0.96)",
          border: "1px solid rgba(124, 58, 237, 0.4)",
          backdropFilter: "blur(16px)",
        }}
      >
        {/* Grupo aluno */}
        <span className="text-[9px] text-[#4a3d7a] px-2 uppercase tracking-wider" style={{ fontFamily: "var(--font-mono)" }}>Aluno</span>
        {STUDENT_SCREENS.map((s) => (
          <button
            key={s.id}
            onClick={() => setScreen(s.id)}
            className="px-3 py-1.5 rounded-xl text-xs font-semibold transition-all duration-150 cursor-pointer"
            style={{
              fontFamily: "var(--font-body)",
              background: screen === s.id ? "rgba(124, 58, 237, 0.85)" : "transparent",
              color: screen === s.id ? "#ffffff" : "#8b7db8",
            }}
          >
            {s.label}
          </button>
        ))}

        <div className="w-px h-5 bg-[rgba(124,58,237,0.25)] mx-1" />

        {/* Grupo professor */}
        <span className="text-[9px] text-[#4a3d7a] px-2 uppercase tracking-wider" style={{ fontFamily: "var(--font-mono)" }}>Prof.</span>
        {TEACHER_SCREENS.map((s) => (
          <button
            key={s.id}
            onClick={() => setScreen(s.id)}
            className="px-3 py-1.5 rounded-xl text-xs font-semibold transition-all duration-150 cursor-pointer"
            style={{
              fontFamily: "var(--font-body)",
              background: screen === s.id ? "rgba(212, 160, 23, 0.75)" : "transparent",
              color: screen === s.id ? "#0d0a1e" : "#8b7db8",
            }}
          >
            {s.label}
          </button>
        ))}
      </div>

      {/* Telas do aluno */}
      {screen === "login"    && <LoginScreen           onNavigate={navigate} />}
      {screen === "register" && <RegisterScreen        onNavigate={navigate} />}
      {screen === "home"     && <StudentHome           onNavigate={navigate} />}
      {screen === "empty"    && <EmptyStateScreen      onNavigate={navigate} />}
      {screen === "grimorio" && <GrimorioDetailScreen  onNavigate={navigate} />}
      {screen === "feitico"  && <SpellExerciseScreen   onNavigate={navigate} />}

      {/* Telas do professor — envolvidas no layout compartilhado */}
      {isTeacher && (
        <TeacherLayout activeScreen={activeTeacherTab} onNavigate={navigate}>
          {screen === "teacher-dashboard" && <TeacherDashboard onNavigate={navigate} />}
          {screen === "teacher-guilda"    && <TeacherGuildDetail onNavigate={navigate} />}
          {screen === "teacher-progresso" && <TeacherProgress  onNavigate={navigate} />}
        </TeacherLayout>
      )}
    </div>
  );
}
