import { useState } from "react";

// Import all images and icons used in the UI
import logo from "./assets/Logo.png";
import add from "./assets/add.svg";
import chat from "./assets/chat.svg";
import upgrade from "./assets/upgrade.svg";
import menu from "./assets/listMenu.svg";
import linkTo from "./assets/link.svg";
import sendIcon from "./assets/send.svg";
import avatar from "./assets/avatar.avif";
import ai from "./assets/ai.webp";

const isPersian = (text) => /[\u0600-\u06FF]/.test(text);
// Main application component
export default function App() {
  // State to control sidebar visibility on mobile
  const [sidebarOpen, setSidebarOpen] = useState(false);

  // State to store user and AI messages
  const [messages, setMessages] = useState([
    { role: "system", content: "You are a helpful assistant." },
  ]);

  // State to control user input value
  const [input, setInput] = useState("");

  // Function to send user message and receive AI response
  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = input;

    // Add user message to state
    setMessages((prev) => [...prev, { role: "user", content: userMessage }]);
    setInput("");

    try {
      const response = await fetch("http://localhost:8000/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: userMessage }),
      });

      const data = await response.json();

      // Add AI response to state
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: data.response },
      ]);
    } catch (error) {
      console.error("Error calling API:", error);

      // Show error message if API call fails
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "Error: couldn't get response from API.",
        },
      ]);
    }
  };

  // UI structure
  return (
    // Main container — flex layout, full height, background color
    <div className="flex w-full h-screen bg-[#FAF1E4] text-[#2D2D2D] overflow-hidden">
      {/* Mobile header */}
      <div className="lg:hidden bg-[#435334] flex items-center justify-between px-4 py-4 shadow text-white w-full fixed top-0 z-40">
        <button onClick={() => setSidebarOpen(true)}>
          <img src={menu} className="w-7 h-7" alt="menu" />
        </button>
        <p className="font-semibold text-[18px]">Dashboard</p>
      </div>

      {/* Desktop sidebar */}
      <aside className="hidden lg:flex bg-[#435334] w-[260px] h-full flex-col text-white">
        {/* Logo */}
        <div className="flex items-center justify-center h-[100px] border-b border-[#39462C]">
          <img src={logo} alt="logo" />
        </div>

        {/* New Chat button */}
        <div className="flex justify-center items-center my-[30px]">
          <button className="w-[200px] bg-[#39462C] py-[17px] flex items-center gap-3 rounded-[40px] pl-6 hover:bg-[#46533B] transition">
            <img src={add} alt="add" />
            <span className="font-bold text-[13px]">New Chat</span>
          </button>
        </div>

        {/* Recent chats list */}
        <div className="px-[12px] flex flex-col gap-[40px] overflow-y-auto flex-1">
          <p className="text-[13px] mb-[15px] text-[#9EB384]">Recent Chats</p>

          {/* Recently opened chat items */}
          {[
            "Platform Marketplace 101",
            "20 Company Name Ideas",
            "UI/UX Trends 2025",
          ].map((item, i) => (
            <div
              key={i}
              className="flex items-center gap-[10px] cursor-pointer hover:bg-[#3C4A31] p-2 rounded-lg transition"
            >
              <img src={chat} alt="chat" />
              <p className="truncate w-[180px] text-[14px]">{item}</p>
            </div>
          ))}
        </div>

        {/* Upgrade to Plus section */}
        <div className="bg-[#FFEED6] flex items-center gap-2 py-3 px-4 text-[#333] cursor-pointer hover:bg-[#f7dcba] transition">
          <img src={upgrade} className="w-5 h-5" alt="upgrade" />
          <span className="text-[14px] font-medium">Upgrade to Plus</span>
        </div>
      </aside>

      {/* Dark backdrop when sidebar is open on mobile */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 bg-black bg-opacity-40 lg:hidden z-40"
          onClick={() => setSidebarOpen(false)}
        ></div>
      )}

      {/* Mobile sidebar */}
      <aside
        className={`fixed top-0 left-0 h-full w-[260px] bg-[#435334] flex flex-col text-white transform transition-transform duration-300 lg:hidden z-50 ${
          sidebarOpen ? "translate-x-0" : "-translate-x-full"
        }`}
      >
        {/* Logo */}
        <div className="flex justify-center items-center h-[100px] border-b border-[#39462C]">
          <img src={logo} alt="logo" />
        </div>

        {/* New Chat */}
        <div className="flex justify-center items-center my-[30px]">
          <button className="w-[200px] bg-[#39462C] py-[17px] flex items-center gap-3 rounded-[40px] pl-6 hover:bg-[#46533B] transition">
            <img src={add} alt="add" />
            <span className="font-bold text-[13px]">New Chat</span>
          </button>
        </div>

        {/* Recent chats */}
        <div className="px-[12px] flex flex-col gap-[40px] overflow-y-auto flex-1">
          <p className="text-[13px] mb-[15px] text-[#9EB384]">Recent Chats</p>

          <div className="flex items-center gap-[10px] cursor-pointer hover:bg-[#3C4A31] p-2 rounded-lg transition">
            <img src={chat} alt="chat" />
            <p className="truncate w-[180px] text-[14px]">UI/UX Trends 2025</p>
          </div>
        </div>

        {/* Upgrade section */}
        <div className="bg-[#FFEED6] flex items-center gap-2 py-3 px-4 text-[#333]">
          <img src={upgrade} className="w-5 h-5" alt="upgrade" />
          <span className="text-[14px] font-medium">Upgrade to Plus</span>
        </div>
      </aside>

      {/* Main content section */}
      <main className="flex-1 flex flex-col h-full">
        {/* Desktop header */}
        <div className="hidden lg:flex h-[100px] border-b items-center px-6 shadow-sm bg-[#39462C] text-white">
          {/* Profile avatar */}
          <img
            src={avatar}
            className="w-12 h-12 rounded-full"
            alt="profile"
          />
        </div>

        {/* Messages and info section */}
        <div className="flex-1 flex overflow-hidden mt-[70px] lg:mt-0">
          {/* Chat messages column */}
          <div className="flex-1 flex flex-col p-6 overflow-y-auto chat-scroll">
            {/* Title and avatar */}
            <div className="flex items-center justify-between gap-3 w-full">
              <p className="font-semibold bg-[#FFEED6] rounded-[14px] w-full p-4 mb-4 shadow text-center">
                NexMind : Digital Mental Health Assistant 💕
              </p>

              <img
                src={avatar}
                className="w-10 h-10 rounded-full"
                alt="profile"
              />
            </div>

            {/* Render user and AI messages */}
            {messages
              .filter((m) => m.role !== "system") // Remove system messages from UI
              .map((m, i) => (
                <div
                  key={i}
                  className={`${
                    m.role === "user" ? "bg-white" : "bg-[#E1F0D1]"
                  } p-3 rounded-lg mb-3 shadow`}
                  style={{
                    direction: isPersian(m.content) ? "rtl" : "ltr",
                    textAlign: isPersian(m.content) ? "right" : "left",
                  }}
                >
                  <p>{m.content}</p>
                </div>
              ))}

            {/* Message input section */}
            <div className="mt-auto flex items-center gap-3 pt-3">
              {/* User input */}
              <input
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && sendMessage()}
                placeholder="Hello, How are you feeling today?..."
                className="flex-1 h-[45px] pl-4 bg-[#FFEED6] ring-1 ring-[#D6BC97] rounded-[10px] focus:outline-none"
              />

              {/* Send button */}
              <button
                onClick={sendMessage}
                className="bg-[#435334] w-[45px] h-[45px] flex items-center justify-center rounded-xl hover:bg-[#354428] transition"
              >
                <img src={sendIcon} className="w-5" />
              </button>
            </div>
          </div>

          {/* Right-side welcome panel */}
          <div className="w-[25%] bg-[#EAF2E1] p-4 overflow-y-auto text-[#39462C]">
            <h2 className="font-semibold text-lg mb-2">Hello 💖</h2>

            <p className="mb-3">Welcome to the NexMind chatbot. 👋</p>

            <p className="mb-3">
              I’m <b>Nexy</b>, your digital mental health assistant, designed to
              listen to your thoughts and emotional experiences in a supportive
              and respectful way.
            </p>

            <p className="mb-3">
              🌈 Think of me as a friendly companion who encourages reflection
              and emotional awareness, while offering general, non-clinical
              guidance when appropriate.
            </p>

            <p className="mb-3">
              👩‍⚕️ My responses are based on general knowledge of psychology and
              emotional well-being. I am not a medical professional.
            </p>

            <p className="font-semibold">
              I’m here to walk alongside you—let’s begin this journey together.
              💞
            </p>
          </div>
        </div>
      </main>
    </div>
  );
}