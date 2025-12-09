from crewai import Agent,LLM
from tools import search_tool,factcheck_tool
from dotenv import load_dotenv
load_dotenv()
import os
from langchain_google_genai import ChatGoogleGenerativeAI
gllm=LLM(
    model="gemini/gemini-2.5-flash",
    verbose=True,
    temperature=0.5,
    api_key=os.getenv("GOOGLE_API_KEY")
)

scraper_agent = Agent(
    role='Fact Research Specialist',
    goal='Quickly search for the claim: {input} and gather key information from credible sources using search results only.',
    verbose=True,
    memory=False,
    backstory=(
        "You are an efficient researcher who specializes in finding reliable information quickly. "
        "You use search tools to find fact-checking sites and reputable news sources. "
        "You extract key information from search results without visiting every page."
    ),
    tools=[search_tool],
    allow_delegation=True,
    llm=gllm
)

truth_checker_agent = Agent(
    role='Fact Verification Analyst',
    goal='Analyze search results about "{input}" and provide a clear verdict (TRUE/FALSE/UNCLEAR) with a confidence score (0-100) and evidence with sources.',
    verbose=True,
    memory=False,
    backstory=(
        "You are a fact-checker who analyzes information from search results efficiently. "
        "You focus on:\n"
        "- Exact dates, numbers, and names\n"
        "- Multiple source verification\n"
        "- Identifying contradictions\n"
        "- Assessing confidence levels based on evidence quality\n"
        "You work fast and provide concise, accurate verdicts with confidence scores and source URLs."
    ),
    tools=factcheck_tool,
    allow_delegation=False,
    llm=gllm
)
 