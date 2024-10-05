const ConversationOutput = ({ conversation }) => {
  return (
    <div className="w-full max-w-md mt-8 bg-white bg-opacity-10 rounded-lg p-4">
      {conversation.map((message, index) => (
        <div key={index} className={`mb-4 ${message.role === 'user' ? 'text-right' : 'text-left'}`}>
          <span className={`inline-block p-2 rounded-lg ${message.role === 'user' ? 'bg-purple-600 text-white' : 'bg-gray-200 text-gray-800'}`}>
            {message.content}
          </span>
        </div>
      ))}
    </div>
  )
}

export default ConversationOutput
