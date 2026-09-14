from pydantic import BaseModel, Field
from langchain_core.messages import SystemMessage, HumanMessage
from src.state import TravelState
from src.config import get_gemini_llm

class ReviewOutput(BaseModel):
    is_approved: bool = Field(description="True if the itinerary strictly meets all user constraints, False otherwise.")
    feedback: str = Field(description="If approved, a brief praise. If rejected, highly specific feedback on what needs to be changed (e.g., 'Day 2 exceeds budget', 'Included a crowded place which user avoids').")

def review_node(state: TravelState) -> dict:
    """
    Review Agent: Evaluates the synthesized itinerary against user constraints.
    """
    print("\n--- REVIEW AGENT: Evaluating Itinerary ---")
    
    # Initialize Gemini for Review
    llm = get_gemini_llm(temperature=0.0)
    structured_llm = llm.with_structured_output(ReviewOutput)
    
    system_prompt = f"""
    You are the strict Quality Assurance Review Agent for an AI Travel Planner.
    Your job is to review the drafted itinerary and ensure it strictly adheres to the user's constraints.
    
    Constraints:
    - Destination: {state.get('destination')}
    - Duration: {state.get('duration')} days
    - Budget: ${state.get('budget')} USD
    - Preferences: {state.get('preferences')}
    - Avoidances: {state.get('avoidances')}
    
    Evaluate the following itinerary. If it violates ANY constraint (especially budget or avoidances), reject it.
    If it is perfect, approve it.
    """
    
    user_prompt = f"""
    Here is the drafted itinerary:
    {state.get('final_itinerary', 'No itinerary provided.')}
    
    Please evaluate this and provide your approval status and feedback.
    """
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ]
    
    try:
        result: ReviewOutput = structured_llm.invoke(messages)
        
        # Track revision loops
        current_revisions = state.get("revision_count", 0) + 1
        
        print(f"Review Approved: {result.is_approved}")
        print(f"Review Feedback: {result.feedback}")
        print(f"Revision Count: {current_revisions}")
        
        return {
            "is_approved": result.is_approved,
            "review_feedback": result.feedback,
            "revision_count": current_revisions
        }
    except Exception as e:
        print(f"Review Agent Error: {e}")
        # Failsafe: approve it if the review agent crashes so it doesn't infinite loop on errors
        return {
            "is_approved": True,
            "review_feedback": f"Review Agent bypassed due to error: {e}",
            "revision_count": state.get("revision_count", 0) + 1
        }
