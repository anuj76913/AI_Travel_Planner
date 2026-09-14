from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.prebuilt import create_react_agent
from src.config import get_groq_llm
from src.state import TravelState

from src.tools.search import destination_search
from src.tools.currency import convert_currency

def destination_node(state: TravelState) -> dict:
    """
    Destination Agent: Recommends POIs using Web Search.
    """
    print("--- DESTINATION AGENT: Researching Attractions ---")
    llm = get_groq_llm(temperature=0.7)
    
    system_prompt = f"""
    You are the Destination Research Agent for an AI Travel Planner.
    Your task is to recommend 5-7 specific attractions, neighborhoods, and dining experiences in {state['destination']}.
    
    User Preferences: {state['preferences']}
    User Avoidances: {state['avoidances']}
    
    Previous Reviewer Feedback (if any): {state.get('review_feedback', 'None')}
    If there is feedback, you MUST adjust your recommendations to satisfy it.
    
    Use the `destination_search` tool to find current and highly rated places that match these preferences.
    Do NOT recommend items that match the avoidances.
    Return your final recommendations as a clear, bulleted markdown list.
    """
    
    # Create a ReAct agent that has access to the search tool
    agent = create_react_agent(llm, tools=[destination_search])
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Please research {state['destination']} based on my preferences.")
    ]
    
    # Run the internal agent loop
    response = agent.invoke({"messages": messages})
    
    # The final message in the state is the agent's final answer
    final_answer = response["messages"][-1].content
    return {"destination_recommendations": final_answer}


def logistics_node(state: TravelState) -> dict:
    """
    Logistics Agent: Recommends transit logic using general search or internal knowledge.
    """
    print("--- LOGISTICS AGENT: Planning Transit ---")
    llm = get_groq_llm(temperature=0.3)
    
    system_prompt = f"""
    You are the Logistics Agent for an AI Travel Planner.
    Based on the fact that the user is visiting {state['destination']} for {state['duration']} days, 
    recommend the best neighborhood(s) to stay and provide practical transit advice.
    
    User Preferences: {state['preferences']}
    User Avoidances: {state['avoidances']}
    
    Previous Reviewer Feedback (if any): {state.get('review_feedback', 'None')}
    If there is feedback, you MUST adjust your recommendations to satisfy it.
    
    Use the `destination_search` tool if you need to look up current transit options or neighborhood vibes.
    Provide your output as a clear markdown summary.
    """
    
    agent = create_react_agent(llm, tools=[destination_search])
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Plan the logistics for {state['destination']}.")
    ]
    
    response = agent.invoke({"messages": messages})
    final_answer = response["messages"][-1].content
    return {"logistics_recommendations": final_answer}


def budget_node(state: TravelState) -> dict:
    """
    Budget Agent: Estimates costs and converts currency.
    """
    print("--- BUDGET AGENT: Estimating Costs ---")
    llm = get_groq_llm(temperature=0.1)
    
    system_prompt = f"""
    You are the Budget Agent for an AI Travel Planner.
    The user has a budget of ${state['budget']} (USD) for a {state['duration']}-day trip to {state['destination']}.
    
    Use the `convert_currency` tool to determine what this budget is in the local currency (e.g., AED).
    Estimate the daily costs for Accommodation, Food, Transport, and Activities in both USD and the local currency.
    
    Determine if ${state['budget']} is Realistic, Tight, or Luxurious. 
    Provide a breakdown table in markdown format and a brief summary of how to allocate the funds.
    
    Previous Reviewer Feedback (if any): {state.get('review_feedback', 'None')}
    If there is feedback, you MUST adjust your calculations to satisfy it.
    """
    
    agent = create_react_agent(llm, tools=[convert_currency])
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Break down my ${state['budget']} budget for {state['destination']}.")
    ]
    
    response = agent.invoke({"messages": messages})
    final_answer = response["messages"][-1].content
    return {"budget_recommendations": final_answer}
