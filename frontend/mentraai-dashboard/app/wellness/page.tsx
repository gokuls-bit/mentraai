import EmotionGraph from "@/components/EmotionGraph"
import Recommendations from "@/components/Recommendations"
import { Sidebar } from "@/components/Sidebar"

export const metadata = {
  title: "MentraAI • Wellness",
}

export default function WellnessPage() {
  return (
    <main className="min-h-[100dvh]">
      <div className="mx-auto max-w-7xl grid grid-cols-1 md:grid-cols-[240px,1fr] gap-6 p-4 md:p-6">
        <Sidebar />
        <section className="flex flex-col gap-6">
          <header>
            <h1 className="text-balance text-xl font-semibold">Wellness</h1>
            <p className="text-sm text-muted-foreground">Your emotional rhythms and mindful nudges</p>
          </header>
          <EmotionGraph />
          <Recommendations />
        </section>
      </div>
    </main>
  )
}
