import React, { useState } from 'react';

const PromptBox = ({ onSubmit }) => {
  const [prompt, setPrompt] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (prompt.trim()) {
      onSubmit(prompt);
      setPrompt(''); // Clear the input field after submission
    }
  };

  return (
    <form onSubmit={handleSubmit} className="mb-4">
      <input
        type="text"
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        className="w-full p-2 rounded border border-gray-300 bg-gray-100 text-gray-900"
        placeholder="Enter your prompt"
      />
      <button
        type="submit"
        className="mt-2 w-full px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors"
      >
        Submit
      </button>
    </form>
  );
};

export default PromptBox;
