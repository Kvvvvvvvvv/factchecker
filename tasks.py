from crewai import Task
from tools import search_tool,factcheck_tool
from agent import scraper_agent,truth_checker_agent

scraper_task = Task(
    description=(
        "CLAIM TO INVESTIGATE: {input}\n\n"
        "YOUR MISSION:\n"
        "1. Deconstruct the claim into key verifiable elements (who, what, when, where).\n"
        "2. Execute targeted search queries to find PRIMARY SOURCES (official reports, video evidence, direct quotes).\n"
        "3. Gather at least 3-5 high-credibility sources, prioritizing:\n"
        "   - Tier 1: Official government/institutional records, academic papers, direct video/audio.\n"
        "   - Tier 2: Major wire services (Reuters, AP, AFP) and established fact-checking bodies.\n"
        "   - Tier 3: Reputable major news outlets.\n"
        "4. For each source, extract:\n"
        "   - Full URL and Publication Date (crucial for timeline).\n"
        "   - Specific evidence supporting or refuting the claim.\n"
        "   - Context that might be missing from the claim.\n"
        "5. Explicitly look for 'fact check' articles related to this specific claim.\n\n"
        "IMPORTANT: Avoid circular reporting. Ensure sources are independent."
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
        "1. Review ALL sources provided by the research investigator.\n"
        "2. Cross-reference facts across multiple sources to identify the 'Ground Truth'.\n"
        "3. Check for consistency in:\n"
        "   - Dates and times (be EXACT - Dec 4 vs Dec 5 matters!)\n"
        "   - Numbers and statistics (check for manipulation).\n"
        "   - Names and spellings.\n"
        "   - Locations and events.\n"
        "4. Identify any contradictions or discrepancies between sources.\n"
        "5. Evaluate the credibility and potential bias of each source.\n"
        "6. Look for official confirmations or denials.\n\n"
        "VERDICT GUIDELINES:\n"
        "- TRUE: The claim is accurate with strong evidence from multiple credible sources.\n"
        "- FALSE: The claim is incorrect or misleading, with evidence proving otherwise.\n"
        "- UNCLEAR: Insufficient evidence, conflicting information, or claim cannot be verified.\n\n"
        "CONFIDENCE SCORE GUIDELINES (0-100):\n"
        "- 90-100: Multiple highly credible sources confirm, no contradictions. Irrefutable.\n"
        "- 70-89: Good evidence from credible sources, minor inconsistencies.\n"
        "- 50-69: Some evidence but contradictions exist or sources less reliable.\n"
        "- 30-49: Conflicting information, unclear sources.\n"
        "- 0-29: Very little evidence or highly contradictory.\n\n"
        "IMPORTANT:\n"
        "- If there are ANY contradictions in key details (dates, numbers), verdict must be UNCLEAR.\n"
        "- Always cite specific sources with URLs.\n"
        "- Explain your reasoning clearly.\n"
        "- Be precise and objective.\n"
        "- ALWAYS provide a confidence score."
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