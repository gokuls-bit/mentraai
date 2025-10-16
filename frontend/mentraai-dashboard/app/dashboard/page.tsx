import EmotionGraph from "@/components/EmotionGraph"
import AIAvatar from "@/components/AIAvatar"
import MindScoreMeter from "@/components/MindScoreMeter"
import Recommendations from "@/components/Recommendations"
import ARPortal from "@/components/ARPortal"
import { Sidebar } from "@/components/Sidebar"

export const metadata = {
  title: "MentraAI • Dashboard",
}

export default function DashboardPage() {
  return (
    <main className="min-h-[100dvh]">
      <div className="mx-auto max-w-7xl grid grid-cols-1 md:grid-cols-[240px,1fr] gap-6 p-4 md:p-6">
        <Sidebar />
        <section className="flex flex-col gap-6">
          <header className="sr-only">
            <h1>MentraAI Dashboard</h1>
          </header>
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2">
              <EmotionGraph />
            </div>
            <AIAvatar />
          </div>
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <MindScoreMeter score={82} />
            <Recommendations />
            <ARPortal />
          </div>
        </section>
      </div>
    </main>
  )
}
