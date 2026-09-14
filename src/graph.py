from langgraph.graph import StateGraph, END
from langchain_core.messages import SystemMessage, HumanMessage
from src.state import TravelState
from src.config import get_groq_llm
from src.agents.orchestrator import orchestrator_node
from src.agents.workers import destination_node, logistics_node, budget_node
from src.agents.review import review_node

def synthesizer_node(state: TravelState) -> dict:
    """
    Combines the outputs of all worker agents into a final day-by-day itinerary.
    """
    print("--- SYNTHESIZER: Compiling Final Itinerary ---")
    llm = get_groq_llm(temperature=0.5)
    
    system_prompt = f"""
    You are the Master Travel Orchestrator. 
    Your job is to synthesize the recommendations from the specialized agents into a cohesive, beautifully formatted Markdown itinerary for {state['destination']} over {state['duration']} days.
    
    Make sure to:
    1. Provide a brief introduction acknowledging the user's constraints (Budget: ${state['budget']}, Preferences: {state['preferences']}, Avoidances: {state['avoidances']}).
    2. Include a section for Accommodation & Logistics (based on the Logistics Agent's input).
    3. Include a Budget Breakdown (based on the Budget Agent's input).
    4. Provide a realistic Day-by-Day itinerary that maps out the activities from the Destination Agent, keeping travel time between locations in mind.
    
    Format the output elegantly using markdown headers, bold text, and bullet points.
    """
    
    user_prompt = f"""
    Destination Recommendations:
    {state['destination_recommendations']}
    
    Logistics Recommendations:
    {state['logistics_recommendations']}
    
    Budget Recommendations:
    {state['budget_recommendations']}
    """
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ]
    
    response = llm.invoke(messages)
    return {"final_itinerary": response.content}


# Define the Graph
workflow = StateGraph(TravelState)

# Add Nodes
workflow.add_node("orchestrator", orchestrator_node)
workflow.add_node("destination", destination_node)
workflow.add_node("logistics", logistics_node)
workflow.add_node("budget", budget_node)
workflow.add_node("synthesizer", synthesizer_node)
workflow.add_node("review", review_node)

# Define the sequential flow to prevent hitting RPM/TPM rate limits
workflow.add_edge("orchestrator", "destination")
workflow.add_edge("destination", "logistics")
workflow.add_edge("logistics", "budget")
workflow.add_edge("budget", "synthesizer")
workflow.add_edge("synthesizer", "review")

# Conditional logic for the review node
def review_routing(state: TravelState):
    if state.get("is_approved", False) or state.get("revision_count", 0) >= 2:
        return "end"
    else:
        return "revise"

workflow.add_conditional_edges(
    "review",
    review_routing,
    {
        "end": END,
        "revise": "destination" # Loop back to destination to start the worker sequence again with feedback
    }
)

workflow.set_entry_point("orchestrator")

app = workflow.compile()
