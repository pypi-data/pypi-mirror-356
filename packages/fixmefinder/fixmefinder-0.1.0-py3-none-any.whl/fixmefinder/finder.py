import re
from pathlib import Path
from typing import Literal, cast

import pathspec

from fixmefinder.entry import Entry, Location, Position

ENCODING = "utf-8"
COMMENT_PATTERN = re.compile(r"^\s*#\s*(TODO|FIXME):(?:\s*\(([^)]+)\))?\s*(.*)")


def parse_line(filename: Path, line_number: int, line: str) -> Entry | None:
    match = COMMENT_PATTERN.match(line)
    if not match:
        return None

    comment_type_str, issue_id, text = match.groups()

    # Safe cast due to regex constraint
    comment_type = cast(Literal["TODO", "FIXME"], comment_type_str)

    start_col = line.index('#')  # position of `#` in the line
    end_col = len(line)

    location = Location(
        file=str(filename),
        start=Position(line=line_number, column=start_col + 1),
        end=Position(line=line_number, column=end_col)
    )

    return Entry(
        type=comment_type,
        text=text.strip(),
        location=location,
        issue_tracker_id=issue_id.strip() if issue_id else None
    )

def load_gitignore(base_dir: Path) -> pathspec.PathSpec:
    gitignore_path = base_dir / ".gitignore"
    if not gitignore_path.exists():
        return pathspec.PathSpec.from_lines("gitwildmatch", [])

    with open(gitignore_path, "r", encoding="utf-8") as f:
        return pathspec.PathSpec.from_lines("gitwildmatch", f)


# TODO: make this async?
def find_fixme_comments(directory: Path) -> set[Entry]:
    entries: set[Entry] = set()
    spec = load_gitignore(directory)

    for file_path in directory.rglob("*.py"):
        relative_path = file_path.relative_to(directory)
        if spec.match_file(str(relative_path)):
            continue  # ignored by .gitignore

        try:
            with open(file_path, "r", encoding=ENCODING) as file:
                for line_number, line in enumerate(file, start=1):
                    entry = parse_line(file_path, line_number, line)
                    if entry:
                        entries.add(entry)
        except (UnicodeDecodeError, OSError):
            continue  # skip unreadable files

    return entries