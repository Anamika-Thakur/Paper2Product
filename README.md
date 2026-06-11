# Research-to-Product Advisor

AI Venture Studio — transforms research papers into product opportunities using 15 specialist agents.

---

## Local setup (VS Code)

### 1. Clone and install

```bash
git clone <your-repo>
cd research-to-product
```

### 2. Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # fill in your keys
uvicorn app.main:app --reload --port 8000
```

### 3. Frontend (new terminal)

```bash
cd frontend
npm install
cp .env.example .env.local      # set REACT_APP_API_URL=http://localhost:8000
npm start
```

Open http://localhost:3000

---

## Deploy

### Backend → Render

1. Push to GitHub
2. New Web Service on render.com → connect repo → Root Dir: `backend`
3. Build command: `pip install -r requirements.txt`
4. Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add all env vars from `.env.example`

### Frontend → Vercel

1. Import repo on vercel.com → Root Dir: `frontend`
2. Add env var: `REACT_APP_API_URL=https://your-render-app.onrender.com`
3. Deploy

### Database → Neon (PostgreSQL)

1. Create project at neon.tech
2. Copy connection string → set as `DATABASE_URL` in Render env vars

### Cache → Upstash (Redis)

1. Create database at upstash.com → REST API tab
2. Copy `UPSTASH_REDIS_REST_URL` and `UPSTASH_REDIS_REST_TOKEN` → add to Render

---

## Architecture

```
Frontend (React/Vercel)
        ↓
Backend API (FastAPI/Render)
        ↓
Agent Pipeline (LangGraph — 15 nodes)
  ├── Research Analyst       (Claude)
  ├── Technical Validator    (Claude)
  ├── Market Discovery       (Groq + web search)
  ├── Customer Persona       (Claude)
  ├── Competitor Intel       (Groq + web search)
  ├── Product Strategist     (Claude)
  ├── MVP Planner            (Claude)
  ├── Technical Architect    (Claude)
  ├── Revenue Strategy       (GPT-4o)
  ├── Risk Analyst           (Claude)
  ├── Investment Agent       (GPT-4o)
  ├── Knowledge Graph        (Claude)
  ├── Opportunity Scorer     (Claude)
  ├── Debate Stage           (Claude × 4 personas)
  └── Judge Agent            (Claude)
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
- **Multi-Model Routing** — Claude for analysis, Groq for market/competitive
- **Human-in-the-Loop** — user can approve/reject market selection before pipeline continues
- **Evaluation Metrics** — per-agent runtime, token usage, cost dashboard
- **Knowledge Graph** — entities, relationships, concept clusters
