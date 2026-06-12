import { ReactNode } from "react";

interface MagicCardProps {
  children: ReactNode;
  className?: string;
  glow?: boolean;
  gold?: boolean;
}

export function MagicCard({ children, className = "", glow = false, gold = false }: MagicCardProps) {
  const glowColor = gold
    ? "shadow-[0_0_20px_rgba(212,160,23,0.12)] border-[rgba(212,160,23,0.25)]"
    : glow
    ? "shadow-[0_0_24px_rgba(124,58,237,0.18)] border-[rgba(124,58,237,0.35)]"
    : "border-[rgba(124,58,237,0.2)]";

  return (
    <div
      className={`rounded-xl border bg-[#16112e] ${glowColor} transition-all duration-200 ${className}`}
    >
      {children}
    </div>
  );
}

interface MagicInputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  icon?: ReactNode;
}

export function MagicInput({ label, icon, className = "", ...props }: MagicInputProps) {
  return (
    <div className="flex flex-col gap-1.5">
      {label && (
        <label className="text-sm text-[#c4b5fd] font-medium" style={{ fontFamily: 'var(--font-body)' }}>
          {label}
        </label>
      )}
      <div className="relative">
        {icon && (
          <div className="absolute left-3 top-1/2 -translate-y-1/2 text-[#8b7db8]">
            {icon}
          </div>
        )}
        <input
          className={`w-full bg-[#1e1540] border border-[rgba(124,58,237,0.3)] rounded-lg text-[#e8e0f8] placeholder-[#4a3d7a]
            focus:outline-none focus:border-[#7c3aed] focus:ring-2 focus:ring-[rgba(124,58,237,0.25)]
            transition-all duration-200 ${icon ? "pl-10 pr-4 py-3" : "px-4 py-3"} ${className}`}
          style={{ fontFamily: 'var(--font-body)' }}
          {...props}
        />
      </div>
    </div>
  );
}

interface MagicButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "ghost" | "gold" | "danger";
  size?: "sm" | "md" | "lg";
  children: ReactNode;
  fullWidth?: boolean;
}

export function MagicButton({
  variant = "primary",
  size = "md",
  children,
  fullWidth = false,
  className = "",
  ...props
}: MagicButtonProps) {
  const variants = {
    primary:
      "bg-[#7c3aed] hover:bg-[#6d28d9] text-white shadow-[0_4px_14px_rgba(124,58,237,0.4)] hover:shadow-[0_4px_20px_rgba(124,58,237,0.55)]",
    secondary:
      "bg-[#2d1f5e] hover:bg-[#3d2a7a] text-[#c4b5fd] border border-[rgba(124,58,237,0.35)]",
    ghost:
      "bg-transparent hover:bg-[rgba(124,58,237,0.1)] text-[#c4b5fd] border border-[rgba(124,58,237,0.2)]",
    gold:
      "bg-[#d4a017] hover:bg-[#e6b020] text-[#0d0a1e] shadow-[0_4px_14px_rgba(212,160,23,0.35)]",
    danger:
      "bg-[#c0392b] hover:bg-[#a93226] text-white shadow-[0_4px_14px_rgba(192,57,43,0.35)]",
  };
  const sizes = {
    sm: "px-3 py-1.5 text-sm rounded-lg",
    md: "px-5 py-2.5 rounded-xl",
    lg: "px-7 py-3.5 rounded-xl",
  };

  return (
    <button
      className={`
        inline-flex items-center justify-center gap-2 font-semibold
        transition-all duration-200 active:scale-[0.97] cursor-pointer
        focus:outline-none focus:ring-2 focus:ring-[rgba(124,58,237,0.4)] focus:ring-offset-1 focus:ring-offset-[#0d0a1e]
        disabled:opacity-50 disabled:cursor-not-allowed
        ${variants[variant]} ${sizes[size]} ${fullWidth ? "w-full" : ""} ${className}
      `}
      style={{ fontFamily: 'var(--font-body)' }}
      {...props}
    >
      {children}
    </button>
  );
}

interface BadgeProps {
  children: ReactNode;
  variant?: "purple" | "gold" | "cyan" | "green" | "red" | "gray";
  size?: "sm" | "md";
}

export function MagicBadge({ children, variant = "purple", size = "sm" }: BadgeProps) {
  const variants = {
    purple: "bg-[rgba(124,58,237,0.2)] text-[#c4b5fd] border-[rgba(124,58,237,0.35)]",
    gold: "bg-[rgba(212,160,23,0.15)] text-[#f0c040] border-[rgba(212,160,23,0.35)]",
    cyan: "bg-[rgba(6,182,212,0.15)] text-[#67e8f9] border-[rgba(6,182,212,0.35)]",
    green: "bg-[rgba(34,197,94,0.15)] text-[#86efac] border-[rgba(34,197,94,0.35)]",
    red: "bg-[rgba(239,68,68,0.15)] text-[#fca5a5] border-[rgba(239,68,68,0.35)]",
    gray: "bg-[rgba(139,125,184,0.15)] text-[#8b7db8] border-[rgba(139,125,184,0.25)]",
  };
  const sizes = {
    sm: "text-xs px-2 py-0.5",
    md: "text-sm px-3 py-1",
  };

  return (
    <span
      className={`inline-flex items-center gap-1 rounded-full border font-semibold ${variants[variant]} ${sizes[size]}`}
      style={{ fontFamily: 'var(--font-body)' }}
    >
      {children}
    </span>
  );
}

interface ProgressBarProps {
  value: number;
  max?: number;
  color?: "purple" | "gold" | "cyan" | "green";
  showLabel?: boolean;
  label?: string;
  size?: "xs" | "sm" | "md";
}

export function MagicProgress({ value, max = 100, color = "purple", showLabel = false, label, size = "sm" }: ProgressBarProps) {
  const pct = Math.min(100, Math.max(0, (value / max) * 100));
  const colors = {
    purple: "bg-[#7c3aed] shadow-[0_0_8px_rgba(124,58,237,0.5)]",
    gold: "bg-[#d4a017] shadow-[0_0_8px_rgba(212,160,23,0.5)]",
    cyan: "bg-[#06b6d4] shadow-[0_0_8px_rgba(6,182,212,0.5)]",
    green: "bg-[#22c55e] shadow-[0_0_8px_rgba(34,197,94,0.5)]",
  };
  const heights = {
    xs: "h-1",
    sm: "h-2",
    md: "h-3",
  };

  return (
    <div className="flex flex-col gap-1 w-full">
      {(showLabel || label) && (
        <div className="flex justify-between items-center text-xs text-[#8b7db8]" style={{ fontFamily: 'var(--font-body)' }}>
          {label && <span>{label}</span>}
          {showLabel && <span>{Math.round(pct)}%</span>}
        </div>
      )}
      <div className={`w-full bg-[#1e1540] rounded-full overflow-hidden ${heights[size]}`}>
        <div
          className={`${heights[size]} rounded-full transition-all duration-500 ${colors[color]}`}
          style={{ width: `${pct}%` }}
        />
      </div>
    </div>
  );
}
