import re


class FileParser:
    """
    Extracts files from AI-generated responses.
    Supports multiple formats to avoid empty file generation.
    """

    def parse_files(self, text: str):

        files = {}

        # Pattern 1 — Markdown code blocks
        # Use limited whitespace to avoid matching a distant filename mentioned in natural language
        pattern_markdown = r'([\w\/\.-]+\.\w+)[ \t]*(?:\r?\n[ \t]*){0,2}```[\w]*\r?\n(.*?)```'
        matches = re.findall(pattern_markdown, text, re.DOTALL)

        for filename, code in matches:
            files[filename.strip()] = code.strip()

        # Pattern 2 — write_file format
        # Use DOTALL and lookahead to capture multiline content properly
        pattern_write = r'write_file\s+([\w\/\.-]+\.\w+)\s*\|\s*(.*?)(?=\r?\nwrite_file|\r?\nTHOUGHT:|\r?\nACTION:|\r?\nFINAL:|$)'
        matches_write = re.findall(pattern_write, text, re.DOTALL)

        for filename, code in matches_write:
            files[filename.strip()] = code.strip()

        return files