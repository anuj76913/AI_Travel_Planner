import os
import sys
import webbrowser
import uvicorn
from dotenv import load_dotenv

def main():
    load_dotenv()
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    print("=" * 60)
    print("[*] Starting AI Travel Planner (Multi-Agent System)")
    print("=" * 60)
    print("[*] Web UI: http://localhost:8000")
    print("[*] Press CTRL+C to stop the server.\n")

    try:
        webbrowser.open("http://localhost:8000")
    except Exception:
        pass

    uvicorn.run("src.api.server:app", host="127.0.0.1", port=8000, reload=True)

if __name__ == "__main__":
    main()
