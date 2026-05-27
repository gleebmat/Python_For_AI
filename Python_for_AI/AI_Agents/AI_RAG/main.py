import re
from pathlib import Path

NOTES_DIR = (
    Path(__file__).parent / "notes"
).resolve()  # we go from this exact file to the upper directory and then to notes and then check whether everything is good
type(NOTES_DIR)
NOTES_DIR
print("\n1. Start from the notes directory:")
print(NOTES_DIR)

print("\n2. Find markdown files:")
paths = sorted(NOTES_DIR.glob("*.md"))
print(paths[:3])


print("Return paths relative to notes/:")
relative_paths = [str(path.relative_to(NOTES_DIR)) for path in paths]
print(relative_paths)


def list_files(pattern: str = "*.md") -> list[str]:
    return sorted(str(path.relative_to(NOTES_DIR)) for path in NOTES_DIR.glob(pattern))


print("\nlist_files():")
print(list_files())


print("\n1. Compile a case-insensitive regex:")
pattern = "connection pool"
rx = re.compile(pattern, re.IGNORECASE)
print(rx)
r = rx.search("Connection pool")
if r:
    print("Found!")
r = rx.search("Tottenham")
if not r:
    print("Not found")

print("2. Search one file line by line:")
file = NOTES_DIR / "02-billing-runbook.md"
text = file.read_text()
lines = text.splitlines()
one_file_hits = []

for i, line in enumerate(lines, start=1):
    if rx.search(line):
        rel = file.relative_to(NOTES_DIR)
        one_file_hits.append(f"{rel}:{i}: {line.strip()}")

print(one_file_hits)

print("\n3. Search every markdown file:")
all_files = sorted(NOTES_DIR.rglob("*.md"))


def grep(pattern: str, max_results: int = 30) -> list[str]:
    rx = re.compile(pattern, re.IGNORECASE)
    hits: list[str] = []
    for file in sorted(NOTES_DIR.rglob("*.md")):
        for i, line in enumerate(file.read_text().splitlines(), start=1):
            if rx.search(line):
                rel = file.relative_to(NOTES_DIR)
                hits.append(f"{rel}:{i}: {line.strip()}")
                if len(hits) >= max_results:
                    return hits

    return hits


print("\ngrep('connection pool'):")
print(grep("connection pool"))

print("\n1. Resolve the requested path:")
requested = "04-architecture-decisions.md"
target = (NOTES_DIR / requested).resolve()
print(target)

print("\n2. Check that it stayed inside notes:/:")
print(target.is_relative_to(NOTES_DIR))  # check if target is really into NOTES_DIR

print("\n3. Read the text:")
print(target.read_text()[:200])


def read_file(path: str) -> str:
    target = (NOTES_DIR / path).resolve()
    if not target.is_relative_to(NOTES_DIR):
        raise ValueError("Path {path is outside of the notes directory}")
    return target.read_text()


print("\nread_file('04-architecture-decisions.md')[:200]:")
print(read_file("04-architecture-decisions.md")[:200])
