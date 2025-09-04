import { motion } from "framer-motion";
import { Bot, User } from "lucide-react";

function ResponseCard({ question, answer }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="backdrop-blur-md bg-white/10 p-4 sm:p-5 rounded-2xl shadow-lg border border-white/20"
    >
      {/* User Question */}
      <div className="flex items-center gap-2 mb-2">
        <User className="text-blue-400" size={18} />
        <h2 className="text-sm sm:text-md md:text-lg font-semibold text-white break-words">
          {question}
        </h2>
      </div>

      {/* AI Response */}
      <div className="flex items-start gap-2">
        <Bot className="text-green-400 mt-1" size={18} />
        <p className="text-gray-200 leading-relaxed text-sm sm:text-base break-words">
          {answer}
        </p>
      </div>
    </motion.div>
  );
}

export default ResponseCard;
