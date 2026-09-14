import os
from src.graph import app

def run_travel_planner(user_request: str):
    print(f"\n--- Processing Request: '{user_request}' ---\n")
    
    # Initialize state
    initial_state = {
        "user_request": user_request
    }
    
    print("Starting Multi-Agent Workflow (Phase 2 with Real-Time Tools)...")
    
    # Run the graph
    final_state = app.invoke(initial_state)
    
    itinerary = final_state.get("final_itinerary", "Error generating itinerary.")
    is_approved = final_state.get("is_approved", False)
    feedback = final_state.get("review_feedback", "None")
    revisions = final_state.get("revision_count", 0)
    
    print("\n\n" + "="*50)
    print(f"FINAL ITINERARY (Approved: {is_approved} | Revisions: {revisions})")
    print(f"Reviewer Feedback: {feedback}")
    print("="*50 + "\n")
    print(itinerary)
    
    # Also save to a file
    with open("output.md", "w", encoding="utf-8") as f:
        f.write(itinerary)
    print("\nItinerary saved to output.md")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="AI Travel Planner")
    parser.add_argument("--prompt", type=str, default="Plan a 5-day trip to Dubai. $3,000 budget. Love food and shopping, hate crowds.", help="The travel request.")
    args = parser.parse_args()
    
    # Check if API key is set before running
    if not os.getenv("GROQ_API_KEY"):
        print("ERROR: GROQ_API_KEY environment variable is missing.")
        print("Please add it to your .env file or export it in your terminal.")
        exit(1)
        
    run_travel_planner(args.prompt)
