from backend.agents.report_agent import ReportAgent

review = """
Overall Score : 9/10

Security:
No issues found.

Performance:
Good.

Recommendation:
Add more unit tests.
"""

agent = ReportAgent()

md = agent.generate_markdown(review, "abc123")

pdf = agent.generate_pdf(review, "abc123")

print(md)
print(pdf)