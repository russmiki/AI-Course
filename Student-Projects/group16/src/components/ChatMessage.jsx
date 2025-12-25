import { useState } from 'react';
import RobotProfileImg from '../assets/bot.png';
import UserProfileImg from '../assets/user.png';
import "./ChatMessage.css";

/**
 * ChatMessage component for displaying messages in the chat.
 */
export function ChatMessage({ message, sender }) {
  const isBot = sender === "bot";
  const [copied, setCopied] = useState(false);

  // Handle copy of the message if the message is from the bot.
  const handleCopy = async () => {
    if (!isBot) return;
    
    try {
      await navigator.clipboard.writeText(message);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy text:', err);
    }
  };

  // Return the ChatMessage component.
  return (
    <div className={`chat-message ${isBot ? "bot" : "user"}`}>
      <img 
        src={isBot ? RobotProfileImg : UserProfileImg} 
        alt={isBot ? "Bot avatar" : "User avatar"} 
        className="avatar"
      />
      <div className="message-wrapper">
        <div 
          className={`message-txt ${isBot ? 'copyable' : ''} ${copied ? 'copied' : ''}`}
          onClick={handleCopy}
          title={isBot ? (copied ? 'Copied!' : 'Click to copy') : ''}
        >
          {message}
        </div>
        {copied && (
          <div className="copy-notification">
            کپی شد!
          </div>
        )}
      </div>
    </div>
  );
}
