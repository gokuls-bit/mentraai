export type EmotionPoint = { time: string; calm: number; focus: number; stress: number }

export function getEmotionData(): EmotionPoint[] {
  // Mocked timeseries
  return [
    { time: "09:00", calm: 62, focus: 48, stress: 22 },
    { time: "10:00", calm: 65, focus: 55, stress: 20 },
    { time: "11:00", calm: 60, focus: 58, stress: 24 },
    { time: "12:00", calm: 58, focus: 52, stress: 28 },
    { time: "13:00", calm: 63, focus: 60, stress: 21 },
    { time: "14:00", calm: 67, focus: 62, stress: 18 },
    { time: "15:00", calm: 71, focus: 66, stress: 16 },
  ]
}

export type Recommendation = { id: string; title: string; detail: string; action?: string }

export function getRecommendations(): Recommendation[] {
  return [
    {
      id: "1",
      title: "3‑minute Breathing Exercise",
      detail: "Reduce micro-stress spikes observed at 12:00.",
      action: "Start",
    },
    {
      id: "2",
      title: "Focus Sprint",
      detail: "Your focus peaks at 15:00; schedule deep work then.",
      action: "Schedule",
    },
    {
      id: "3",
      title: "Stretch Reminder",
      detail: "Neck tension detected from posture metrics; stretch now.",
      action: "Stretch",
    },
  ]
}
