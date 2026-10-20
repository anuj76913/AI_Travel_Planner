import json
import asyncio
import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.graph import app as graph_app

app = FastAPI(title="AI Travel Planner API")

# Path to the frontend HTML file
FRONTEND_DIR = Path(__file__).resolve().parent.parent.parent / "frontend"

# Allow CORS for local frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PlanRequest(BaseModel):
    prompt: str

@app.post("/plan")
async def plan_trip(req: PlanRequest):
    """
    Streaming endpoint that executes the LangGraph workflow
    and streams agent events as newline-delimited JSON.
    """
    initial_state = {"user_request": req.prompt}

    def event_generator():
        for chunk in graph_app.stream(initial_state):
            for node, state_update in chunk.items():
                
                payload = {
                    "node": node,
                    "status": "completed",
                }
                
                if node == "orchestrator":
                    payload["data"] = {
                        "destination": state_update.get("destination"),
                        "budget": state_update.get("budget"),
                        "duration": state_update.get("duration")
                    }
                elif node == "destination":
                    payload["data"] = state_update.get("destination_recommendations")
                elif node == "logistics":
                    payload["data"] = state_update.get("logistics_recommendations")
                elif node == "budget":
                    payload["data"] = state_update.get("budget_recommendations")
                elif node == "synthesizer":
                    payload["data"] = state_update.get("final_itinerary")
                elif node == "review":
                    payload["data"] = {
                        "is_approved": state_update.get("is_approved"),
                        "feedback": state_update.get("review_feedback"),
                        "revisions": state_update.get("revision_count")
                    }
                
                # Yield as a single JSON line followed by newline
                yield json.dumps(payload) + "\n"

    return StreamingResponse(event_generator(), media_type="application/x-ndjson")

@app.get("/health")
async def health_check():
    """Health check endpoint for deployment monitoring."""
    return {"status": "ok"}

@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    """Serve the frontend HTML file."""
    html_path = FRONTEND_DIR / "index.html"
    return HTMLResponse(content=html_path.read_text(encoding="utf-8"))

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("src.api.server:app", host="0.0.0.0", port=port, reload=False)
