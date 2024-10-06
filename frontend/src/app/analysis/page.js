"use client"; // Add this line at the top

import { useState } from 'react';
import ParticlesBackground from '../../components/ParticleBackground'; // Adjust the path

export default function AnalysisPage() {
    const analysis = localStorage.getItem('analysis');
    const [graphData, setGraphData] = useState(null);

    return (
      <div className="relative min-h-screen flex items-center justify-center p-4">
        <ParticlesBackground />
        <div className="flex min-h-screen items-center justify-center">
          <div className="text-center absolute top-10">
            <h1 className="text-white text-4xl font-bold">Conversation Analysis</h1>
          </div>
          <div className="flex w-4/5 h-4/5 justify-between">
            {/* Analysis Section */}
            <div className="w-1/2 p-4 bg-gray-100 rounded-lg">
              <h2 className="text-xl font-semibold mb-4">Analysis:</h2>
              <p>{analysis || 'No analysis provided'}</p>
            </div>
            
            {/* Graph Section */}
            <div className="w-1/2 p-4 bg-gray-200 rounded-lg">
              <h2 className="text-xl font-semibold mb-4">Graph:</h2>
              {/* Placeholder for your graph */}
              <div className="w-full h-full bg-white rounded-lg flex items-center justify-center">
                {/* Replace with your graph component */}
                <p>Graph will be displayed here</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
}