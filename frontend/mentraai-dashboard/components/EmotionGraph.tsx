"use client"
import { Area, AreaChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts"
import { getEmotionData } from "@/lib/api"
import { motion } from "framer-motion"

export default function EmotionGraph() {
  const data = getEmotionData()
  return (
    <motion.section
      role="figure"
      aria-label="Emotion trends over time"
      initial={{ opacity: 0, y: 8 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, amount: 0.4 }}
      transition={{ duration: 0.5 }}
      className="gradient-border rounded-xl p-0.5"
    >
      <div className="card-surface rounded-[calc(var(--radius-lg)-2px)] p-4">
        <header className="mb-2">
          <h2 className="text-balance text-base font-semibold">Emotion Graph</h2>
          <p className="text-xs text-muted-foreground">Calm, Focus, and Stress signals today</p>
        </header>
        <div className="h-64 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={data} margin={{ left: 8, right: 8 }}>
              <defs>
                <linearGradient id="calm" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor="var(--color-chart-2)" stopOpacity="0.6" />
                  <stop offset="100%" stopColor="var(--color-chart-2)" stopOpacity="0.05" />
                </linearGradient>
                <linearGradient id="focus" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor="var(--color-chart-1)" stopOpacity="0.6" />
                  <stop offset="100%" stopColor="var(--color-chart-1)" stopOpacity="0.05" />
                </linearGradient>
                <linearGradient id="stress" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor="var(--color-chart-5)" stopOpacity="0.6" />
                  <stop offset="100%" stopColor="var(--color-chart-5)" stopOpacity="0.05" />
                </linearGradient>
              </defs>
              <CartesianGrid stroke="oklch(0.35 0 0 / .25)" vertical={false} />
              <XAxis dataKey="time" stroke="oklch(0.7 0 0 / .8)" fontSize={12} />
              <YAxis stroke="oklch(0.7 0 0 / .8)" fontSize={12} />
              <Tooltip
                contentStyle={{
                  background: "oklch(0.2 0 0 / .9)",
                  border: "1px solid oklch(0.4 0 0 / .5)",
                  borderRadius: "10px",
                  color: "white",
                }}
                labelStyle={{ color: "oklch(0.9 0 0)" }}
              />
              <Area type="monotone" dataKey="calm" name="Calm" stroke="var(--color-chart-2)" fill="url(#calm)" />
              <Area type="monotone" dataKey="focus" name="Focus" stroke="var(--color-chart-1)" fill="url(#focus)" />
              <Area type="monotone" dataKey="stress" name="Stress" stroke="var(--color-chart-5)" fill="url(#stress)" />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>
    </motion.section>
  )
}
