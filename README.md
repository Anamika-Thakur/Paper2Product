# Paper-to-Product Advisor

Give Your Vision Weight — transforms research papers into product opportunities using 15 specialist agents.

---

## Architecture

```
Frontend (React/Vercel)
        ↓
Backend API (FastAPI/Render)
        ↓
Agent Pipeline (LangGraph — 15 nodes)
  ├── Research Analyst       
  ├── Technical Validator    
  ├── Market Discovery       
  ├── Customer Persona       
  ├── Competitor Intel       
  ├── Product Strategist     
  ├── MVP Planner            
  ├── Technical Architect    
  ├── Revenue Strategy       
  ├── Risk Analyst           
  ├── Investment Agent      
  ├── Knowledge Graph        
  ├── Opportunity Scorer     
  ├── Debate Stage           
  └── Judge Agent           
        ↓
PostgreSQL (Neon) + Redis (Upstash)
```

## Features

- **Agent Memory & Reasoning Logs** — every agent stores reasoning steps, confidence score, and source citations
- **Agent Debate Stage** — 4 agents argue FOR/AGAINST/CHALLENGE/SKEPTICAL; Judge resolves conflicts
- **Opportunity Scoring Framework** — 6-dimension weighted score (not just one number)
- **Portfolio Analysis** — rank multiple papers by commercial viability
- **Report Export** — PDF, DOCX, Markdown
- **Source Citations** — every insight linked to its data source
- **Human-in-the-Loop** — user can approve/reject market selection before pipeline continues
- **Evaluation Metrics** — per-agent runtime, token usage, cost dashboard
- **Knowledge Graph** — entities, relationships, concept clusters
