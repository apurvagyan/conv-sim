import { useState } from 'react';

const PromptBox = ({ onSubmit }) => {
  const [person1Desc, setPerson1Desc] = useState('');
  const [person2Desc, setPerson2Desc] = useState('');
  const [prompt, setPrompt] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (prompt.trim() && person1Desc.trim() && person2Desc.trim()) {
      setLoading(true); // Set loading to true when submission starts
      try {
        await onSubmit({ prompt, person1Desc, person2Desc });
      } finally {
        setLoading(false); // Reset loading to false after submission
        setPrompt(''); // Clear the input field after submission
        setPerson1Desc('');
        setPerson2Desc('');
      }
    }
  };

  return (
    <form onSubmit={handleSubmit} className="mb-4">
      <input
        type="text"
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        className="w-full p-2 mb-4 rounded border border-gray-300 bg-gray-100 text-gray-900"
        placeholder="Enter your prompt"
      />
      <input
        type="text"
        value={person1Desc}
        onChange={(e) => setPerson1Desc(e.target.value)}
        className="w-full p-2 mb-4 rounded border border-gray-300 bg-gray-100 text-gray-900"
        placeholder="Enter person 1's description"
      />
      <input
        type="text"
        value={person2Desc}
        onChange={(e) => setPerson2Desc(e.target.value)}
        className="w-full p-2 mb-4 rounded border border-gray-300 bg-gray-100 text-gray-900"
        placeholder="Enter person 2's description"
      />
      <button
        type="submit"
        className="mt-2 w-full px-4 py-2 bg-slate-700 text-white rounded hover:bg-blue-700 transition-colors flex justify-center items-center"
      >
        {loading ? (
          <div className="animate-spin rounded-full h-6 w-6 border-t-2 border-b-2 border-white"></div> // Spinner
        ) : (
          'Submit'
        )}
      </button>
    </form>
  );
};

export default PromptBox;
