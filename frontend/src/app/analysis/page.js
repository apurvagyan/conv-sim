"use client"; // Add this line at the top

import DOMPurify from 'dompurify';
import { useState } from 'react';
import ParticlesBackground from '../../components/ParticleBackground'; // Adjust the path

export default function AnalysisPage() {
    const analysis = localStorage.getItem('analysis').replace(/\n/g, '<br>');
    const sanitizedAnalysis = DOMPurify.sanitize(analysis);

    const formattedAnalysis = analysis ? analysis.replace(/\n/g, '<br>') : 'No analysis available';
    const [graphData, setGraphData] = useState(null);

    return (
      <div className="relative min-h-screen flex-col items-center justify-center p-4">
        <ParticlesBackground />
        <div className="flex-col min-h-screen items-center justify-center">
          <div className="text-center top-10 pt-10 mb-10">
            <h1 className="text-white text-4xl font-bold">Conversation Analysis</h1>
          </div>
          <div className="flex w-full h-full justify-between space-x-4 p-10">
            {/* Analysis Section */}
            <div className="w-1/2 p-10 bg-gray-100 rounded-lg bg-opacity-10 ">
              <h2 className="text-xl text-white font-semibold mb-4">Analysis:</h2>
              <span className={`p-2 rounded-lg text-white`} dangerouslySetInnerHTML={{ __html: sanitizedAnalysis }}>
              </span>
            </div>
            
            {/* Graph Section */}
            <div className="w-1/2 p-10 bg-gray-200 rounded-lg bg-opacity-10">
              <h2 className="text-xl text-white font-semibold mb-4">Graph:</h2>
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