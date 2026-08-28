from typing import TypedDict, Optional, Dict, Any


class MultiAgentState(TypedDict, total=False):
    """
    Shared state passed between all agents in the
    multi-agent code review workflow.
    """

    # Repository information
    repository: str
    commit: str
    changed_files: list[str]
    git_diff: str

    # Analysis results
    code_analysis: Dict[str, Any]
    security_analysis: Dict[str, Any]
    findings: list[Dict[str, Any]]

    # Risk assessment
    risk_score: int
    risk_level: str

    # AI review
    llm_review: Optional[str]

    # Final result
    final_review: Optional[Dict[str, Any]]

    # Workflow information
    current_agent: str
    workflow_status: str