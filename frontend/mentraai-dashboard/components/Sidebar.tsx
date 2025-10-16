"use client"
import Link from "next/link"
import { usePathname } from "next/navigation"
import { motion } from "framer-motion"
import { Activity, Brain, Beaker } from "lucide-react"
import { cn } from "@/lib/utils"

const items = [
  { href: "/dashboard", label: "Dashboard", icon: Activity },
  { href: "/wellness", label: "Wellness", icon: Brain },
  { href: "/ar-lab", label: "AR Lab", icon: Beaker },
]

export function Sidebar() {
  const pathname = usePathname()
  return (
    <aside
      aria-label="Primary"
      className="sticky top-0 h-[100dvh] w-full max-w-[240px] hidden md:flex flex-col gap-2 p-4"
    >
      <div className="gradient-border rounded-xl p-0.5">
        <div className="card-surface rounded-[calc(var(--radius-lg)-2px)] p-4">
          <div className="mb-4">
            <h1 className="text-pretty text-lg font-semibold">MentraAI</h1>
            <p className="text-sm text-muted-foreground">The Empathetic Learning Copilot</p>
          </div>
          <nav role="navigation" aria-label="Main">
            <ul className="flex flex-col gap-1">
              {items.map((it) => {
                const active = pathname.startsWith(it.href)
                const Icon = it.icon
                return (
                  <li key={it.href}>
                    <Link
                      href={it.href}
                      aria-current={active ? "page" : undefined}
                      className={cn(
                        "group flex items-center gap-2 rounded-lg px-3 py-2 text-sm transition-colors",
                        active ? "bg-secondary/60 text-primary" : "hover:bg-secondary/40 text-muted-foreground",
                      )}
                    >
                      <Icon
                        className={cn("h-4 w-4", active ? "text-primary" : "text-muted-foreground")}
                        aria-hidden="true"
                      />
                      <span className="text-pretty">{it.label}</span>
                    </Link>
                  </li>
                )
              })}
            </ul>
          </nav>
        </div>
      </div>

      <motion.div
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4 }}
        className="mt-auto text-xs text-muted-foreground"
      >
        <p>v0 preview • glass theme</p>
      </motion.div>
    </aside>
  )
}
