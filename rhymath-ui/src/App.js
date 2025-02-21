import React, { useState } from "react";
import axios from "axios";

function App() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);

  const sendMessage = async () => {
    if (!input.trim()) return;
    
    const newMessages = [...messages, { user: "You", text: input }];
    setMessages(newMessages);

    try {
      const response = await axios.post("http://localhost:8000/chat", 
        { user_input: input },  
        { headers: { "Content-Type": "application/json" } }
      );

      setMessages([
        ...newMessages,
        { user: "RhyMath", text: response.data.response }
      ]);
    } catch (error) {
      console.error("Error fetching response:", error);
      setMessages([...newMessages, { user: "RhyMath", text: "❌ Error: Could not get response." }]);
    }

    setInput("");
  };

  return (
    <div className="chat-container">
      <div className="chat-box">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.user === "You" ? "user" : "bot"}`}>
            <strong>{msg.user}:</strong> {msg.text}
          </div>
        ))}
      </div>
      <input 
        value={input} 
        onChange={(e) => setInput(e.target.value)} 
        placeholder="Type your message..."
        onKeyPress={(e) => e.key === "Enter" && sendMessage()}
      />
      <button onClick={sendMessage}>Send</button>
    </div>
  );
}

export default App;
