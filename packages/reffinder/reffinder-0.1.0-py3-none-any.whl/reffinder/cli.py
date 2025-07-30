import argparse
import asyncio
import logging
import os

from reffinder.function import FunctionLocation
from reffinder.langserver import LangServer
from reffinder.messages import DidOpenMessage
from reffinder.references import find_references
from reffinder.utils import build_graph 

async def main_async(cwd: str, file_path:str, line:int, char:int, all:bool) -> None:
    server = await LangServer.start()
    await server.initialize(cwd)

    open_message = DidOpenMessage(
        file_path=file_path
    )
    await server.send_message(open_message)


    floc = FunctionLocation(
        file_path=file_path,
        start_line=line,
        start_col=char,
    )

    find_references_task = asyncio.create_task(find_references(server, floc, all))
    all_references = await find_references_task
    build_graph(all_references)
    await server.shutdown()


def main():
    parser = argparse.ArgumentParser(description="Your CLI tool")
    parser.add_argument("file", help="The relative path of the file")
    parser.add_argument("line", type=int, help="The line number of the function (O based index)")
    parser.add_argument("char", type=int, help="The character position of the function name (O based index)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")
    parser.add_argument("--all", action="store_true", help="Find all reference in the workspace, without skipping any directories")
    
    args = parser.parse_args()
    # Set log level based on --verbose flag
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format='[%(levelname)s] %(message)s'
    )
    cwd = os.getcwd()
    asyncio.run(
        main_async(
            cwd=cwd,
            file_path=cwd+'/'+args.file,
            line=args.line,
            char=args.char,
            all=args.all
        )
    )

    