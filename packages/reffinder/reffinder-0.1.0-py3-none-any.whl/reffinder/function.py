import ast
from dataclasses import dataclass
from typing import Optional



class FunctionLocation:
    file_path: str
    start_line: int
    start_col: int
    function_name: Optional[str] = None
    definition_line: Optional[str] = None
    end_line: Optional[int] = None
    end_col: Optional[int] = None
    referencing_function: Optional["FunctionLocation"] = None

    def __init__(self, **kwargs) -> None:
        self.file_path = kwargs["file_path"]
        self.start_line = kwargs["start_line"]
        self.start_col = kwargs["start_col"]
        self.definition_line = kwargs.get("definition_line")
        self.end_line = kwargs.get("end_line")
        self.end_col = kwargs.get("end_col")
        self.referencing_function = kwargs.get("referencing_function")
        self.function_name = kwargs.get("function_name")

        if not kwargs.get("function_name"):
            self.function_name = self.get_function_name_from_position(
                file_path=kwargs["file_path"],
                line=kwargs["start_line"],
                character=kwargs["start_col"],
            )
        self.id = (self.file_path, self.start_line, self.function_name,)
        
    @staticmethod
    def get_function_name_from_position(file_path: str, line: int, character: int) -> Optional[str]:
        """
        Returns the name of the function defined at the given line and character in the file.

        Args:
            file_path (str): Path to the Python file.
            line (int): Line number (0-indexed).
            character (int): Character position in the line (0-indexed).

        Returns:
            str | None: The name of the function if found, otherwise None.
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            source = f.read()

        tree = ast.parse(source, filename=file_path)

        class FunctionFinder(ast.NodeVisitor):
            def __init__(self):
                self.result = None

            def visit_FunctionDef(self, node):
                if hasattr(node, 'lineno') and hasattr(node, 'col_offset'):
                    if node.lineno == line+1 and node.col_offset <= character < node.col_offset + len(node.name):
                        self.result = node.name
                self.generic_visit(node)

            def visit_AsyncFunctionDef(self, node):
                self.visit_FunctionDef(node)  # Same logic for async functions

        finder = FunctionFinder()
        finder.visit(tree)
        fn_name = finder.result
        return fn_name
