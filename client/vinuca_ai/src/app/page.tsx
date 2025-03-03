'use client'
import { useState, useEffect } from 'react'
import { Greet } from './components/greet'
import { Count } from './components/count'

export default function Home() {
  const [message, setMessage] = useState('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/gemini-response')
        const data = await response.json()
        setMessage(data.message) // get from data.message
      } catch (error) {
        console.error('Error fetching data:', error)
        setMessage('Error connecting to API')
      } finally {
        setLoading(false)
      }
    }
    fetchData()
  }, [])
  console.log("message:", message)
  return (
    <main className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Next.js + FastAPI</h1>
      < Greet /> <br></br>
      <Count /> <br></br><br></br>
      {loading ? (
        <p>Loading...</p>
      ) : (
        <p>Message from API: {message}</p>
      )}
    </main>
  )
}