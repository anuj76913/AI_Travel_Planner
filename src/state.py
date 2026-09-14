from typing import TypedDict, List

class TravelState(TypedDict):
    """Represents the state of the travel planner."""
    user_request: str
    
    # Constraints extracted by the orchestrator
    destination: str
    duration: int
    budget: float
    preferences: List[str]
    avoidances: List[str]
    
    # Baseline scraped data
    baseline_data: str
    
    # Agent outputs
    destination_recommendations: str
    logistics_recommendations: str
    budget_recommendations: str
    
    # Final synthesized itinerary
    final_itinerary: str
    
    # Review / Feedback Loop variables
    review_feedback: str
    is_approved: bool
    revision_count: int
