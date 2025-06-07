// import Image from "next/image";

import WebsiteForm from "@/components/WebsiteForm";



export default function Home() {
  return (
      <div className="min-h-screen flex flex-col items-center justify-center  px-4">
        <h1 className="text-4xl font-extrabold text-stone-100 mb-4 text-center sm:text-left cursor-none">
          Clone Any Website
        </h1>
        <p className="text-pink-50 mb-8 text-center sm:text-left max-w-xl">
          Enter the URL of the website you want to clone and get started instantly.
        </p>
        <WebsiteForm/>
        
      </div>
  );
}
