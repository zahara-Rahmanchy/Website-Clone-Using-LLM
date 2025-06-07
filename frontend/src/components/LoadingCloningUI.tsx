'use client';

import { useEffect, useState } from 'react';

const messages = [
  'Cloning in progress... please hold on.',
  'Scraping website and analyzing structure...',
  'Generating a clean HTML layout for preview...',
  'Almost there! Putting on the final touches...',
  'Good things take time — thanks for your patience.',
];

export default function LoadingCloningUI() {
  const [messageIndex, setMessageIndex] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setMessageIndex((prev) => (prev + 1) % messages.length);
    }, 3500); // switch message every 3.5 seconds
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="w-full h-[60vh] flex flex-col items-center justify-center text-center px-4">
      <svg
        className="animate-spin h-8 w-8 text-gray-50 mb-4"
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
      >
        <circle
          className="opacity-25"
          cx="12"
          cy="12"
          r="10"
          stroke="currentColor"
          strokeWidth="4"
        />
        <path
          className="opacity-75"
          fill="currentColor"
          d="M4 12a8 8 0 018-8v8z"
        />
      </svg>
      <p className="text-gray-100 text-lg transition-opacity duration-500 ease-in-out">
        {messages[messageIndex]}
      </p>
    </div>
  );
}
