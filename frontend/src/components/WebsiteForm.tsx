"use client"
import { useState } from "react";
import WebsitePreview from "./WebsitePreview";
import LoadingCloningUI from "./LoadingCloningUI";
import { CloneWebsite } from "@/actions/CloneWebsite";


export default function WebsiteForm() {
  const [url, setUrl] = useState("");

  // const handleSubmit = (e:React.FormEvent<HTMLFormElement>) => {
  //   e.preventDefault();
  //   alert(`Cloning website: ${url}`);
  //   // Add your cloning logic here
  // };
 
  const [html, setHtml] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setHtml(null);
    console.log("hello url: ",url)
   
      const result = await CloneWebsite(url);

    if (result.error) {
      setError(result.error);
      setLoading(false);
    } else {
      setHtml(result.html);
      setLoading(false);
    }

    
  };

  return (
    //  <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-r from-purple-500 via-pink-500 to-red-500 px-4">
    <>
      <div className="bg-white bg-opacity-90 backdrop-blur-md rounded-2xl shadow-lg max-w-xl w-full p-8 sm:py-7 px-12">
       
        <form onSubmit={handleSubmit} className="flex flex-col sm:flex-row gap-4">
          <input
            type="url"
            required
            placeholder="https://example.com"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            className="flex-grow px-5 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-4 focus:ring-pink-400 transition"
          />
          <button
            type="submit"
            disabled={loading}
            className="px-8 py-3 cursor-pointer bg-pink-600 text-white font-semibold rounded-lg hover:bg-pink-700 transition"
          >
             {loading ? 'Cloning...' : 'Clone'}
          </button>
        </form>
       
      </div>
       {loading && <LoadingCloningUI/>}
      {error && <p className="text-red-400 my-10 w-[90%] mx-auto text-center">{error}</p>}
      {html && (
        <div className=" w-[90%] mx-auto mb-20">
          <h2 className="text-xl font-semibold mb-4 text-center text-gray-100">Cloned Preview</h2>
          <WebsitePreview html={html} />
        </div>
      )}
    </>
  );
}
