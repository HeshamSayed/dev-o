"""
Code analysis and manipulation tools for agents.

Provides tools for parsing, analyzing, searching, and understanding code.
"""
import ast
import re
import subprocess
from typing import Dict, Any, List, Optional
from pathlib import Path

from .base import BaseTool, ToolResult


class SearchCodebaseTool(BaseTool):
    """Search codebase for patterns or text."""

    name = "search_codebase"
    description = "Search the codebase for text patterns, function definitions, class definitions, or imports"

    parameters_schema = {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Search query (text, regex, or code pattern)"
            },
            "search_type": {
                "type": "string",
                "enum": ["text", "function", "class", "import", "regex"],
                "description": "Type of search to perform",
                "default": "text"
            },
            "file_pattern": {
                "type": "string",
                "description": "File pattern to search (e.g., '*.py', '**/*.js')",
                "default": "**/*.py"
            },
            "max_results": {
                "type": "integer",
                "description": "Maximum number of results to return",
                "default": 50
            }
        },
        "required": ["query"]
    }

    async def execute(self, arguments: Dict[str, Any]) -> ToolResult:
        """Execute codebase search."""
        query = arguments.get("query", "")
        search_type = arguments.get("search_type", "text")
        file_pattern = arguments.get("file_pattern", "**/*.py")
        max_results = arguments.get("max_results", 50)

        try:
            project_path = self.agent.project.local_path
            if not project_path or not Path(project_path).exists():
                return ToolResult(
                    success=False,
                    error="Project path not set or does not exist"
                )

            results = []

            if search_type == "text":
                results = self._search_text(project_path, query, file_pattern, max_results)
            elif search_type == "regex":
                results = self._search_regex(project_path, query, file_pattern, max_results)
            elif search_type == "function":
                results = self._search_function(project_path, query, file_pattern, max_results)
            elif search_type == "class":
                results = self._search_class(project_path, query, file_pattern, max_results)
            elif search_type == "import":
                results = self._search_import(project_path, query, file_pattern, max_results)

            return ToolResult(
                success=True,
                result={
                    "query": query,
                    "search_type": search_type,
                    "results_count": len(results),
                    "results": results
                }
            )

        except Exception as e:
            return ToolResult(
                success=False,
                error=f"Search failed: {str(e)}"
            )

    def _search_text(self, project_path: str, query: str, pattern: str, max_results: int) -> List[Dict]:
        """Search for text in files."""
        results = []
        project_dir = Path(project_path)

        for file_path in project_dir.glob(pattern):
            if not file_path.is_file():
                continue

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line_num, line in enumerate(f, 1):
                        if query.lower() in line.lower():
                            results.append({
                                "file": str(file_path.relative_to(project_dir)),
                                "line": line_num,
                                "content": line.strip()
                            })
                            if len(results) >= max_results:
                                return results
            except:
                continue

        return results

    def _search_regex(self, project_path: str, pattern: str, file_pattern: str, max_results: int) -> List[Dict]:
        """Search using regex pattern."""
        results = []
        project_dir = Path(project_path)
        regex = re.compile(pattern, re.IGNORECASE)

        for file_path in project_dir.glob(file_pattern):
            if not file_path.is_file():
                continue

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line_num, line in enumerate(f, 1):
                        if regex.search(line):
                            results.append({
                                "file": str(file_path.relative_to(project_dir)),
                                "line": line_num,
                                "content": line.strip()
                            })
                            if len(results) >= max_results:
                                return results
            except:
                continue

        return results

    def _search_function(self, project_path: str, name: str, pattern: str, max_results: int) -> List[Dict]:
        """Search for function definitions."""
        results = []
        project_dir = Path(project_path)

        for file_path in project_dir.glob(pattern):
            if not file_path.is_file() or not str(file_path).endswith('.py'):
                continue

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    tree = ast.parse(content)

                    for node in ast.walk(tree):
                        if isinstance(node, ast.FunctionDef):
                            if name.lower() in node.name.lower():
                                results.append({
                                    "file": str(file_path.relative_to(project_dir)),
                                    "line": node.lineno,
                                    "name": node.name,
                                    "type": "function"
                                })
                                if len(results) >= max_results:
                                    return results
            except:
                continue

        return results

    def _search_class(self, project_path: str, name: str, pattern: str, max_results: int) -> List[Dict]:
        """Search for class definitions."""
        results = []
        project_dir = Path(project_path)

        for file_path in project_dir.glob(pattern):
            if not file_path.is_file() or not str(file_path).endswith('.py'):
                continue

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    tree = ast.parse(content)

                    for node in ast.walk(tree):
                        if isinstance(node, ast.ClassDef):
                            if name.lower() in node.name.lower():
                                results.append({
                                    "file": str(file_path.relative_to(project_dir)),
                                    "line": node.lineno,
                                    "name": node.name,
                                    "type": "class"
                                })
                                if len(results) >= max_results:
                                    return results
            except:
                continue

        return results

    def _search_import(self, project_path: str, module: str, pattern: str, max_results: int) -> List[Dict]:
        """Search for import statements."""
        results = []
        project_dir = Path(project_path)

        for file_path in project_dir.glob(pattern):
            if not file_path.is_file():
                continue

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line_num, line in enumerate(f, 1):
                        if line.strip().startswith(('import ', 'from ')) and module in line:
                            results.append({
                                "file": str(file_path.relative_to(project_dir)),
                                "line": line_num,
                                "content": line.strip()
                            })
                            if len(results) >= max_results:
                                return results
            except:
                continue

        return results


class AnalyzeCodeTool(BaseTool):
    """Analyze code structure and extract metadata."""

    name = "analyze_code"
    description = "Analyze a Python file to extract classes, functions, imports, and dependencies"

    parameters_schema = {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "Path to the file to analyze (relative to project root)"
            }
        },
        "required": ["file_path"]
    }

    async def execute(self, arguments: Dict[str, Any]) -> ToolResult:
        """Execute code analysis."""
        file_path = arguments.get("file_path", "")

        try:
            project_path = self.agent.project.local_path
            if not project_path:
                return ToolResult(
                    success=False,
                    error="Project path not set"
                )

            full_path = Path(project_path) / file_path

            if not full_path.exists():
                return ToolResult(
                    success=False,
                    error=f"File not found: {file_path}"
                )

            # Read file
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Parse Python code
            try:
                tree = ast.parse(content)
                analysis = self._analyze_ast(tree)
            except SyntaxError as e:
                return ToolResult(
                    success=False,
                    error=f"Syntax error in file: {str(e)}"
                )

            # Add file stats
            analysis["file_path"] = file_path
            analysis["line_count"] = len(content.splitlines())
            analysis["size_bytes"] = len(content.encode('utf-8'))

            return ToolResult(
                success=True,
                result=analysis
            )

        except Exception as e:
            return ToolResult(
                success=False,
                error=f"Analysis failed: {str(e)}"
            )

    def _analyze_ast(self, tree: ast.AST) -> Dict[str, Any]:
        """Analyze AST and extract metadata."""
        imports = []
        classes = []
        functions = []

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append({
                        "type": "import",
                        "module": alias.name,
                        "alias": alias.asname
                    })

            elif isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    imports.append({
                        "type": "from",
                        "module": node.module,
                        "name": alias.name,
                        "alias": alias.asname
                    })

            elif isinstance(node, ast.ClassDef):
                classes.append({
                    "name": node.name,
                    "line": node.lineno,
                    "bases": [self._get_name(base) for base in node.bases],
                    "methods": [
                        m.name for m in node.body
                        if isinstance(m, ast.FunctionDef)
                    ]
                })

            elif isinstance(node, ast.FunctionDef):
                # Only top-level functions (not methods)
                if isinstance(getattr(node, 'parent', None), ast.Module):
                    functions.append({
                        "name": node.name,
                        "line": node.lineno,
                        "args": [arg.arg for arg in node.args.args],
                        "is_async": isinstance(node, ast.AsyncFunctionDef)
                    })

        return {
            "imports": imports,
            "classes": classes,
            "functions": functions,
            "import_count": len(imports),
            "class_count": len(classes),
            "function_count": len(functions)
        }

    def _get_name(self, node: ast.AST) -> str:
        """Extract name from AST node."""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._get_name(node.value)}.{node.attr}"
        else:
            return str(node)


class GetDependenciesTool(BaseTool):
    """Get dependencies between code artifacts."""

    name = "get_dependencies"
    description = "Get dependencies for a code artifact (what it depends on and what depends on it)"

    parameters_schema = {
        "type": "object",
        "properties": {
            "artifact_name": {
                "type": "string",
                "description": "Name of the artifact (class, function, model, etc.)"
            },
            "artifact_type": {
                "type": "string",
                "enum": ["model", "serializer", "view", "function", "class"],
                "description": "Type of artifact",
                "default": "class"
            }
        },
        "required": ["artifact_name"]
    }

    async def execute(self, arguments: Dict[str, Any]) -> ToolResult:
        """Execute dependency lookup."""
        from apps.code.models import ArtifactRegistry

        artifact_name = arguments.get("artifact_name", "")
        artifact_type = arguments.get("artifact_type", "class")

        try:
            # Find artifact in registry
            artifact = await self._get_artifact(artifact_name, artifact_type)

            if not artifact:
                return ToolResult(
                    success=False,
                    error=f"Artifact not found: {artifact_name}"
                )

            # Get dependencies
            dependencies = artifact.dependencies or {}
            depends_on = dependencies.get("depends_on", [])
            depended_by = dependencies.get("depended_by", [])

            return ToolResult(
                success=True,
                result={
                    "artifact_name": artifact_name,
                    "artifact_type": artifact.artifact_type,
                    "file_path": artifact.file_path,
                    "depends_on": depends_on,
                    "depends_on_count": len(depends_on),
                    "depended_by": depended_by,
                    "depended_by_count": len(depended_by)
                }
            )

        except Exception as e:
            return ToolResult(
                success=False,
                error=f"Failed to get dependencies: {str(e)}"
            )

    async def _get_artifact(self, name: str, artifact_type: str):
        """Get artifact from registry."""
        from apps.code.models import ArtifactRegistry
        from asgiref.sync import sync_to_async

        @sync_to_async
        def get():
            return ArtifactRegistry.objects.filter(
                project=self.agent.project,
                name=name,
                artifact_type=artifact_type,
                is_active=True
            ).first()

        return await get()
