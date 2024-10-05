'use client';

import ParticleBackground from '../components/ParticleBackground'
import PromptBox from '../components/PromptBox'
import ConversationOutput from '../components/ConversationOutput'
import { useState } from 'react'

export default function Home() {
  const [conversation, setConversation] = useState([])

  const handleSubmit = (promptData) => {
    // Here you would typically send the data to your backend
    // For now, we'll just add it to the conversation state
    setConversation([...conversation, { role: 'user', content: promptData.prompt }])
    // Simulate a response
    setTimeout(() => {
      setConversation(prev => [...prev, { role: 'assistant', content: 'This is a simulated response.' }])
    }, 1000)
  }

  return (
    <div className="relative min-h-screen">
      <ParticleBackground />

      <main className="relative z-10 flex flex-col items-center justify-center min-h-screen p-4">
        <h1 className="text-4xl font-bold text-white mb-8">Conversation Simulator</h1>
        <PromptBox onSubmit={handleSubmit} />
        <ConversationOutput conversation={conversation} />
      </main>
    </div>
  )
}
