"use client"
import { motion } from "framer-motion"

export default function AIAvatar() {
  return (
    <section aria-label="MentraAI Avatar" className="gradient-border rounded-xl p-0.5">
      <div className="card-surface rounded-[calc(var(--radius-lg)-2px)] p-4 flex flex-col items-center text-center">
        <motion.div
          initial={{ opacity: 0, y: 6, scale: 0.98 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          transition={{ duration: 0.5 }}
          className="relative"
        >
          <motion.div
            className="glow absolute inset-0 rounded-full"
            aria-hidden="true"
            style={{ filter: "blur(24px)" }}
            animate={{ opacity: [0.5, 0.9, 0.6, 0.8] }}
            transition={{ duration: 4, repeat: Number.POSITIVE_INFINITY, repeatType: "mirror" }}
          />
          <motion.img
            src="/ai-avatar-neon-glow.jpg"
            alt="MentraAI empathetic avatar"
            width={160}
            height={160}
            className="relative rounded-full border border-border"
            style={{ imageRendering: "auto" }}
            animate={{ y: [0, -4, 0] }}
            transition={{ duration: 4, repeat: Number.POSITIVE_INFINITY, ease: "easeInOut" }}
          />
        </motion.div>
        <div className="mt-4">
          <h2 className="text-base font-semibold">MentraAI</h2>
          <p className="text-sm text-muted-foreground">Empathetic Learning Copilot</p>
        </div>
      </div>
    </section>
  )
}
