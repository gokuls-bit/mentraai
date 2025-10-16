"use client"
import Link from "next/link"
import { motion } from "framer-motion"
import { Sparkles } from "lucide-react"

export default function ARPortal() {
  return (
    <section aria-label="AR Portal" className="gradient-border rounded-xl p-0.5">
      <div className="card-surface rounded-[calc(var(--radius-lg)-2px)] p-4 flex items-center justify-between gap-4">
        <div>
          <h3 className="text-balance text-base font-semibold">AR Portal</h3>
          <p className="text-sm text-muted-foreground">Jump into the AR Lab to visualize concepts spatially.</p>
        </div>
        <motion.div
          initial={{ scale: 0.98, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ duration: 0.4 }}
        >
          <Link
            href="/ar-lab"
            className="group relative inline-flex items-center gap-2 rounded-lg px-4 py-2 bg-primary text-primary-foreground overflow-hidden"
            aria-label="Open AR Lab"
          >
            <span className="relative z-10">Enter</span>
            <Sparkles className="h-4 w-4 relative z-10" aria-hidden="true" />
            <span
              aria-hidden="true"
              className="absolute inset-0 opacity-40 group-hover:opacity-70 transition-opacity"
              style={{
                background:
                  "radial-gradient(60% 120% at 30% 50%, var(--color-chart-2), transparent 60%), radial-gradient(60% 120% at 70% 50%, var(--color-chart-4), transparent 60%)",
              }}
            />
          </Link>
        </motion.div>
      </div>
    </section>
  )
}
