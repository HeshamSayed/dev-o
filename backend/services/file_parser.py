"""
File parser for extracting file blocks from AI responses.
"""

import re
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class FileParser:
    """Parse AI responses for file creation tags."""

    FILE_PATTERN = r'<file\s+path="([^"]+)"\s*>(.*?)</file>'

    @staticmethod
    def parse_files(content: str) -> List[Dict[str, str]]:
        """
        Parse AI response content for file blocks.

        Format:
        <file path="path/to/file.py">
        file content here
        </file>

        If no file tags found, attempts to extract from markdown code blocks.

        Args:
            content: AI response text containing file blocks

        Returns:
            List of dicts with 'path' and 'content' keys
        """
        files = []

        # Find all file blocks using regex
        matches = re.finditer(
            FileParser.FILE_PATTERN,
            content,
            re.DOTALL | re.MULTILINE
        )

        for match in matches:
            path = match.group(1).strip()
            file_content = match.group(2).strip()

            files.append({
                'path': path,
                'content': file_content
            })

        # Fallback: If no file tags found, try to extract from markdown code blocks
        if not files:
            logger.warning("[FILE_PARSER] No file tags found, attempting markdown code block extraction")
            files = FileParser._extract_from_markdown(content)
            if files:
                logger.info(f"[FILE_PARSER] Extracted {len(files)} files from markdown")

        return files

    @staticmethod
    def _extract_from_markdown(content: str) -> List[Dict[str, str]]:
        """
        Extract code blocks from markdown format and infer filenames.

        Looks for patterns like:
        Creating `main.py`:
        ```python
        code here
        ```

        Or:
        ### main.py
        ```python
        code here
        ```
        """
        files = []

        # Pattern 1: "Creating `filename`:" followed by code block (with possible newlines)
        # Matches: Creating `main.py`:\n```python\ncode\n```
        pattern1 = r'(?:Creating|creating)\s+[`"]([a-zA-Z0-9_./]+\.[a-zA-Z0-9]+)[`"]\s*:?\s*\n*```\w*\s*\n(.*?)```'
        matches1 = re.findall(pattern1, content, re.DOTALL)
        for filename, code in matches1:
            files.append({
                'path': filename.strip(),
                'content': code.strip()
            })
            logger.info(f"[FILE_PARSER] Extracted from markdown (pattern 1): {filename}")

        # Pattern 2: Heading followed by code block
        pattern2 = r'###?\s+([a-zA-Z0-9_./]+\.[a-zA-Z0-9]+)\s*\n```(?:\w+)?\s*\n(.*?)```'
        matches2 = re.findall(pattern2, content, re.DOTALL)
        for filename, code in matches2:
            # Avoid duplicates
            if not any(f['path'] == filename.strip() for f in files):
                files.append({
                    'path': filename.strip(),
                    'content': code.strip()
                })
                logger.info(f"[FILE_PARSER] Extracted from markdown (pattern 2): {filename}")

        # Pattern 3: Just code blocks with language hints - infer filename
        if not files:
            pattern3 = r'```(\w+)\s*\n(.*?)```'
            matches3 = re.findall(pattern3, content, re.DOTALL)
            for idx, (lang, code) in enumerate(matches3):
                # Infer file extension from language
                ext_map = {
                    'python': 'py',
                    'javascript': 'js',
                    'typescript': 'ts',
                    'java': 'java',
                    'cpp': 'cpp',
                    'c': 'c',
                    'go': 'go',
                    'rust': 'rs',
                    'ruby': 'rb',
                    'php': 'php',
                    'html': 'html',
                    'css': 'css',
                    'json': 'json',
                    'yaml': 'yaml',
                    'yml': 'yml',
                    'sql': 'sql',
                    'bash': 'sh',
                    'sh': 'sh',
                }
                ext = ext_map.get(lang.lower(), 'txt')
                filename = f"generated_{idx + 1}.{ext}"
                files.append({
                    'path': filename,
                    'content': code.strip()
                })
                logger.info(f"[FILE_PARSER] Extracted generic code block as: {filename}")

        return files

    @staticmethod
    def strip_file_tags(content: str) -> str:
        """
        Remove file tags from content, leaving only the text.
        Useful for displaying clean messages to users.

        Args:
            content: AI response text with file blocks

        Returns:
            Content with file blocks removed
        """
        return re.sub(
            FileParser.FILE_PATTERN,
            '',
            content,
            flags=re.DOTALL | re.MULTILINE
        ).strip()

    @staticmethod
    def contains_files(content: str) -> bool:
        """
        Check if content contains any file blocks.

        Args:
            content: AI response text

        Returns:
            True if content contains file blocks, False otherwise
        """
        return bool(re.search(FileParser.FILE_PATTERN, content))

    @staticmethod
    def detect_language(file_path: str) -> str:
        """
        Detect programming language from file extension.

        Args:
            file_path: Path to the file

        Returns:
            Language identifier for syntax highlighting
        """
        extension_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.jsx': 'javascript',
            '.ts': 'typescript',
            '.tsx': 'typescript',
            '.html': 'html',
            '.css': 'css',
            '.scss': 'scss',
            '.sass': 'sass',
            '.json': 'json',
            '.xml': 'xml',
            '.yaml': 'yaml',
            '.yml': 'yaml',
            '.md': 'markdown',
            '.sh': 'bash',
            '.bash': 'bash',
            '.sql': 'sql',
            '.java': 'java',
            '.c': 'c',
            '.cpp': 'cpp',
            '.cs': 'csharp',
            '.go': 'go',
            '.rs': 'rust',
            '.php': 'php',
            '.rb': 'ruby',
            '.swift': 'swift',
            '.kt': 'kotlin',
            '.r': 'r',
            '.dockerfile': 'dockerfile',
            '.env': 'text',
            '.txt': 'text',
        }

        # Get file extension
        for ext, lang in extension_map.items():
            if file_path.lower().endswith(ext):
                return lang

        # Special cases for files without extensions
        filename = file_path.split('/')[-1].lower()
        if filename in ['dockerfile', 'makefile', 'rakefile']:
            return filename.lower()

        return 'text'
