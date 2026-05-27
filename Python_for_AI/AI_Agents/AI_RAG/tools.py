import re
from pathlib import Path

NOTES_DIR = (Path(__file__).parent / "notes").resolve()
NOTES_DIR


def list_files(pattern: str = "*.md") -> list[str]:
    return sorted(str(path.relative_to(NOTES_DIR)) for path in NOTES_DIR.glob(pattern))


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


def read_file(path: str) -> str:
    target = (NOTES_DIR / path).resolve()
    if not target.is_relative_to(NOTES_DIR):
        raise ValueError("Path {path is outside of the notes directory}")
    return target.read_text()
