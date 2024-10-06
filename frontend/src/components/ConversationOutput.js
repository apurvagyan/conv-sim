const ConversationOutput = ({ conversation }) => {
  return (
    <div style={{ maxWidth: '800px' }} className="w-full max-w-lg mt-8 bg-white bg-opacity-10 rounded-lg p-4">
      {conversation.map((message, index) => (
        <div key={index} className={`mb-4 ${message.speaker === 1 ? 'text-right' : 'text-left'}`}>
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
