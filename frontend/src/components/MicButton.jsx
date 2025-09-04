import { useState } from "react";
import { motion } from "framer-motion";
import { Mic } from "lucide-react";

function MicButton({ onResult }) {
  const [listening, setListening] = useState(false);

  const startListening = () => {
    setListening(true);
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = "en-US";
    recognition.start();

    recognition.onresult = (event) => {
      const text = event.results[0][0].transcript;
      setListening(false);
      onResult(text);
    };

    recognition.onerror = () => setListening(false);
  };

  return (
    <div className="relative">
      {listening && (
        <motion.div
          className="absolute -inset-4 sm:-inset-6 rounded-full bg-blue-600 opacity-40 blur-md"
          animate={{ scale: [1, 1.3, 1] }}
          transition={{ repeat: Infinity, duration: 1.5 }}
        />
      )}
      <motion.button
        onClick={startListening}
        whileTap={{ scale: 0.9 }}
        className="w-24 h-24 sm:w-28 sm:h-28 md:w-36 md:h-36 rounded-full 
                   bg-gradient-to-r from-blue-600 to-indigo-900 
                   flex items-center justify-center 
                   shadow-2xl text-white"
      >
        <Mic size={40} className="sm:size-20 md:size-20"/>
      </motion.button>
    </div>
  );
}

export default MicButton;
