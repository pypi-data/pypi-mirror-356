from functools import lru_cache
import os
from pathlib import Path
from subprocess import Popen, PIPE, DEVNULL

from fixmefinder.entry import Entry

@lru_cache(maxsize=1)
def get_repo_url() -> str:
    """
    Get the URL of the repository from the origin remote.
    """
    process = Popen(["git", "remote", "get-url", "origin"], stdout=PIPE, stderr=DEVNULL)
    stdout, _ = process.communicate()
    name = stdout.decode("utf-8").strip()
    name = name if name != "" else "Unknown"
    return name

def make_title(entry: Entry) -> str:
    """
    Generate a title for the issue based on the entry type and text.
    """

    if entry.type == "FIXME":
        return f"[BUG] {entry.text}"
    
    if entry.type == "TODO":
        return f"[TODO] {entry.text}"

    raise ValueError(f"Unknown entry type: {entry.type}")

def make_issue(entry: Entry):
    title = make_title(entry)

    path = Path(entry.location.file)
    path = path.relative_to(os.getcwd())

    file = f"File: {path}:{entry.location.start.line}:{entry.location.start.column}"
    repo = get_repo_url()

    body = f"File: {file}\nRepo: {repo}\n\n{entry.text}"

    return (title, body)
