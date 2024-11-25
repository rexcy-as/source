# # /web/backend/api/scrape.py

# from fastapi import FastAPI, APIRouter
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# import subprocess
# import json

# app = FastAPI()

# # Allow CORS for requests from your frontend (localhost:3000)
# origins = [
#     "http://localhost:3000",  # Frontend
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,  # Allows requests from the specified origin
#     allow_credentials=True,
#     allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
#     allow_headers=["*"],  # Allows all headers
# )

# router = APIRouter()

# class ScrapeRequest(BaseModel):
#     url: str

# class ScrapeResponse(BaseModel):
#     event_name: str
#     tickets: list

# @router.post("/scrape", response_model=ScrapeResponse)
# async def scrape(request: ScrapeRequest):
#     # Call the scraping script from the CLI
#     url = request.url
#     result = subprocess.run(
#         ['python3', 'cli/main.py', url],
#         capture_output=True,
#         text=True
#     )
    
#     if result.returncode != 0:
#         return {"error": "Scraping failed"}

#     # Parse the JSON output from the scraping script
#     scraped_data = json.loads(result.stdout)
    
#     return scraped_data

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}
