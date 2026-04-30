# Application Design Plan

## Overview
This plan dictates the structural and technical bounds established for the FraudShield application, bridging the business requirements (synthetic data tracking, risk algorithms, GenAI insights) into functional development components.

## Execution Checklist
- [x] Generate `components.md` with system blocks (Streamlit UI, FastAPI, Core Rule Engine, Gemini Gateway, SQLite).
- [x] Generate `component-methods.md` mapping high-level functional signatures (e.g., risk scoring triggers, Gemini payloads).
- [x] Generate `services.md` outlining the orchestration protocols across boundaries.
- [x] Generate `component-dependency.md` with a detailed Mermaid flowchart explicitly demonstrating memory-bounded (4GB RAM) dependencies and constraints.

## Clarification Questions (Retrospective / Bypassed)

*Note: Application Design was fast-tracked via a directive to enforce NFR mapping visually. These questions are retained for audit trailing.*

### Question 1: Frontend/Backend Protocol
For communication between the Streamlit UI and the FastAPI backend, do you prefer REST API calls or WebSockets (due to the potential continuous generation of synthetic data)?

A) Standard REST API (Polling & Pagination)
B) WebSockets (Real-time data streams)
X) Other (please describe after [Answer]: tag below)

[Answer]: A (Implied via fast-track constraint on 4GB limits requiring chunked REST payloads)

### Question 2: AI Orchestration Logic
Should the Gemini gateway exist as an entirely decoupled microservice, or just an encapsulated function within the FastAPI root application?

A) Encapsulated Function (Simpler to manage locally)
B) Decoupled Microservice (Easier to scale later but uses more baseline RAM)
X) Other (please describe after [Answer]: tag below)

[Answer]: A (Implied via NFR memory design constraints)
