// components/Chat.tsx
"use client"; // This ensures the component runs on the client side.

import { useState } from "react";

export default function Chat() {
  const [query, setQuery] = useState(""); // Stores user input
  const [response, setResponse] = useState(""); // Stores AI response
  const [loading, setLoading] = useState(false); // Tracks loading state

  // Function to send the user input to FastAPI
  async function sendMessage() {
    if (!query.trim()) return; // Prevent empty queries

    setLoading(true); // Start loading state
    setResponse(""); // Clear previous response

    try {
      const res = await fetch("http://localhost:8000/api/gemini-response", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: query }), // Send user input as JSON
      });

      if (!res.ok) throw new Error("Failed to fetch response");

      const data = await res.json();
      setResponse(data.message); // Store the AI-generated response
    } catch (error) {
      console.error("Error:", error);
      setResponse("Error fetching response. Please try again.");
    } finally {
      setLoading(false); // Stop loading state
    }
  }

  return (
    <div className="p-4 max-w-md mx-auto bg-white rounded-lg shadow-md">
      <h2 className="text-xl font-semibold mb-2">Chat with AI</h2>
      
      <textarea
        className="w-full p-2 border rounded"
        placeholder="Type your question..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        rows={3}
      ></textarea>

      <button
        className="mt-2 px-4 py-2 bg-pink-600 text-white rounded disabled:opacity-50"
        onClick={sendMessage}
        disabled={loading}
      >
        {loading ? "Thinking..." : "Send"}
      </button>

      {response && (
        <div className="mt-4 p-2 bg-gray-100 border rounded">
          <strong>Vinuca:</strong> {response}
        </div>
      )}
    </div>
  );
}
