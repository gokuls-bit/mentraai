"use client"
import { getRecommendations } from "@/lib/api"
import { motion } from "framer-motion"
import { CheckCircle2, Timer, Activity } from "lucide-react"

const iconMap = [CheckCircle2, Timer, Activity]

export default function Recommendations() {
  const recs = getRecommendations()
  return (
    <section aria-label="Personalized recommendations" className="gradient-border rounded-xl p-0.5">
      <div className="card-surface rounded-[calc(var(--radius-lg)-2px)] p-4">
        <h2 className="text-balance text-base font-semibold mb-2">Recommendations</h2>
        <ul className="flex flex-col gap-2">
          {recs.map((r, i) => {
            const Icon = iconMap[i % iconMap.length]
            return (
              <motion.li
                key={r.id}
                initial={{ opacity: 0, y: 6 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, amount: 0.3 }}
                transition={{ duration: 0.35, delay: i * 0.06 }}
                className="flex items-start gap-3 rounded-lg p-3 hover:bg-secondary/40 transition-colors"
              >
                <Icon className="h-5 w-5 text-primary mt-0.5" aria-hidden="true" />
                <div className="flex-1">
                  <p className="font-medium">{r.title}</p>
                  <p className="text-sm text-muted-foreground">{r.detail}</p>
                </div>
                {r.action ? (
                  <button
                    className="rounded-md px-3 py-1.5 text-xs bg-primary text-primary-foreground hover:opacity-90 transition-opacity"
                    aria-label={`${r.action} ${r.title}`}
                  >
                    {r.action}
                  </button>
                ) : null}
              </motion.li>
            )
          })}
        </ul>
      </div>
    </section>
  )
}
