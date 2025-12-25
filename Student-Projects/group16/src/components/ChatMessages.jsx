import React from 'react';
import {ChatMessage} from './ChatMessage';
import { WelcomeMessage } from './WelcomeMessage';
import "./ChatMessages.css";

/**
 * ChatMessages component for displaying the messages in the chat.
 */
function ChatMessages({ messages }) {
  
  const containerElm = React.useRef(null);

  React.useEffect(() => {
    containerElm.current.scrollTop = containerElm.current.scrollHeight;
  }, [messages])

  return (
    <div className="chat-messages" ref={containerElm}>
      <WelcomeMessage />
      {messages.map((msg) => {
        return (
          <ChatMessage
            key={msg.id}
            message={msg.message}
            sender={msg.sender}
          />
        );
      })}
    </div>
  );
}

export default ChatMessages;