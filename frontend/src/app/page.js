'use client';

import React, { useState, useCallback } from 'react';
import Particles from "react-tsparticles";
import { loadFull } from "tsparticles";
import PromptBox from '../components/PromptBox';
import ConversationOutput from '../components/ConversationOutput';

export default function Home() {
  const [conversation, setConversation] = useState([]);

  const particlesInit = useCallback(async engine => {
    await loadFull(engine);
  }, []);

  const handleSubmit = (promptData) => {
    setConversation([...conversation, { role: 'user', content: promptData }]);
    setTimeout(() => {
      setConversation(prev => [...prev, { role: 'assistant', content: 'This is a simulated response.' }]);
    }, 1000);
  };

  return (
    <div className="relative min-h-screen flex items-center justify-center p-4">
      <div className="stars"></div>
      <Particles
        id="tsparticles"
        init={particlesInit}
        options={{
          background: {
            color: {
              value: "transparent",
            },
          },
          fpsLimit: 60,
          interactivity: {
            events: {
              onClick: {
                enable: true,
                mode: "push",
              },
              onHover: {
                enable: true,
                mode: "repulse",
              },
              resize: true,
            },
            modes: {
              push: {
                quantity: 4,
              },
              repulse: {
                distance: 200,
                duration: 0.4,
              },
            },
          },
          particles: {
            color: {
              value: "#ffffff",
            },
            links: {
              color: "#ffffff",
              distance: 150,
              enable: true,
              opacity: 0.5,
              width: 1,
            },
            move: {
              direction: "none",
              enable: true,
              outModes: {
                default: "bounce",
              },
              random: false,
              speed: 2,
              straight: false,
            },
            number: {
              density: {
                enable: true,
                area: 800,
              },
              value: 80,
            },
            opacity: {
              value: 0.5,
            },
            shape: {
              type: "circle",
            },
            size: {
              value: { min: 1, max: 5 },
            },
          },
          detectRetina: true,
        }}
      />
      <div className="z-10 bg-black bg-opacity-30 p-8 rounded-lg shadow-lg max-w-md w-full">
        <h1 className="text-4xl font-bold text-white mb-8 text-center">Conversation Simulator</h1>
        <PromptBox onSubmit={handleSubmit} />
        <ConversationOutput conversation={conversation} />
      </div>
    </div>
  );
}
