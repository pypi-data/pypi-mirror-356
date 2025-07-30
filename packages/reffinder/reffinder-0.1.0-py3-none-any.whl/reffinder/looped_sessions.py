import logging
import ast
import os
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm

logger = logging.getLogger(__name__)

class SessionInForVisitor(ast.NodeVisitor):
    """
    AST Visitor to find instances of `db.managed_session()` inside `for` loops.
    """
    def __init__(self):
        self.violations = []

    def visit_For(self, node):
        for subnode in ast.walk(node):
            if isinstance(subnode, ast.With):
                for item in subnode.items:
                    ctx_expr = item.context_expr
                    if isinstance(ctx_expr, ast.Call):
                        func = ctx_expr.func
                        if isinstance(func, ast.Attribute) and func.attr == 'managed_session':
                            if isinstance(func.value, ast.Name) and func.value.id == 'db':
                                self.violations.append((node.lineno, node.col_offset))
        self.generic_visit(node)

def analyze_file(filepath):
    """
    Analyze a single Python file for violations of using `db.managed_session()` inside `for` loops.
    Args:
        filepath (str): Path to the Python file to analyze.
    Returns:
        tuple: (filepath, violations) if violations found, otherwise None.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        tree = ast.parse(content, filename=filepath)
        visitor = SessionInForVisitor()
        visitor.visit(tree)
        if visitor.violations:
            return filepath, visitor.violations
    except (SyntaxError, UnicodeDecodeError):
        return None
    return None


def get_python_files(directory):
    """
    Generator to yield all Python files in the given directory and its subdirectories.
    Args:
        directory (str): Path to the directory to search for Python files.
    Yields:
        str: Path to each Python file found.
    """
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                yield os.path.join(root, file)

def write_results_to_md(results, output_path="violations.md"):
    """
    Write the results of the analysis to a Markdown file.
    Args:
        results (list): List of tuples containing file paths and violations.
        output_path (str): Path to the output Markdown file.
    """
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# Violations: `db.managed_session()` inside `for` loops\n\n")
        for filepath, violations in results:
            f.write(f"## {filepath}\n")
            for lineno, col in violations:
                f.write(f"- `with db.managed_session()` inside `for` @ file://{filepath}#{lineno} \n")
            f.write("\n")
    logger.info(f"✅ Results written to `{output_path}`")

# ========================================
# Main Entry Point
# ========================================
if __name__ == "__main__":
    import sys
    import logging
    logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
    logger = logging.getLogger(__name__)
    if len(sys.argv) < 2:
        logger.error("Usage: python looped_sessions.py /path/to/codebase")
        sys.exit(1)

    base_dir = sys.argv[1]
    python_files = list(get_python_files(base_dir))

    logger.info(f"🔍 Scanning {len(python_files)} Python files...\n")

    results = []
    total_violations = 0
    with ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:

        futures = {executor.submit(analyze_file, path): path for path in python_files}
        for future in tqdm(as_completed(futures), total=len(futures), desc="Scanning"):
            result = future.result()
            total_violations += len(result[1]) if result else 0
            if result:
                results.append(result)
    logger.info(f"🔍 Found {total_violations} violations")
    write_results_to_md(results)
