from langgraph.graph import StateGraph, START, END

from backend.agents.agent_state import MultiAgentState
from backend.agents.code_analysis_agent import CodeAnalysisAgent
from backend.agents.security_agent import SecurityAgent
from backend.agents.risk_agent import RiskAgent
from backend.agents.review_agent import ReviewAgent


# =========================================================
# Agents
# =========================================================

code_agent = CodeAnalysisAgent()
security_agent = SecurityAgent()
risk_agent = RiskAgent()
review_agent = ReviewAgent()


# =========================================================
# Supervisor
# =========================================================

def supervisor_node(state: MultiAgentState):

    return {
        "current_agent": "supervisor",
        "workflow_status": "analysis_started",
    }


# =========================================================
# Code Analysis Agent
# =========================================================

def code_analysis_node(state: MultiAgentState):

    result = code_agent.analyze(state)

    return result


# =========================================================
# Security Agent
# =========================================================

def security_analysis_node(state: MultiAgentState):

    result = security_agent.analyze(state)

    return result


# =========================================================
# Analysis Merge
# =========================================================

def analysis_merge_node(state: MultiAgentState):

    return {
        "current_agent": "supervisor",
        "workflow_status": "analysis_completed",
    }


# =========================================================
# Risk Agent
# =========================================================

def risk_assessment_node(state: MultiAgentState):

    result = risk_agent.analyze(state)

    return {
        **result,
        "workflow_status": "risk_assessment_completed",
    }


# =========================================================
# Review Agent
# =========================================================

def llm_review_node(state: MultiAgentState):

    review = review_agent.review_code(
        repository=state.get("repository", ""),
        commit=state.get("commit", ""),
        changed_files=state.get("changed_files", []),
        git_diff=state.get("git_diff", ""),
        code_analysis=state.get("code_analysis", {}),
        security_analysis=state.get("security_analysis", {}),
        risk_score=state.get("risk_score", 0),
    )

    return {
        "llm_review": review,
        "current_agent": "review",
        "workflow_status": "review_completed",
    }


# =========================================================
# Final Review
# =========================================================

def final_review_node(state: MultiAgentState):

    return {
        "final_review": {
            "repository": state.get("repository"),
            "commit": state.get("commit"),
            "changed_files": state.get("changed_files"),
            "code_analysis": state.get("code_analysis"),
            "security_analysis": state.get("security_analysis"),
            "risk_score": state.get("risk_score"),
            "risk_level": state.get("risk_level"),
            "llm_review": state.get("llm_review"),
        },
        "current_agent": "supervisor",
        "workflow_status": "completed",
    }


# =========================================================
# Build Graph
# =========================================================

def build_code_review_graph():

    graph = StateGraph(MultiAgentState)

    # Register nodes
    graph.add_node("supervisor", supervisor_node)
    graph.add_node("code_analysis", code_analysis_node)
    graph.add_node("security_analysis", security_analysis_node)
    graph.add_node("analysis_merge", analysis_merge_node)
    graph.add_node("risk_assessment", risk_assessment_node)
    graph.add_node("llm_review", llm_review_node)
    graph.add_node("final_review", final_review_node)

    # -----------------------------------------------------
    # Supervisor → Parallel Analysis
    # -----------------------------------------------------

    graph.add_edge(START, "supervisor")

    graph.add_edge("supervisor", "code_analysis")
    graph.add_edge("supervisor", "security_analysis")

    # -----------------------------------------------------
    # Parallel Analysis → Merge
    # -----------------------------------------------------

    graph.add_edge("code_analysis", "analysis_merge")
    graph.add_edge("security_analysis", "analysis_merge")

    # -----------------------------------------------------
    # Risk → Review → Final
    # -----------------------------------------------------

    graph.add_edge("analysis_merge", "risk_assessment")
    graph.add_edge("risk_assessment", "llm_review")
    graph.add_edge("llm_review", "final_review")

    # -----------------------------------------------------
    # End
    # -----------------------------------------------------

    graph.add_edge("final_review", END)

    return graph.compile()


# =========================================================
# Compiled Graph
# =========================================================

code_review_graph = build_code_review_graph()