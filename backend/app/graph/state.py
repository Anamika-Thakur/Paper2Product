from typing import TypedDict, Optional


class ResearchState(TypedDict):
    project_id: str
    raw_text: str

    research_profile:      Optional[dict]
    innovation_score:      Optional[dict]
    market_opportunities:  Optional[dict]
    customer_personas:     Optional[list]
    competitive_landscape: Optional[dict]
    product_concepts:      Optional[list]
    mvp_plan:              Optional[dict]
    architecture:          Optional[dict]
    revenue_strategy:      Optional[dict]
    risk_profile:          Optional[dict]
    investment_score:      Optional[dict]
    knowledge_graph:       Optional[dict]
    opportunity_scores:    Optional[dict]
    debate_transcript:     Optional[list]
    final_report:          Optional[dict]

    agent_metadata:  Optional[dict]
    awaiting_hitl:   Optional[str]
    hitl_approved:   Optional[bool]
    hitl_feedback:   Optional[str]
    error:           Optional[str]


AGENT_STEPS = [
    ("research_analyst",    "Research Analyst",        7),
    ("technical_validator", "Technical Validator",    14),
    ("market_discovery",    "Market Discovery",       21),
    ("customer_persona",    "Customer Persona",       28),
    ("competitor_intel",    "Competitor Intelligence",35),
    ("product_strategist",  "Product Strategist",     42),
    ("mvp_planner",         "MVP Planner",            49),
    ("architect",           "Technical Architect",    56),
    ("revenue_strategy",    "Revenue Strategy",       63),
    ("risk_analyst",        "Risk Analyst",           70),
    ("investment_agent",    "Investment Agent",       77),
    ("knowledge_graph",     "Knowledge Graph",        82),
    ("opportunity_scorer",  "Opportunity Scorer",     87),
    ("debate",              "Agent Debate",           93),
    ("judge",               "Judge Agent",           100),
]

# ── All agents on Groq — truly free, no daily limits ─────────────────────────
# llama-3.3-70b-versatile : best quality, 6000 TPM free
# llama-3.1-8b-instant    : fastest,    20000 TPM free  ← use for lighter agents
#
# Strategy: alternate between the two models so we never hit per-model RPM cap.
# Heavy reasoning agents → 70b, lighter extraction agents → 8b

MODEL_ROUTING = {
    # Heavy agents — need best reasoning
    "research_analyst":    ("groq", "llama-3.3-70b-versatile"),
    "technical_validator": ("groq", "llama-3.1-8b-instant"),      # lighter task
    "market_discovery":    ("groq", "llama-3.3-70b-versatile"),
    "customer_persona":    ("groq", "llama-3.1-8b-instant"),
    "competitor_intel":    ("groq", "llama-3.3-70b-versatile"),
    "product_strategist":  ("groq", "llama-3.3-70b-versatile"),
    "mvp_planner":         ("groq", "llama-3.1-8b-instant"),
    "architect":           ("groq", "llama-3.1-8b-instant"),
    "revenue_strategy":    ("groq", "llama-3.3-70b-versatile"),
    "risk_analyst":        ("groq", "llama-3.1-8b-instant"),
    "investment_agent":    ("groq", "llama-3.3-70b-versatile"),
    "knowledge_graph":     ("groq", "llama-3.1-8b-instant"),
    "opportunity_scorer":  ("groq", "llama-3.3-70b-versatile"),
    "debate":              ("groq", "llama-3.1-8b-instant"),       # 4 calls, use fast model
    "judge":               ("groq", "llama-3.3-70b-versatile"),   # most important — use best
}

FIELD_MAP = {
    "research_analyst":    "research_profile",
    "technical_validator": "innovation_score",
    "market_discovery":    "market_opportunities",
    "customer_persona":    "customer_personas",
    "competitor_intel":    "competitive_landscape",
    "product_strategist":  "product_concepts",
    "mvp_planner":         "mvp_plan",
    "architect":           "architecture",
    "revenue_strategy":    "revenue_strategy",
    "risk_analyst":        "risk_profile",
    "investment_agent":    "investment_score",
    "knowledge_graph":     "knowledge_graph",
    "opportunity_scorer":  "opportunity_scores",
    "debate":              "debate_transcript",
    "judge":               "final_report",
}

PRICING = {
    "llama-3.3-70b-versatile": (0.00059, 0.00079),
    "llama-3.1-8b-instant":    (0.00005, 0.00008),
}