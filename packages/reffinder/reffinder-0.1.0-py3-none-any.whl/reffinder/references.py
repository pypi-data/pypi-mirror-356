# import logging
# from reffinder.function import FunctionLocation
# from reffinder.langserver import LangServer
# from reffinder.messages import ReferenceMessage
# from reffinder.utils import get_enclosing_function, parse_reference_response, uri_to_file_path

# logger = logging.getLogger(__name__)

# # TODO Refactor this!!
# async def find_references(server: LangServer, floc: FunctionLocation) -> list[FunctionLocation]:
#     all_references = [floc]
#     all_reference_ids = [floc.id]
#     unvisited_functions = [floc]

#     while unvisited_functions:
#         func = unvisited_functions.pop()        

#         logger.info(f"Visiting function: {func.id}")
#         reference_message = ReferenceMessage(func)
#         reference_response = await server.send_message(reference_message, read_response=True)
#         if not reference_response:
#             # TODO raise here
#             logger.error("No response received from the server.")
#             continue
#         refs = parse_reference_response(reference_response)
#         for ref in refs:
#             # logger.info(f'Found reference: {ref}')
#             ref_loc = get_enclosing_function(uri_to_file_path(ref.uri), ref.range.start.line)
#             if not ref_loc:
#                 # TODO find all the edge cases, treat them properly and raise if not case is handled
#                 logger.warning(f"No enclosing function found for reference: {ref.uri} at line {ref.range.start.line}")
#                 continue
#             refloc = FunctionLocation(
#                 referencing_function=func,
#                 file_path=ref_loc.file_path,
#                 start_line=ref_loc.start_line,  # Convert to 0-based index
#                 start_col=4, # Assuming start_col is always 4 for simplicity  
#                 function_name=ref_loc.function_name
#             )
#             if refloc.id not in all_reference_ids and '/tests/' not in refloc.file_path: # TODO Handle better and dynamically
#                 logger.info(f'Added unvisited function: {refloc.id}')
#                 unvisited_functions.append(refloc)
#                 all_references.append(refloc)
#                 all_reference_ids.append(refloc.id)
#     return all_references

import logging
from typing import List

from reffinder.function import FunctionLocation
from reffinder.langserver import LangServer
from reffinder.messages import ReferenceMessage
from reffinder.utils import (
    get_enclosing_function,
    parse_reference_response,
    uri_to_file_path,
)

logger = logging.getLogger(__name__)

# Constants
DEFAULT_START_COL = 4  # Placeholder default, should ideally be inferred
EXCLUDE_PATH_PATTERNS = ['/tests/']  # TODO: Make this configurable


async def find_references(server: LangServer, root_function: FunctionLocation, all:bool) -> List[FunctionLocation]:
    """
    Recursively find all functions that reference the given root_function using a language server.

    Args:
        server (LangServer): The language server instance.
        root_function (FunctionLocation): The starting function location.
        all (bool): If True, will not skip any directories based on exclude patterns.

    Returns:
        List[FunctionLocation]: A list of all referencing FunctionLocations found, including the root.
    """
    all_references = [root_function]
    visited_ids = {root_function.id}
    queue = [root_function]

    while queue:
        current_func = queue.pop()
        logger.debug(f"Fetching references for function: {current_func.id}")

        try:
            reference_response = await _fetch_reference(server, current_func)
        except ValueError as e:
            logger.error(f"Failed to get references for {current_func.id}: {e}")
            continue

        for ref in parse_reference_response(reference_response):
            ref_loc = get_enclosing_function(uri_to_file_path(ref.uri), ref.range.start.line)
            if not ref_loc:
                # TODO find all the edge cases, treat them properly and raise if not case is handled
                logger.warning(
                    f"No enclosing function found for reference: {ref.uri}, line {ref.range.start.line}"
                )
                continue

            new_function = FunctionLocation(
                referencing_function=current_func,
                file_path=ref_loc.file_path,
                start_line=ref_loc.start_line,
                start_col=DEFAULT_START_COL,  # TODO: Derive actual column if possible
                function_name=ref_loc.function_name,
            )

            if new_function.id in visited_ids:
                continue

            if _is_excluded_path(new_function.file_path, all):
                logger.debug(f"Excluded reference in path: {new_function.file_path}")
                continue

            logger.info(f"Discovered new reference: {new_function.id}")
            queue.append(new_function)
            all_references.append(new_function)
            visited_ids.add(new_function.id)

    return all_references


async def _fetch_reference(server: LangServer, func: FunctionLocation):
    """
    Sends a reference message to the language server and ensures a response is received.

    Raises:
        ValueError: If no response is received.
    """
    message = ReferenceMessage(func)
    response = await server.send_message(message, read_response=True)

    if not response:
        raise ValueError("No response received from language server.")

    return response


def _is_excluded_path(path: str, all:bool) -> bool:
    """Check if the path matches any of the exclude patterns."""
    if all:
        return False 
    return any(pattern in path for pattern in EXCLUDE_PATH_PATTERNS)
