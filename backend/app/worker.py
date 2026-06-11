"""
Pipeline runner — uses FastAPI BackgroundTasks (no Celery, no Redis queue needed).
Uses Upstash Redis purely as a progress cache for SSE streaming.
"""
import time
from datetime import datetime
from app.core.database import SessionLocal
from app.core.cache import set_progress, delete_progress
from app.models.project import Project
from app.graph.workflow import workflow
from app.graph.state import FIELD_MAP, AGENT_STEPS

STEP_PROGRESS = {s[0]: s[2] for s in AGENT_STEPS}


def run_analysis(project_id: str, raw_text: str):
    db = SessionLocal()
    project = None
    try:
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            return

        project.status = "processing"
        db.commit()

        state = {
            "project_id": project_id,
            "raw_text": raw_text,
            "research_profile": None,
            "innovation_score": None,
            "market_opportunities": None,
            "customer_personas": None,
            "competitive_landscape": None,
            "product_concepts": None,
            "mvp_plan": None,
            "architecture": None,
            "revenue_strategy": None,
            "risk_profile": None,
            "investment_score": None,
            "knowledge_graph": None,
            "opportunity_scores": None,
            "debate_transcript": None,
            "final_report": None,
            "agent_metadata": {},
            "awaiting_hitl": None,
            "hitl_approved": None,
            "hitl_feedback": None,
            "error": None,
        }

        total_tokens = 0
        total_cost   = 0.0
        t_start      = time.time()

        for step_output in workflow.stream(state):
            for node_name, node_state in step_output.items():
                # Write output field to DB
                field = FIELD_MAP.get(node_name)
                if field and node_state.get(field) is not None:
                    db.refresh(project)
                    setattr(project, field, node_state[field])

                # Accumulate metrics
                meta = (node_state.get("agent_metadata") or {}).get(node_name, {})
                total_tokens += meta.get("total_tokens", 0) or 0
                total_cost   += meta.get("estimated_cost_usd", 0.0) or 0.0

                progress = str(STEP_PROGRESS.get(node_name, 0))
                project.current_agent = node_name
                project.progress      = progress
                db.commit()

                # Push to Upstash Redis for SSE
                set_progress(project_id, {
                    "status":        "processing",
                    "current_agent": node_name,
                    "progress":      progress,
                })

                state.update(node_state)

        # Finalise
        db.refresh(project)
        project.status           = "completed"
        project.current_agent    = None
        project.progress         = "100"
        project.completed_at     = datetime.utcnow()
        project.total_tokens     = {"total": total_tokens}
        project.total_cost_usd   = round(total_cost, 4)
        project.total_duration_sec = round(time.time() - t_start, 2)
        db.commit()

        set_progress(project_id, {"status": "completed", "current_agent": None, "progress": "100"})

    except Exception as e:
        if project:
            try:
                db.refresh(project)
                project.status        = "failed"
                project.error_message = str(e)[:1000]
                db.commit()
            except Exception:
                pass
        set_progress(project_id, {"status": "failed", "current_agent": None, "progress": "0"})
        raise
    finally:
        db.close()
        delete_progress(project_id)
