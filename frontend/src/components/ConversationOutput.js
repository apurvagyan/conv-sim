const ConversationOutput = ({ conversation }) => {
  return (
    <div style={{ maxWidth: '800px' }} className="w-full max-w-lg mt-8 bg-white bg-opacity-10 rounded-lg p-4">
      {conversation.map((message, index) => (
        <div key={index} className={`mb-4 ${message.speaker === 1 ? 'text-right' : 'text-left'}`}>
          <div className="mb-1">
            <span className={`inline-block px-2 py-1 rounded-full text-sm font-semibold ${
              message.speaker === 1 
                ? 'bg-gray-500 text-white' 
                : 'bg-slate-600 text-white'
            }`}>
              {message.name}
            </span>
          </div>
          <span className={`inline-block p-2 rounded-lg ${
            message.speaker === 1 
              ? 'bg-black bg-opacity-30 text-white' 
              : 'bg-gray-800 bg-opacity-40 text-gray-200'
          }`}>
            {message.content}
          </span>
        </div>
      ))}
    </div>
  )
}

export default ConversationOutput
