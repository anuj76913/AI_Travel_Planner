import json
from langchain_core.messages import SystemMessage, HumanMessage
from src.config import get_groq_llm
from src.state import TravelState

def orchestrator_node(state: TravelState) -> TravelState:
    """
    Parses the user's natural language request to extract constraints.
    """
    print("--- ORCHESTRATOR: Extracting Constraints ---")
    llm = get_groq_llm(temperature=0.0)
    
    system_prompt = """
    You are the Orchestrator for an AI Travel Planner.
    Your job is to extract the following information from the user's travel request and return it STRICTLY as a JSON object:
    {
        "destination": "Name of the destination city (e.g., Dubai)",
        "duration": number of days (integer),
        "budget": total budget in USD (float, extract the number),
        "preferences": [list of strings like "food", "shopping", "beaches"],
        "avoidances": [list of strings like "crowds", "heat"]
    }
    If any field is missing or ambiguous, make a reasonable guess based on the prompt or leave it empty/default.
    Return ONLY valid JSON, no markdown formatting.
    """
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=state["user_request"])
    ]
    
    response = llm.invoke(messages)
    
    try:
        # Clean the response in case the LLM returned markdown code blocks
        content = response.content.strip()
        if content.startswith("```json"):
            content = content[7:]
        if content.endswith("```"):
            content = content[:-3]
            
        parsed_data = json.loads(content)
        
        return {
            "destination": parsed_data.get("destination", "Dubai"),
            "duration": parsed_data.get("duration", 5),
            "budget": parsed_data.get("budget", 3000.0),
            "preferences": parsed_data.get("preferences", []),
            "avoidances": parsed_data.get("avoidances", [])
        }
    except Exception as e:
        print(f"Error parsing orchestrator output: {e}. Using defaults.")
        # Fallback to defaults if parsing fails
        return {
            "destination": "Dubai",
            "duration": 5,
            "budget": 3000.0,
            "preferences": ["sightseeing"],
            "avoidances": []
        }
