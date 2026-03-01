import { useState, useRef, useEffect } from "react";

export default function Chat() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { role: "user", text: input };
    setMessages(prev => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: input })
      });

      const data = await response.json();

      const botMessage = { role: "bot", text: data.answer };

      setMessages(prev => [...prev, botMessage]);
    } catch (err) {
      console.error(err);
    }

    setLoading(false);
  };

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    try {
        await fetch("http://127.0.0.1:8000/upload", {
        method: "POST",
        body: formData
        });

        alert("File uploaded successfully!");
    } catch (err) {
        console.error(err);
    }
  };

  return (
    <div className="chat-container">

        <div className="messages">
        {messages.map((msg, index) => (
            <div
            key={index}
            className={`message ${msg.role === "user" ? "user" : "bot"}`}
            >
            {msg.text}
            </div>
        ))}
        {loading && <div className="bot message">Thinking...</div>}
        <div ref={messagesEndRef} />
        </div>

        <div className="bottom-section">
        <div className="file-upload">
            <input
            type="file"
            accept=".txt,.pdf,.docx"
            onChange={handleFileUpload}
            />
        </div>

        <div className="input-area">
            <input
            value={input}
            onChange={e => setInput(e.target.value)}
            placeholder="Ask something..."
            onKeyDown={e => e.key === "Enter" && sendMessage()}
            />
            <button onClick={sendMessage}>Send</button>
        </div>
        </div>

    </div>
    );
}