from backend.diff_extractor import DiffExtractor
from backend.ai_analyzer import AIAnalyzer

extractor = DiffExtractor()

commit = extractor.extract_latest_commit()

reviewer = AIAnalyzer()

result = reviewer.analyze(commit["diff"])

print("=" * 60)

print(result)