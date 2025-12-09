from fastapi import FastAPI
import asyncio
from fastapi.middleware.cors import CORSMiddleware
import speech_recognition as sr

recognizer = sr.Recognizer()

def listen():
    """Listen for voice input and convert to text"""
    print("🎤 Initializing microphone...")
    try:
        with sr.Microphone() as source:
            print("🎤 Adjusting for ambient noise... (Please wait)")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print("🎤 Listening... Speak now!")
            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            except sr.WaitTimeoutError:
                print("❌ Listening timed out (no speech detected)")
                return {"error": "No speech detected. Please speak louder or closer to the mic."}

        try:
            print("🎤 Recognizing speech...")
            query = recognizer.recognize_google(audio)
            print(f"🎤 You said: {query}")
            return {"text": query.lower()}

        except sr.UnknownValueError:
            print("❌ Could not understand audio")
            return {"error": "Could not understand audio. Please speak clearly."}

        except sr.RequestError as e:
            print(f"❌ Service error: {e}")
            return {"error": f"Speech service error: {e}"}

    except Exception as e:
        print(f"❌ Microphone error: {str(e)}")
        return {"error": f"Microphone error: {str(e)}"}

api=FastAPI()

@api.get('/listen')
async def listen_endpoint():
    """Endpoint to trigger voice listening"""
    result = await asyncio.to_thread(listen)
    # If listen() returned a string (legacy), wrap it
    if isinstance(result, str):
        return {"text": result}
    return result

# Allow requests from your frontend (VS Code Live Server)
origins = ["*"]

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