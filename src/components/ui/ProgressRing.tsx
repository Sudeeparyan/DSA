"use client";

export function ProgressRing({
  value,
  total,
  size = 120,
}: {
  value: number;
  total: number;
  size?: number;
}) {
  const pct = total === 0 ? 0 : Math.min(1, value / total);
  const stroke = Math.max(8, size / 12);
  const r = (size - stroke) / 2;
  const c = 2 * Math.PI * r;
  const offset = c * (1 - pct);

  return (
    <div
      className="relative inline-flex items-center justify-center"
      style={{ width: size, height: size }}
      role="img"
      aria-label={`${value} of ${total} understood`}
    >
      <svg width={size} height={size} className="-rotate-90">
        <circle
          cx={size / 2}
          cy={size / 2}
          r={r}
          fill="none"
          stroke="var(--border)"
          strokeWidth={stroke}
        />
        <circle
          cx={size / 2}
          cy={size / 2}
          r={r}
          fill="none"
          stroke="var(--accent)"
          strokeWidth={stroke}
          strokeLinecap="round"
          strokeDasharray={c}
          strokeDashoffset={offset}
        />
      </svg>
      <div className="absolute text-center">
        <div className="brand-font text-lg font-extrabold leading-none sm:text-xl">
          {value}
          <span className="text-muted">/{total}</span>
        </div>
        <div className="mt-1 text-[10px] font-semibold uppercase tracking-wide text-muted">
          done
        </div>
      </div>
    </div>
  );
}
