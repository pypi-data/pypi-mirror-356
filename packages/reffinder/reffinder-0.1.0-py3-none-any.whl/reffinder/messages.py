import json
import os
from typing import Optional
import uuid
from reffinder.enums import Language
from reffinder.enums import LSPMethod
from reffinder.function import FunctionLocation


class BaseMessage:
    def __init__(self, method: str, params: dict = {}, id: Optional[str]  = None):
        self.method = method
        self.params = params
        self.id = id

    @property
    def message(self):
        message = {
            "jsonrpc": "2.0",
            "method": self.method,
            "params": self.params,
        }
        # Notifications should not have an id
        if self.id is not None:
            message["id"] = self.id
        return message

    def encode(self):
        body = json.dumps(self.message)
        return f"Content-Length: {len(body)}\r\n\r\n{body}".encode("utf-8")

    def __repr__(self):
        return f"Message(id={self.id} -  method={self.method})"
    
class DidOpenMessage(BaseMessage):
    def __init__(self, file_path: str, language_id: Language = Language.PYTHON,):
        file_uri = f"file://{os.path.abspath(file_path)}"
        # Send didOpen
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

        super().__init__(method="textDocument/didOpen", params={
            "textDocument": {
                "uri": file_uri,
                "languageId": language_id,
                "version": 1,
                "text": text
            }
        })

class ReferenceMessage(BaseMessage):
    def __init__(self, floc:FunctionLocation):
        file_uri = f"file://{os.path.abspath(floc.file_path)}"
        super().__init__(
            method=LSPMethod.REFERENCES,
            params={
            "textDocument": {"uri": file_uri},
            "position": {"line": floc.start_line, "character": floc.start_col},
            "context": {"includeDeclaration": True}
            },
            id=str(uuid.uuid4())
        )

