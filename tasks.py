from crewai import Task
from tools import search_tool,factcheck_tool
from agent import scraper_agent,truth_checker_agent

scraper_task = Task(
    description=(
        "CLAIM TO INVESTIGATE: {input}\n\n"
        "YOUR MISSION:\n"
        "1. Search for the EXACT claim using multiple search queries\n"
        "2. Find at least 3-5 credible sources from:\n"
        "   - Major news outlets (BBC, Reuters, AP, CNN, etc.)\n"
        "   - Fact-checking websites (Snopes, PolitiFact, FactCheck.org, AFP Fact Check)\n"
        "   - Official statements or press releases\n"
        "   - Academic or government sources\n"
        "3. For each source, extract:\n"
        "   - Full URL\n"
        "   - Publication date\n"
        "   - Key facts (especially dates, numbers, names)\n"
        "   - Direct quotes or evidence\n"
        "4. Look for contradictions or updates to the story\n"
        "5. Note the source's credibility and potential bias\n\n"
        "IMPORTANT: Cast a wide net but prioritize quality over quantity."
    ),
    expected_output=(
        "A comprehensive research report containing:\n"
        "- 3-5 credible sources with full details\n"
        "- Key facts extracted from each source\n"
        "- Any contradictions or conflicting information found\n"
        "- Timeline of events if applicable\n"
        "- Source credibility assessment"
    ),
    tools=[search_tool],
    agent=scraper_agent
)

factcheck_task = Task(
    description=(
        "CLAIM TO VERIFY: {input}\n\n"
        "YOUR MISSION:\n"
        "Using the research provided by the investigator, determine the TRUTH:\n\n"
        "ANALYSIS STEPS:\n"
        "1. Review ALL sources provided by the research investigator\n"
        "2. Cross-reference facts across multiple sources\n"
        "3. Check for consistency in:\n"
        "   - Dates and times (be EXACT - Dec 4 vs Dec 5 matters!)\n"
        "   - Numbers and statistics\n"
        "   - Names and spellings\n"
        "   - Locations and events\n"
        "4. Identify any contradictions or discrepancies\n"
        "5. Consider the credibility and bias of each source\n"
        "6. Look for official confirmations or denials\n\n"
        "VERDICT GUIDELINES:\n"
        "- TRUE: The claim is accurate with strong evidence from multiple credible sources\n"
        "- FALSE: The claim is incorrect or misleading, with evidence proving otherwise\n"
        "- UNCLEAR: Insufficient evidence, conflicting information, or claim cannot be verified\n\n"
        "CONFIDENCE SCORE GUIDELINES (0-100):\n"
        "- 90-100: Multiple highly credible sources confirm, no contradictions\n"
        "- 70-89: Good evidence from credible sources, minor inconsistencies\n"
        "- 50-69: Some evidence but contradictions exist or sources less reliable\n"
        "- 30-49: Conflicting information, unclear sources\n"
        "- 0-29: Very little evidence or highly contradictory\n\n"
        "IMPORTANT:\n"
        "- If there are ANY contradictions in key details (dates, numbers), verdict must be UNCLEAR\n"
        "- Always cite specific sources with URLs\n"
        "- Explain your reasoning clearly\n"
        "- Be precise and objective\n"
        "- ALWAYS provide a confidence score"
    ),
    expected_output=(
        "VERDICT: [TRUE / FALSE / UNCLEAR]\n"
        "CONFIDENCE_SCORE: [0-100]\n\n"
        "EVIDENCE:\n"
        "- Summary of supporting evidence with source URLs\n"
        "- Any contradicting evidence with source URLs\n\n"
        "REASONING:\n"
        "- Clear explanation of why this verdict was reached\n"
        "- Why this confidence score was assigned\n\n"
        "SOURCES:\n"
        "- List of all sources consulted with URLs"
    ),
    tools=factcheck_tool,
    agent=truth_checker_agent,
    context=[scraper_task]
)