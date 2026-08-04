from backend.diff_extractor import DiffExtractor

extractor = DiffExtractor()

data = extractor.extract_latest_commit()

print("=" * 60)
print("LATEST COMMIT")
print("=" * 60)

print("Commit ID :", data["commit_id"])
print("Author    :", data["author"])
print("Email     :", data["email"])
print("Message   :", data["message"])

print("\nChanged Files")

for file in data["files"]:
    print(" -", file)

print("\nDiff")
print("=" * 60)
print(data["diff"])