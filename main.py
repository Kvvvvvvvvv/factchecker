from fastapi import FastAPI
import asyncio
from fastapi.middleware.cors import CORSMiddleware
api=FastAPI()
# Allow requests from your frontend (VS Code Live Server)
origins = [
    "http://127.0.0.1:5502",  # This is the key line
    "http://localhost:5502",
]

api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
from crew import crew
import re

@api.get('/result/{query}')
async def get_result(query: str):
    result = await asyncio.to_thread(crew.kickoff, inputs={'input': query})
    result_str = str(result)
    
    # Parse the verdict and confidence score
    verdict_match = re.search(r'VERDICT:\s*(TRUE|FALSE|UNCLEAR)', result_str, re.IGNORECASE)
    score_match = re.search(r'CONFIDENCE_SCORE:\s*(\d+)', result_str, re.IGNORECASE)
    
    verdict = verdict_match.group(1).upper() if verdict_match else "UNCLEAR"
    score = int(score_match.group(1)) if score_match else 0
    
    return {
        'verdict': verdict,
        'confidence_score': score,
        'full_report': result_str
    }