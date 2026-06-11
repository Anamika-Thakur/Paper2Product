from langgraph.graph import StateGraph, END
from app.graph.state import ResearchState
from app.agents.research_analyst    import research_analyst_node
from app.agents.technical_validator import technical_validator_node
from app.agents.market_discovery    import market_discovery_node
from app.agents.customer_persona    import customer_persona_node
from app.agents.competitor_intel    import competitor_intel_node
from app.agents.product_strategist  import product_strategist_node
from app.agents.mvp_planner         import mvp_planner_node
from app.agents.architect           import architect_node
from app.agents.revenue_strategy    import revenue_strategy_node
from app.agents.risk_analyst        import risk_analyst_node
from app.agents.investment_agent    import investment_agent_node
from app.agents.knowledge_graph     import knowledge_graph_node
from app.agents.opportunity_scorer  import opportunity_scorer_node
from app.agents.debate              import debate_node
from app.agents.judge               import judge_node


def build_workflow():
    g = StateGraph(ResearchState)

    # Register nodes
    for name, fn in [
        ("research_analyst",    research_analyst_node),
        ("technical_validator", technical_validator_node),
        ("market_discovery",    market_discovery_node),
        ("customer_persona",    customer_persona_node),
        ("competitor_intel",    competitor_intel_node),
        ("product_strategist",  product_strategist_node),
        ("mvp_planner",         mvp_planner_node),
        ("architect",           architect_node),
        ("revenue_strategy",    revenue_strategy_node),
        ("risk_analyst",        risk_analyst_node),
        ("investment_agent",    investment_agent_node),
        ("knowledge_graph",     knowledge_graph_node),
        ("opportunity_scorer",  opportunity_scorer_node),
        ("debate",              debate_node),
        ("judge",               judge_node),
    ]:
        g.add_node(name, fn)

    # Sequential pipeline
    g.set_entry_point("research_analyst")
    edges = [
        ("research_analyst",    "technical_validator"),
        ("technical_validator", "market_discovery"),
        ("market_discovery",    "customer_persona"),
        ("customer_persona",    "competitor_intel"),
        ("competitor_intel",    "product_strategist"),
        ("product_strategist",  "mvp_planner"),
        ("mvp_planner",         "architect"),
        ("architect",           "revenue_strategy"),
        ("revenue_strategy",    "risk_analyst"),
        ("risk_analyst",        "investment_agent"),
        ("investment_agent",    "knowledge_graph"),   # Feature 10
        ("knowledge_graph",     "opportunity_scorer"),# Feature 3
        ("opportunity_scorer",  "debate"),            # Feature 2
        ("debate",              "judge"),
        ("judge",               END),
    ]
    for src, dst in edges:
        g.add_edge(src, dst)

    return g.compile()


workflow = build_workflow()
