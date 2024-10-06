'use client';

import ParticleBackground from '@/components/ParticleBackground';
import Link from 'next/link';
import { useCallback, useState } from 'react';
import { loadFull } from "tsparticles";
import ConversationOutput from '../components/ConversationOutput';
import PromptBox from '../components/PromptBox';


export default function Home() {
  const [conversation, setConversation] = useState([]);
  const [analysis, setAnalysis] = useState('');
  const [responseReceived, setResponseReceived] = useState(false);

  const particlesInit = useCallback(async engine => {
    await loadFull(engine);
  }, []);

  const handleSubmit = async ({prompt, person1Desc, person2Desc}) => {
    setConversation([...conversation, { speaker: 1, content: prompt }]);

    try {
      const response = await fetch('http://127.0.0.1:8080/user-prompt', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt: prompt, agent_1_desc: person1Desc, agent_2_desc: person2Desc }),
      });
  
      setResponseReceived(true);
      const data = await response.json();
      setConversation(data.messages);
      setAnalysis(data.analysis);
      localStorage.setItem('analysis', data.analysis);
    } catch {
      setConversation(prev => [...prev, { speaker: 2, content: 'An error occurred.' }]);
    }

    // setTimeout(() => {
    //   setConversation(prev => [...prev, { role: 'assistant', content: 'This is a simulated response.' }]);
    // }, 1000);
  };

  return (
    <div className="relative min-h-screen flex items-center justify-center p-4">
      <div className="stars"></div>
      <ParticleBackground />
      <div className="z-10 bg-black bg-opacity-30 p-8 rounded-lg shadow-lg max-w-md w-full">
        <h1 className="text-4xl font-bold text-white mb-8 text-center">Conversation Simulator</h1>
        <PromptBox onSubmit={handleSubmit} />
        <ConversationOutput conversation={conversation} />
        {responseReceived && (<Link href="/analysis">
          <button className="mt-2 w-full px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors">
            Analysis
          </button>
        </Link>)}
      </div>
    </div>
  );
}
