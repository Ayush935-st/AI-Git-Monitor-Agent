from backend.agents.git_monitor_agent import GitMonitorAgent
from backend.services.git_service import GitService

git_service = GitService("repositories/sample_repo")

agent = GitMonitorAgent(git_service)

agent.initialize()

result = agent.check_for_new_commit()

print(result)