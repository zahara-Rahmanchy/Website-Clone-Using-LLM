# # from fastapi import FastAPI
# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# import httpx
# from pydantic import BaseModel
# from hyperbrowser import Hyperbrowser
# from playwright.sync_api import sync_playwright
# import base64

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # In production, set specific domains
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
# api_key = "hb_a8cfbd79326c0d4372222e06bece"
# @app.get("/")
# def read_root():
#     return {"message": "Hello World"}


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
import asyncio
import base64
import json
import os
from typing import Dict, Any, Optional
import httpx

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import hyperbrowser
from pydantic import BaseModel, HttpUrl
import google.genai as genai

from dotenv import load_dotenv
from hyperbrowser import Hyperbrowser
from hyperbrowser.models import (
    ScrapeOptions,
    StartScrapeJobParams,
    CreateSessionParams,
)
load_dotenv(override=True) 
app = FastAPI(title="Website Clone API", version="1.0.0")
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # or ["*"] for all origins (not recommended for production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
HYPERBROWSER_API_KEY = os.getenv("HYPERBROWSER_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# print("HYper key: ",HYPERBROWSER_API_KEY,"\n gemini: ",GEMINI_API_KEY)


HYPERBROWSER_BASE_URL = "https://api.hyperbrowser.ai/api"


# Initialize Gemini
newclient = genai.Client(api_key=GEMINI_API_KEY)



# #############################################################################
hyperbrowser.api_key = HYPERBROWSER_API_KEY
scraper = Hyperbrowser(api_key=HYPERBROWSER_API_KEY)
# genai.configure(api_key=GEMINI_API_KEY)



# Request body model
class CloneRequest(BaseModel):
    url: str

@app.post("/api/clone/advanced")
async def clone_website_advanced(req: CloneRequest):
    print("Hello entered")
    url = req.url
    print(f"Advanced cloning for: {url}")

    try:
        scrape_result = scraper.scrape.start_and_wait(
            StartScrapeJobParams(
                url=url,
                session_options=CreateSessionParams(
                    accept_cookies=False,
                    use_stealth=True,
                    use_proxy=False,
                    wait_until="networkidle", 
                    solve_captchas=False,
                    scroll_page=True
                ),
                scrape_options=ScrapeOptions(
                    formats=["markdown", "html", "links", "screenshot"],
                    only_main_content=False,
                    exclude_tags=[],
                    include_tags=[],
                ),
            )
        )
        # gemini-2.5-pro-exp-03-25
    except Exception as e:
        print(f"Hyperbrowser advanced scrape failed: {e}")
        raise HTTPException(status_code=502, detail="Advanced scrape failed")

    html = scrape_result.data.html
    screenshot_url = scrape_result.data.screenshot
    links = scrape_result.data.links

    if not html:
        raise HTTPException(status_code=500, detail="No HTML returned from advanced scrape")

    try:
        # model = genai.GenerativeModel("gemini-pro")
        prompt = f"""
        You are a professional frontend developer.

        Using the provided raw HTML content, the list of internal links, and the screenshot as a visual reference, reconstruct the **entire** webpage exactly as it appears in the screenshot.

        Instructions:
        - Accurately **match the layout, structure, colors, and visual style** shown in the screenshot.
        - If the provided HTML is incomplete or broken, you must **infer and fill in the missing sections**.
        - Preserve the structure and styling **through to the bottom of the page** — do not truncate or skip any part.
        - Use the screenshot and links to ensure completeness and correctness of all sections.
        - Include all necessary CSS (either inline or in `<style>` tags in the `<head>`).
        - Ensure responsive design where applicable.

        Provided HTML:
        {html}

        Links:
        {links}

        Screenshot (visual reference only):
        {screenshot_url}

        Output a single, fully valid, complete HTML5 document.
        Do not include explanations or extra text — only the HTML.
        """

        
        response = newclient.models.generate_content(model="gemini-2.5-flash-preview-05-20",contents=prompt)
        cloned_html = response.text
        print("cloned_html: ", cloned_html)
    except Exception as e:
        print(f"Gemini generation failed: {e}")
        raise HTTPException(status_code=502, detail=f"Gemini generation failed: ${e}")

    return {
        "cloned_html": cloned_html,
        "links":links,
        "screenshot_url": screenshot_url
    }

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Website Clone API is running"}

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Website Clone API", "version": "1.0.0"}




# prompt = f"""
# You are a frontend developer. Using this HTML content,the links available and the screenshot as visual reference, generate a complete website same as the screenshot.

# HTML:
# {html}
# links:
# {links}
# Screenshot (reference only): {screenshot_url}

# Return a single valid HTML5 document.
#         """