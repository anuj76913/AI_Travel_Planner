# Phase-Wise Implementation Plan: Multi-Agent Travel Planner

This document outlines the step-by-step implementation plan for building the Dubai AI Travel Planner, based on the defined architecture and problem statement.

## Prerequisites & Setup
* **Repository Setup**: Initialize version control and define standard directory structures for agents, tools, and configurations.
* **Environment Configuration**: Set up the Python/TypeScript environment (e.g., virtual environment, `package.json`).
* **Dependencies**: Install core multi-agent frameworks (e.g., LangChain, LangGraph, or AutoGen) and LLM SDKs (Groq, Gemini).
  * **LLM Allocation**: Orchestrator, Budget, Logistics, and Destination agents will use **llama-3.3-70b-versatile** via Groq. The Review agent will use **Gemini 2.5 Flash** as its LLM.
* **API Keys Management**: Create a `.env` file to securely store necessary API keys (Groq API, Gemini API, Search API).

---

## Phase 1: Foundation & Mocked Agents (POC)
**Goal**: Establish the Orchestrator's capability to parse requests, delegate tasks to worker agents, and synthesize a final output using scraped baseline data. This validates the core control flow.

* **Step 1.1: Orchestrator Basic Setup**
  * Develop the Orchestrator agent to accept a natural language request.
  * Implement LLM prompts to extract structured constraints: Destination (Dubai), Duration, Budget, Preferences, and Avoidances.
* **Step 1.2: Build Baseline Worker Agents (Data Scraping)**
  * **Destination Agent**: Extracts initial attraction data from reliable sources like `https://en.wikivoyage.org/wiki/Dubai#Budget` instead of using static mock lists.
  * **Logistics Agent**: Returns baseline transit data and neighborhoods scraped from travel guides.
  * **Budget Agent**: Extracts foundational cost estimates for accommodations, food, and activities directly from `https://en.wikivoyage.org/wiki/Dubai#Budget`.
* **Step 1.3: Integration & Synthesis (The Graph)**
  * Connect the Orchestrator to these baseline agents using a framework like LangGraph.
  * Enable the Orchestrator to synthesize the responses into a coherent day-by-day draft itinerary.

---

## Phase 2: Tool & API Integration
**Goal**: Replace mock agents with functional, autonomous agents capable of fetching real-world, real-time data using external APIs.

* **Step 2.1: Destination Research Agent Upgrades**
  * Integrate a Web Search tool (e.g., Tavily, Google Custom Search).
  * Integrate Places/Reviews APIs (e.g., Google Places) to fetch real Dubai venues, ratings, descriptions, and operating hours based on the user's preferences.
* **Step 2.2: Logistics Agent Upgrades**
  * Integrate Web Search tool to look up current transit options or neighborhood vibes.
  * Implement logic/prompts to cluster daily activities geographically, reducing unnecessary travel time across Dubai.
* **Step 2.3: Budget Agent Upgrades**
  * Integrate Currency Conversion APIs for real-time rates (e.g., USD to AED).
  * Build a heuristic calculation module using live or realistic data points to track the cumulative cost against the user's budget.
* **Step 2.4: System Hardening**
  * Implement error handling for API rate limits and timeouts.
  * Add safeguards against LLM hallucinations (ensuring places actually exist).

---

## Phase 3: Validation, Feedback Loop & Polish
**Goal**: Implement the Review Agent, establish the autonomous revision loop, and finalize the system output for the user.

* **Step 3.1: Review Agent Implementation**
  * Create the Review Agent with strict evaluation criteria mapping directly to the Orchestrator's extracted constraints (e.g., "Is total cost <= $3000?", "Is it restricted to Dubai?").
* **Step 3.2: Autonomous Feedback Loop**
  * Update the orchestration flow to route the Orchestrator's draft to the Review Agent.
  * If the Review Agent rejects the draft, capture specific feedback (e.g., "Day 3 exceeds budget") and route the task back to the Orchestrator/Worker agents for targeted revisions.
* **Step 3.3: Output Formatting**
  * Ensure the final output is structured beautifully (Markdown, JSON) with clear day-by-day breakdowns, summarized budget tables, and practical logistics tips.
* **Step 3.4: User Acceptance Testing (UAT)**
  * Run the system against various real-world prompts (e.g., low budgets, extreme luxury, unique preferences like "skydiving" vs "historical souks").

---

## Phase 4: Future Enhancements (Post-MVP)
* **Live Bookings**: Integrate with APIs like Amadeus or Skyscanner for real-time hotel/flight booking capabilities.
* **User Interface**: Build a web application (e.g., Next.js/React) to interact with the multi-agent system visually, showing agent reasoning in real-time.
* **Personalization Memory**: Implement a vector database to remember user preferences across multiple separate trip planning sessions.
