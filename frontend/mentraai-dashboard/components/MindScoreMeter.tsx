"use client"
import { motion } from "framer-motion"

type Props = {
  score: number // 0..100
  label?: string
}

export default function MindScoreMeter({ score, label = "MindScore" }: Props) {
  const size = 160
  const stroke = 10
  const r = (size - stroke) / 2
  const circumference = 2 * Math.PI * r
  const progress = Math.max(0, Math.min(100, score))
  const offset = circumference - (progress / 100) * circumference

  return (
    <section aria-label={`${label}: ${progress}%`} className="gradient-border rounded-xl p-0.5">
      <div className="card-surface rounded-[calc(var(--radius-lg)-2px)] p-4 flex items-center justify-center">
        <div
          className="relative"
          role="img"
          aria-roledescription="circular progress"
          aria-valuemin={0}
          aria-valuemax={100}
          aria-valuenow={progress}
        >
          <svg width={size} height={size} role="presentation">
            <circle cx={size / 2} cy={size / 2} r={r} stroke="oklch(0.35 0 0 / .35)" strokeWidth={stroke} fill="none" />
            <motion.circle
              cx={size / 2}
              cy={size / 2}
              r={r}
              stroke="var(--color-chart-1)"
              strokeWidth={stroke}
              strokeLinecap="round"
              fill="none"
              initial={{ strokeDasharray: circumference, strokeDashoffset: circumference }}
              animate={{ strokeDashoffset: offset }}
              transition={{ duration: 1.1, ease: "easeOut" }}
              style={{ filter: "drop-shadow(0 0 8px oklch(0.7 0.15 250 / .6))" }}
            />
          </svg>
          <div className="absolute inset-0 grid place-items-center">
            <div className="text-center">
              <p className="text-xs text-muted-foreground">{label}</p>
              <p className="text-3xl font-semibold">{progress}%</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
