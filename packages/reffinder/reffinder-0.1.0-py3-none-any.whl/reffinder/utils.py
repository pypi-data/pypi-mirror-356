import logging
import ast
from pathlib import Path
from typing import Optional
from urllib.parse import unquote, urlparse

from graphviz import Digraph # type: ignore [import-untyped] 

from reffinder.function import FunctionLocation
from reffinder.response import Reference
logger = logging.getLogger(__name__)

def parse_reference_response(response: dict) -> list[Reference]:
    """
    Parses the response from the language server and returns a list of Reference objects.
    Args:
        response (object): The response from the language server, expected to be a dictionary.
    Returns:
        list[Reference]: A list of Reference objects parsed from the response.
    Raises:
        ValueError: If the response is not a dictionary or does not contain the expected structure.
    """
    if not isinstance(response, dict):
        raise ValueError("Response must be a dictionary.")

    result = response.get("result", [])
    references: list[Reference] = []
    if not result :
        logger.warning("No references found in the response.")
        return references
    for item in result:
        ref = Reference(item)
        references.append(ref)

    return references

import ast



def get_enclosing_function(file_path:str, line:int) -> Optional[FunctionLocation]:
    """ Returns the function enclosing the given line in the specified file.
    Args:
        file_path (str): Path to the Python file.
        line (int): Line number (0-indexed).
    Returns:
        Optional[FunctionLocation]: The enclosing function location if found, otherwise None.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        source = ''.join(lines)
    
    tree = ast.parse(source, filename=file_path)
    result = None

    class FunctionFinder(ast.NodeVisitor):
        def visit_FunctionDef(self, node):
            nonlocal result
            if hasattr(node, 'body'):
                start = node.lineno
                end = max(
                    [getattr(n, 'end_lineno', getattr(n, 'lineno', start)) for n in ast.walk(node)],
                    default=start
                )
                if start <= line + 1 <= end:
                    result = FunctionLocation(
                        file_path=file_path,
                        function_name=node.name,
                        start_line=node.lineno - 1,  # Convert to 0-based index
                        end_line=getattr(node, 'end_lineno', None),
                        start_col=node.col_offset,
                        end_col=getattr(node, 'end_col_offset', None),
                        definition_line=lines[node.lineno - 1].rstrip('\n')  # Add this line
                    )

            self.generic_visit(node)

    FunctionFinder().visit(tree)
    return result

def uri_to_file_path(uri: str) -> str:
    """ Converts a URI to a file path.
    Args:
        uri (str): The URI to convert.
    Returns:
        str: The file path extracted from the URI.
    """
    parsed = urlparse(uri)
    if parsed.scheme == "file":
        return unquote(parsed.path)
    return uri

def build_graph(all_references: list[FunctionLocation]) -> None:
    """ Builds a directed graph of function references and saves it as an SVG file.
    Args:
        all_references (list[FunctionLocation]): A list of FunctionLocation objects representing all references.
    """
    dot = Digraph(comment="Function Reference Tree", format='svg')
    node_ids = {}

    # Create unique node ids and labels
    for idx, ref in enumerate(all_references):
        label = f"{ref.function_name}\n{Path(ref.file_path)}:{ref.start_line+1}"
        node_id = f"node{idx}"
        node_ids[(ref.file_path, ref.start_line, ref.function_name)] = node_id
        url = f"vscode://file/{ref.file_path}:{ref.start_line+1}"
        dot.node(node_id, label, URL=url, target="_blank")


    # Add edges: referencing_function -> function
    for idx, ref in enumerate(all_references):
        if ref.referencing_function:
            parent_key = (
                ref.referencing_function.file_path,
                ref.referencing_function.start_line,
                ref.referencing_function.function_name,
            )
            child_key = (ref.file_path, ref.start_line, ref.function_name)
            if parent_key in node_ids and child_key in node_ids:
                dot.edge(node_ids[parent_key], node_ids[child_key])

    # Render to file and open it
    dot.render('function_reference_tree', view=True)