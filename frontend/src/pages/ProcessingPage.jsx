import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { CheckCircle, Circle, Loader2, XCircle, Zap } from "lucide-react";
import { projectsApi } from "../api/client";

const STAGES = [
  { key: "Research Analyst",                         desc: "Extracting problem, novelty & methodology" },
  { key: "Technical Validator + Market Discovery",   desc: "Running in parallel — innovation score + market sizing" },
  { key: "Personas + Competitors + Knowledge Graph", desc: "Running in parallel — 3 agents simultaneously" },
  { key: "Product Strategy + Risk + Investment",     desc: "Running in parallel — 3 agents simultaneously" },
  { key: "MVP + Architecture + Revenue",             desc: "Running in parallel — 3 agents simultaneously" },
  { key: "Opportunity Scorer",                       desc: "Multi-dimensional scoring framework" },
  { key: "Agent Debate",                             desc: "4 agents argue FOR / AGAINST / CHALLENGE / SKEPTICAL" },
  { key: "Judge Agent",                              desc: "Resolving conflicts & final verdict" },
];

export default function ProcessingPage() {
  const { projectId } = useParams();
  const navigate = useNavigate();
  const [status, setStatus] = useState({ status: "processing", current_agent: null, progress: "0" });

  useEffect(() => {
    const base = process.env.REACT_APP_API_URL || "http://localhost:8000";
    const token = localStorage.getItem("token");

    const es = new EventSource(`${base}/api/projects/${projectId}/stream?token=${token}`);
    es.onmessage = (e) => {
      const d = JSON.parse(e.data);
      setStatus(d);
      if (d.status === "completed") {
        es.close();
        setTimeout(() => navigate(`/projects/${projectId}/report`), 600);
      }
      if (d.status === "failed") es.close();
    };
    es.onerror = () => es.close();

    const poll = setInterval(async () => {
      try {
        const r = await projectsApi.status(projectId);
        setStatus(r.data);
        if (r.data.status === "completed") {
          clearInterval(poll);
          setTimeout(() => navigate(`/projects/${projectId}/report`), 600);
        }
        if (r.data.status === "failed") clearInterval(poll);
      } catch {}
    }, 4000);

    return () => { es.close(); clearInterval(poll); };
  }, [projectId, navigate]);

  const progress = parseInt(status.progress || "0");
  const currentLabel = status.current_agent || "";

  // Find which stage index is active
  const activeIdx = STAGES.findIndex(s => currentLabel.includes(s.key.split(" ")[0]));

  return (
    <div className="max-w-lg mx-auto px-4 py-12">
      <div className="text-center mb-8">
        <div className="inline-flex items-center gap-2 mb-3 bg-brand-500/10 border border-brand-500/20 rounded-full px-4 py-1.5">
          <Zap size={13} className="text-brand-400" />
          <span className="text-xs text-brand-300 font-medium">Parallel pipeline — 8 stages</span>
        </div>
        <h1 className="text-xl font-bold text-white mb-1">Analysing your research</h1>
        <p className="text-gray-400 text-sm">15 agents running across 8 parallel stages</p>
      </div>

      <div className="bg-gray-800 rounded-full h-1.5 mb-2 overflow-hidden">
        <div className="bg-brand-500 h-1.5 rounded-full transition-all duration-700" style={{ width: `${progress}%` }} />
      </div>
      <p className="text-center text-xs text-gray-500 mb-6">{progress}% complete</p>

      <div className="space-y-2">
        {STAGES.map((stage, i) => {
          // Determine state of each stage based on progress
          const stageProgress = [7, 21, 35, 56, 70, 82, 93, 100][i];
          const prevProgress  = [0, 7,  21, 35, 56, 70, 82, 93][i];
          const done   = progress >= stageProgress;
          const active = progress > prevProgress && progress < stageProgress ||
                         (currentLabel && currentLabel.includes(stage.key.split(" ")[0]));
          const failed = status.status === "failed" && active;
          const isParallel = stage.key.includes("+");

          return (
            <div key={stage.key}
              className={`flex items-start gap-3 p-3 rounded-lg transition-all ${
                active ? "bg-brand-500/10 border border-brand-500/20" : "bg-gray-900/50"
              }`}>
              <div className="mt-0.5 flex-shrink-0">
                {failed  ? <XCircle size={16} className="text-red-400" />
                : done   ? <CheckCircle size={16} className="text-green-400" />
                : active ? <Loader2 size={16} className="text-brand-400 animate-spin" />
                :           <Circle size={16} className="text-gray-700" />}
              </div>
              <div className="flex-1">
                <div className="flex items-center gap-2">
                  <p className={`text-sm font-medium ${active ? "text-white" : done ? "text-gray-300" : "text-gray-600"}`}>
                    {stage.key}
                  </p>
                  {isParallel && (
                    <span className="text-xs bg-teal-500/10 text-teal-400 border border-teal-500/20 rounded-full px-1.5 py-0.5 font-medium">
                      parallel
                    </span>
                  )}
                </div>
                {active && <p className="text-xs text-gray-400 mt-0.5">{stage.desc}</p>}
              </div>
            </div>
          );
        })}
      </div>

      {status.status === "failed" && (
        <div className="mt-6 p-4 bg-red-500/10 border border-red-500/20 rounded-xl text-red-300 text-sm">
          Analysis failed. Check your API keys and try again.
        </div>
      )}
    </div>
  );
}