from typing import TypedDict, Optional, Dict, Any

from langgraph.graph import StateGraph, START, END

from backend.tools.code_analyzer import CodeAnalyzer
from backend.tools.security_scanner import SecurityScanner
from backend.agents.review_agent import ReviewAgent


class CodeReviewState(TypedDict, total=False):
    repository: str
    commit: str
    changed_files: list[str]
    git_diff: str

    code_analysis: Dict[str, Any]
    security_analysis: Dict[str, Any]
    risk_score: int

    llm_review: Optional[str]
    final_review: Optional[Dict[str, Any]]


# ---------------------------------
# Analysis tools
# ---------------------------------

code_analyzer = CodeAnalyzer()
security_scanner = SecurityScanner()
review_agent = ReviewAgent()


# ---------------------------------
# Node 1: Git Analysis
# ---------------------------------

def git_analysis_node(state: CodeReviewState):

    changed_files = state.get("changed_files", [])
    git_diff = state.get("git_diff", "")

    return {
        "code_analysis": {
            "changed_file_count": len(changed_files),
            "changed_files": changed_files,
            "diff_size": len(git_diff),
        }
    }


# ---------------------------------
# Node 2: Code-Based Analysis
# ---------------------------------

def code_analysis_node(state: CodeReviewState):

    changed_files = state.get("changed_files", [])
    git_diff = state.get("git_diff", "")

    analysis = code_analyzer.analyze(
        changed_files=changed_files,
        git_diff=git_diff,
    )

    return {
        "code_analysis": {
            **state.get("code_analysis", {}),
            **analysis,
            "status": "completed",
        }
    }


# ---------------------------------
# Node 3: Security Analysis
# ---------------------------------

def security_analysis_node(state: CodeReviewState):

    git_diff = state.get("git_diff", "")

    analysis = security_scanner.scan(git_diff)

    return {
        "security_analysis": {
            **analysis,
            "status": "completed",
        }
    }


# ---------------------------------
# Node 4: Risk Assessment
# ---------------------------------

def risk_assessment_node(state: CodeReviewState):

    code_analysis = state.get("code_analysis", {})
    security_analysis = state.get("security_analysis", {})

    risk_score = 0

    for finding in code_analysis.get("findings", []):

        severity = finding.get("severity", "").lower()

        if severity == "high":
            risk_score += 5

        elif severity == "medium":
            risk_score += 2

        elif severity == "low":
            risk_score += 1

    for finding in security_analysis.get("findings", []):

        severity = finding.get("severity", "").lower()

        if severity == "high":
            risk_score += 5

        elif severity == "medium":
            risk_score += 2

        elif severity == "low":
            risk_score += 1

    risk_score = min(risk_score, 10)

    if risk_score >= 7:
        risk_level = "HIGH"

    elif risk_score >= 4:
        risk_level = "MEDIUM"

    else:
        risk_level = "LOW"

    return {
        "risk_score": risk_score,

        "code_analysis": {
            **code_analysis,
            "risk_level": risk_level,
        },
    }


# ---------------------------------
# Node 5: LLM Engineering Review
# ---------------------------------

def llm_review_node(state: CodeReviewState):

    repository = state.get("repository", "")
    commit = state.get("commit", "")
    changed_files = state.get("changed_files", [])
    git_diff = state.get("git_diff", "")

    code_analysis = state.get("code_analysis", {})
    security_analysis = state.get("security_analysis", {})
    risk_score = state.get("risk_score", 0)

    review = review_agent.review_code(
        repository=repository,
        commit=commit,
        changed_files=changed_files,
        git_diff=git_diff,
        code_analysis=code_analysis,
        security_analysis=security_analysis,
        risk_score=risk_score,
    )

    return {
        "llm_review": review
    }


# ---------------------------------
# Node 6: Final Review
# ---------------------------------

def final_review_node(state: CodeReviewState):

    return {
        "final_review": {
            "repository": state.get("repository"),
            "commit": state.get("commit"),
            "changed_files": state.get("changed_files"),
            "code_analysis": state.get("code_analysis"),
            "security_analysis": state.get("security_analysis"),
            "risk_score": state.get("risk_score"),
            "llm_review": state.get("llm_review"),
        }
    }


# ---------------------------------
# Build LangGraph
# ---------------------------------

def build_code_review_graph():

    graph = StateGraph(CodeReviewState)

    graph.add_node("git_analysis", git_analysis_node)
    graph.add_node("code_analysis", code_analysis_node)
    graph.add_node("security_analysis", security_analysis_node)
    graph.add_node("risk_assessment", risk_assessment_node)
    graph.add_node("llm_review", llm_review_node)
    graph.add_node("final_review", final_review_node)

    graph.add_edge(START, "git_analysis")
    graph.add_edge("git_analysis", "code_analysis")
    graph.add_edge("code_analysis", "security_analysis")
    graph.add_edge("security_analysis", "risk_assessment")
    graph.add_edge("risk_assessment", "llm_review")
    graph.add_edge("llm_review", "final_review")
    graph.add_edge("final_review", END)

    return graph.compile()


code_review_graph = build_code_review_graph()