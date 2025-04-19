import React, { useState, useRef, useEffect } from 'react';
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

  const handleSend = (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMsg = { text: input.trim(), sender: 'user' };
    setMessages((prev) => [...prev, userMsg]);
    setInput('');

    // Fake bot response
    setTimeout(() => {
      const botReply = generateBotResponse(input.trim());
      setMessages((prev) => [...prev, { text: botReply, sender: 'bot' }]);
    }, 500);
  };

  const generateBotResponse = (msg) => {
    // Replace this with API call to a real chatbot
    if (msg.toLowerCase().includes("hello")) return "Hey there!";
    if (msg.toLowerCase().includes("how are you")) return "I'm just code, but I'm doing great!";
    return "Sorry, I don't understand that yet 🤖";
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
