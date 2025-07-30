from dataclasses import dataclass
import json

@dataclass
class Position:
    line: int
    character: int

@dataclass
class Range:
    start: Position
    end: Position


class Reference:
    uri: str
    range: Range

    def __init__(self, data: dict) -> None:
        uri = data.get("uri")
        if not uri:
            raise ValueError("Reference must have a 'uri' field.")
        self.uri = uri
        self.range = Range(
            start=Position(**data["range"]["start"]),
            end=Position(**data["range"]["end"])
        )

    def __repr__(self) -> str:
        return json.dumps({
            "uri": self.uri,
            "start_line": self.range.start.line,
            "start_character": self.range.start.character,
        })


