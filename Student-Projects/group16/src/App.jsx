import { ChatInput } from './components/ChatInput';
import ChatMessages from './components/ChatMessages';
import { useState } from 'react';
import './App.css';



function App() {
  const [messages, setNewMessage] = useState([
    { message: "موضوع مورد نظرت رو بنویس", sender: "bot", id: crypto.randomUUID() }
  ]);

  return (
    <div className="app-container">
      <ChatMessages messages={messages} />
      <ChatInput messages={messages} setNewMessage={setNewMessage} />
    </div>
  );
}

export default App
