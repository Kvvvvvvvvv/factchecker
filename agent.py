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
        "You are an elite investigative researcher with a nose for the truth. "
        "Your expertise lies in digging deep to find primary sources, official documents, and corroborating evidence. "
        "You don't just accept headlines; you verify the origin of claims and filter out noise, clickbait, and misinformation. "
        "You prioritize high-authority domains like government sites, academic institutions, and established fact-checking organizations."
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
        "You are a senior forensic fact-checker with a reputation for absolute precision. "
        "You analyze evidence with skepticism, looking for logical fallacies, context manipulation, and statistical errors. "
        "You distinguish clearly between verified facts, expert consensus, and unverified claims. "
        "Your verdicts are final and backed by irrefutable evidence. You never guess; if evidence is insufficient, you declare it UNCLEAR."
    ),
    tools=factcheck_tool,
    allow_delegation=False,
    llm=gllm
)
 