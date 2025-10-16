import Link from "next/link"
import { Sidebar } from "@/components/Sidebar"

export const metadata = {
  title: "MentraAI • AR Lab",
}

export default function ARLabPage() {
  return (
    <main className="min-h-[100dvh]">
      <div className="mx-auto max-w-7xl grid grid-cols-1 md:grid-cols-[240px,1fr] gap-6 p-4 md:p-6">
        <Sidebar />
        <section className="flex flex-col gap-6">
          <header>
            <h1 className="text-balance text-xl font-semibold">AR Lab</h1>
            <p className="text-sm text-muted-foreground">
              Prototype portal for spatial learning. Visualize concepts with depth and motion.
            </p>
          </header>

          <div className="gradient-border rounded-xl p-0.5">
            <div className="card-surface rounded-[calc(var(--radius-lg)-2px)] p-6">
              <p className="text-pretty leading-relaxed">
                This AR Lab surface is a placeholder for integrating WebXR or 3D scenes. Use it to explore empathetic
                feedback loops in a spatial context.
              </p>
              <ul className="mt-4 list-disc pl-5 text-sm text-muted-foreground">
                <li>Highlight attention paths</li>
                <li>Project guided breathing visuals</li>
                <li>Render concept maps as constellations</li>
              </ul>
              <div className="mt-6">
                <Link
                  href="/dashboard"
                  className="inline-flex rounded-md px-4 py-2 bg-primary text-primary-foreground"
                  aria-label="Back to dashboard"
                >
                  Back to Dashboard
                </Link>
              </div>
            </div>
          </div>
        </section>
      </div>
    </main>
  )
}
