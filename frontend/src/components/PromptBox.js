import { useState } from 'react'

const PromptBox = ({ onSubmit }) => {
  const [prompt, setPrompt] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    onSubmit({ prompt })
    setPrompt('')
  }

  return (
    <form onSubmit={handleSubmit} className="w-full max-w-md">
      <div className="flex items-center border-b border-purple-500 py-2">
        <input
          className="appearance-none bg-transparent border-none w-full text-white mr-3 py-1 px-2 leading-tight focus:outline-none"
          type="text"
          placeholder="Enter your prompt"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
        />
        <button
          className="flex-shrink-0 bg-purple-500 hover:bg-purple-700 border-purple-500 hover:border-purple-700 text-sm border-4 text-white py-1 px-2 rounded"
          type="submit"
        >
          Submit
        </button>
      </div>
    </form>
  )
}

export default PromptBox
