import re


class FileParser:

    def parse_files(self, text):

        files = {}

        patterns = [

            r'FILE:\s*([^\n]+)\n```[\w]*\n(.*?)```',

            r'###\s*([^\n]+)\n```[\w]*\n(.*?)```',

            r'([^\n]+\.\w+)\n```[\w]*\n(.*?)```'
        ]

        for pattern in patterns:

            matches = re.findall(pattern, text, re.DOTALL)

            for filename, content in matches:

                filename = filename.strip()
                content = content.strip()

                files[filename] = content

        return files