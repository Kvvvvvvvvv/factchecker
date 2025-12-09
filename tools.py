from crewai_tools import TavilySearchTool
from dotenv import load_dotenv
load_dotenv()
import os
os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")

# Initialize the tool for internet searching capabilities
# Using Tavily only - no Selenium scraping for better performance
search_tool = TavilySearchTool(
    max_results=5,  # Limit to 5 results for efficiency
    include_answer=True,  # Get direct AI-generated answers from Tavily
    include_raw_content=True,  # Get content snippets from search results
)

# Use only Tavily search tool - no web scraping needed
factcheck_tool = [search_tool]