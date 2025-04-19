import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import './ChatPage.css';

const ChatPage = () => {
  const [messages, setMessages] = useState([
    { text: "Hello! Ask me anything 👋", sender: "bot" }
  ]);
  const [input, setInput] = useState('');
  const chatEndRef = useRef(null);

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(scrollToBottom, [messages]);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;
  
    const userQuery = input.trim();
  
    // Show user's message
    setMessages(prev => [...prev, { text: userQuery, sender: 'user' }]);
    setInput('');
  
    try {
      // Send query and get bot response directly
      const res = await axios.post('http://localhost:5000/chat', JSON.stringify({ query: userQuery }), {
        headers: {
          'Content-Type': 'application/json',
        },
      });
  
      const botText = res.data?.response || "Sorry, I didn’t get that 🤖";
  
      setMessages(prev => [...prev, { text: botText, sender: 'bot' }]);
    } catch (err) {
      console.error('Error communicating with backend:', err);
      setMessages(prev => [...prev, { text: "⚠️ Could not reach the server.", sender: 'bot' }]);
    }
  };
  

  return (
    <div className="chat-container">
      <div className="chat-header">💬 ChatBot</div>
      <div className="chat-messages">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`chat-bubble ${msg.sender === 'user' ? 'user' : 'bot'}`}
          >
            {msg.text}
          </div>
        ))}
        <div ref={chatEndRef} />
      </div>
      <form className="chat-input" onSubmit={handleSend}>
        <input
          type="text"
          value={input}
          placeholder="Type your message..."
          onChange={(e) => setInput(e.target.value)}
        />
        <button type="submit">Send</button>
      </form>
    </div>
  );
};

export default ChatPage;
