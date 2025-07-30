from typing import Literal
from dataclasses import dataclass


@dataclass(frozen=True)
class Position:
    line: int
    column: int

    def __str__(self) -> str:
        return f"{self.line}:{self.column}"

@dataclass(frozen=True)
class Location:
    file: str
    start: Position
    end: Position

    def __str__(self) -> str:
        return f"{self.file}:{self.start}:{self.end}"

@dataclass(frozen=True)
class Entry:
    type: Literal["TODO", "FIXME"]
    text: str
    location: Location
    issue_tracker_id: str | None = None

    def format(self) -> str:
        return f"# {self.type}: {f'({self.issue_tracker_id}) ' if self.issue_tracker_id else ''}{self.text}"