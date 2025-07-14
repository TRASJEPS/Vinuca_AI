// components/Chat.tsx
"use client"; // This ensures the component runs on the client side.

import { useState, Suspense } from "react";

export default function Chat() {
  const [query, setQuery] = useState(""); // Stores user input
  const [response, setResponse] = useState(""); // Stores AI response
  const [loading, setLoading] = useState(false); // Tracks loading state

  // Function to send the user input to FastAPI
  /*async function sendMessage() {
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
  }*/

  // Function to stream output from AI
  async function sendMessage() {
    if(!query.trim()) return;

    setLoading(true);
    setResponse('');

    try {
      const res = await fetch("http://localhost:8000/api/gemini-response", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: query, chat_history: []}), // Send user input as JSON
      });

      // check if response status okay and if data is returned
      if (!res.ok || !res.body) throw new Error("Stream failed");

      const reader = res.body.getReader();
      const decoder = new TextDecoder("utf-8");
  
      let done = false;
  
      while (!done) {
        const { value, done: doneReading } = await reader.read();
        done = doneReading;
        const chunk = decoder.decode(value);
        //console.log(chunk)
        if (chunk) setResponse((prev) => prev + chunk);
        console.log(chunk);
        // Filter out anything that isn't an SSE data line
        /*const matches = chunk.match(/data:\s(.*)/g);
        console.log("matches:", matches);
        if (matches) {
          for (const match of matches) {
            const text = match.replace("data: ", "").trim();
            console.log("text:", text);
            if (text) setResponse((prev) => prev + text);
            console.log("response:", response);
          }
        }*/
      }
    } catch (err) {
      console.error("Streaming error:", err);
      setResponse("Something went wrong.");
    } finally {
      setLoading(false);
    }
  }
  // set max-w-md to max-w-9/10 to allot for more sizing options for AI responses
  return (
    <div className="p-8 max-w-9/10 mx-auto bg-white rounded-lg shadow-md">
      <h2 className="text-xl p-4 font-semibold mb-2 text-center">Your Virtual Beauty Assistant</h2>
      
      {/*Vinuca_AI/client/vinuca_ai/src/app/favicon.ico */}
      {/* May remove the name "Vinuca" annd just stick to icons.. */}
      {response && (
        <div className=" flex p-2 mb-6 bg-gray-100 border rounded">
          <img src="../favicon.ico" alt="Description" className="w-6 h-6 mr-2" />
          <strong className="pr-2">Vinuca:</strong> {response}
        </div>
      )}

      <div className="flex gap-4 align-middle items-center border rounded">
      {/* removing ((border rounded)) line to clean */}
      {/* set resize-none to remove the lower right grey bars */}
        <textarea
          className="w-full p-4 resize-none"
          placeholder="How can I help you?"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          rows={1}
        ></textarea>

        {/* THE SEND BUTTON / CSS COLORS */}
        {/* button MR-2 to align send */}
        {/* PINK to BLUE */}
        <button
          className={`px-4 py-2 mr-2 ${loading ? 'bg-[rgb(0,0,255)]' : 'bg-[rgb(255,149,202)]'} text-white font-bold rounded disabled:opacity-50 hover:bg-[rgb(255,110,199)]`}
          onClick={sendMessage}
          disabled={loading}
        >
          {/* THE SEND BUTTON / LOADING ↑⤴ */}
          {/* The SVG needs a react 'react fragment' wrapper <></> */}
          {/* SPAN applied to loading response to lock in wheel on same line may simplify... - - may remove */}

          {loading ? ( 
            <>
            <svg className="size-5 animate-spin ..." viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            {/* <span className="inline-block">Let me think...</span>  */}
            </>
            ) 
          : "⤴"}
        </button>
      </div>

      

      

    </div>
  );
}