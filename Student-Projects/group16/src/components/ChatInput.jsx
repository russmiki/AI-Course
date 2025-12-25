import { useState } from "react";
import { GoogleGenAI } from "@google/genai";
import { tweetPrompt } from "../prompts/tweetPrompt";
import { ErrorPopup } from "./ErrorPopup";
import { getErrorMessage } from "../utils/errorHandler";
import { useApiKey } from "../hooks/useApiKey";
import "./ChatInput.css";

/**
 * ChatInput component for sending messages to the bot and getting response from the AI.
 */
export function ChatInput({ messages, setNewMessage }) {
  const apiKey = useApiKey();
  const [inputText, setInputText] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showError, setShowError] = useState(false);

  // Save the input text to the state.
  function saveInputText(event) {
    setInputText(event.target.value);
  }

  // Show the error popup.
  function showErrorPopup(errorMessage) {
    setError(errorMessage);
    setShowError(true);
  }

  // Close the error popup.
  function closeErrorPopup() {
    setShowError(false);
    setError(null);
  }

  // Get the AI response from the bot.
  async function getAIResponse(userMessage) {
    try {
      const ai = new GoogleGenAI({
        apiKey: apiKey,
      });

      const prompt = tweetPrompt;

      const response = await ai.models.generateContent({
        model: "gemini-2.5-flash",
        contents: prompt + userMessage,
      });

      if (!response || !response.text) {
        throw new Error("پاسخ نامعتبر از سرور دریافت شد.");
      }

      return response.text;
    } catch (error) {
      const errorMessage = getErrorMessage(error);
      throw new Error(errorMessage);
    }
  }


  async function sendMessage() {
    if (!inputText.trim() || isLoading) return;

    const userMessage = inputText.trim();
    const newMessages = [
      ...messages,
      {
        message: userMessage,
        sender: "user",
        id: crypto.randomUUID(),
      },
    ];

    setNewMessage(newMessages);
    setInputText("");
    setIsLoading(true);

    try {
      const aiResponse = await getAIResponse(userMessage);

      setNewMessage([
        ...newMessages,
        {
          message: aiResponse,
          sender: "bot",
          id: crypto.randomUUID(),
        },
      ]);
    } catch (error) {
      // Remove user message on error
      setNewMessage(messages);
      showErrorPopup(error.message || "خطایی رخ داد. لطفاً دوباره تلاش کنید.");
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <>
      <div className="chat-container">
        <input
          name="chat-input"
          type="text"
          placeholder="Send a message here..."
          onChange={saveInputText}
          value={inputText}
          className="chat-input"
          disabled={isLoading}
          onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault();
              sendMessage();
            }
          }}
        />
        <button
          onClick={sendMessage}
          className="send-button"
          disabled={isLoading}
        >
          {isLoading ? "Sending..." : "Send"}
        </button>
      </div>
      <ErrorPopup
        message={error}
        onClose={closeErrorPopup}
        isVisible={showError}
      />
    </>
  );
}