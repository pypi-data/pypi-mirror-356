from enum import Enum


class Language(str, Enum):
    PYTHON = "python"

class LSPMethod(str, Enum):
    INITIALIZE = "initialize"
    INITIALIZED = "initialized"
    DID_OPEN = "textDocument/didOpen"
    REFERENCES = "textDocument/references"