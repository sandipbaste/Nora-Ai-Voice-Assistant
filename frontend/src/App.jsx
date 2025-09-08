import { useState } from "react";
import MicButton from "./components/MicButton";
import ResponseCard from "./components/ResponseCard";
import axios from "axios";
import { motion } from "framer-motion";

function App() {
  const [responses, setResponses] = useState([]);

  const handleUserInput = async (text) => {
    if (!text) return;
    try {
      const res = await axios.post("http://localhost:8000/ask/", { question: text });
      const newResponse = { question: text, answer: res.data.answer, audio: res.data.audio_url };
      setResponses([newResponse, ...responses]);

      // Play audio response
      const audio = new Audio(`http://localhost:8000${res.data.audio_url}`);
      audio.play();
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="min-h-screen w-full bg-gradient-to-br from-sky-500 via-blue-200 
                flex flex-col items-center justify-center p-4 sm:p-6">
  {/* Header */}
  <motion.h1
    initial={{ opacity: 0, y: -20 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ duration: 0.7 }}
    className="text-2xl pt-16 sm:text-3xl md:text-4xl font-bold text-center mb-2 sm:mb-3"
  >
    🎙️ Nora - Your AI Assistant
  </motion.h1>

  <motion.h2
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ duration: 0.7 }}
    className="mb-12 sm:mb-20 text-base sm:text-lg md:text-xl text-center text-gray-800"
  >
    Ask your problem with Nora
  </motion.h2>

  {/* Mic Button */}
  <div className="flex justify-center mb-10 sm:mb-12">
    <MicButton onResult={handleUserInput} />
  </div>

  {/* Responses */}
  <div className="max-sm:6 space-y-4 w-full max-w-md sm:max-w-2xl px-2">
    {responses.map((res, i) => (
      <ResponseCard key={i} question={res.question} answer={res.answer} />
    ))}
  </div>
</div>

  );
}

export default App;
