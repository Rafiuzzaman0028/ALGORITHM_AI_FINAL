import re

try:
    from ai_engine.project_builder.file_parser import FileParser
except (ImportError, ModuleNotFoundError):
    from ..project_builder.file_parser import FileParser


class ResponseFormatter:
    """
    Normalizes AI provider responses.
    Adds a human-friendly project analysis summary.
    """

    def format_results(self, execution_results):
        formatted_results = []

        for item in execution_results["results"]:
            task_type = item.get("task_type")
            provider = item.get("provider")
            result = item.get("result", {})

            output = result.get("output", "")

            formatted = {
                "task_type": task_type,
                "provider": provider,
                "status": result.get("status"),
                "output": output,
                "summary": self.build_human_summary(task_type, output),
                "tokens_used": result.get("tokens_used")
            }

            formatted_results.append(formatted)

        return {
            "formatted_results": formatted_results
        }

    def build_human_summary(self, task_type, output):
        if not output:
            return "No project output was generated."

        files = self.extract_files_from_output(output)
        text = output.lower()
        project_name = self.detect_project_name(output, task_type)
        app_type = self.detect_app_type(task_type, text)
        style = self.detect_style(text)
        features = self.detect_features(text)
        technologies = self.detect_technologies(text, files)

        summary_lines = []

        summary_lines.append(
            f"Here's your {project_name}! It looks like a {app_type} "
            f"with {style}."
        )

        if features:
            summary_lines.append("")
            summary_lines.append("What's included:")
            summary_lines.append("")

            for feature in features[:8]:
                summary_lines.append(f"- {feature}")

        if technologies:
            summary_lines.append("")
            summary_lines.append(
                "Tech stack: " + ", ".join(technologies) + "."
            )

        summary_lines.append("")
        summary_lines.append("To make it yours, you can customize:")
        summary_lines.append("")
        summary_lines.append("- The project name, branding, colors, and content")
        summary_lines.append("- The real data/API endpoints and database connection")
        summary_lines.append("- Any extra pages, dashboard sections, or user flows")
        summary_lines.append("- Whether you want it exported, previewed, or downloaded as a ZIP")

        return "\n".join(summary_lines)

    def extract_files_from_output(self, output):
        files = []

        try:
            parser = FileParser()
            parsed_files = parser.parse_files(output)

            for filename, content in parsed_files.items():
                files.append({
                    "path": filename,
                    "content": content or ""
                })

            if files:
                return files

        except Exception:
            pass

        pattern = r'([\w\/\.-]+\.\w+)'
        matches = re.findall(pattern, output)

        unique_files = []

        for match in matches:
            if match not in unique_files:
                unique_files.append(match)

        for filename in unique_files:
            files.append({
                "path": filename,
                "content": ""
            })

        return files

    def detect_project_name(self, output, task_type):
        patterns = [
            r'"name"\s*:\s*"([^"]+)"',
            r"'name'\s*:\s*'([^']+)'",
            r"#\s*([A-Za-z0-9 \-_]+)",
            r"title>\s*([^<]+)\s*</title>"
        ]

        for pattern in patterns:
            match = re.search(pattern, output, re.IGNORECASE)
            if match:
                name = match.group(1).strip()
                name = name.replace("-", " ").replace("_", " ")
                return name

        if task_type:
            return f"{task_type} project"

        return "project"

    def detect_app_type(self, task_type, text):
        if "movie" in text or "streaming" in text:
            return "movie streaming web app"

        if "portfolio" in text:
            return "developer portfolio website"

        if "e-commerce" in text or "cart" in text or "product" in text:
            return "e-commerce website"

        if "dashboard" in text or "analytics" in text:
            return "dashboard application"

        if "todo" in text or "task" in text:
            return "task management app"

        if "blog" in text:
            return "blog website"

        if "restaurant" in text or "menu" in text:
            return "restaurant website"

        if "login" in text or "auth" in text:
            return "full-stack authenticated web app"

        if task_type:
            return f"{task_type} application"

        return "web application"

    def detect_style(self, text):
        style_parts = []

        if "dark" in text:
            style_parts.append("a dark modern aesthetic")

        if "gradient" in text:
            style_parts.append("gradient-based visual styling")

        if "responsive" in text:
            style_parts.append("a responsive layout")

        if "tailwind" in text:
            style_parts.append("utility-first Tailwind styling")

        if "card" in text or "cards" in text:
            style_parts.append("card-based sections")

        if "terminal" in text:
            style_parts.append("a terminal-inspired feel")

        if not style_parts:
            return "a clean modern interface"

        return ", ".join(style_parts)

    def detect_features(self, text):
        checks = [
            ("Hero section with headline and call-to-action buttons", ["hero", "cta"]),
            ("Navigation bar for moving between sections/pages", ["navbar", "navigation", "nav"]),
            ("Movie listing/cards with titles, images, and descriptions", ["movie", "card"]),
            ("Search or filtering experience for finding content", ["search", "filter"]),
            ("Authentication flow with login/signup support", ["login", "signup", "auth", "authentication"]),
            ("Backend API routes for serving application data", ["express", "router", "api"]),
            ("Database/model layer for storing project data", ["mongoose", "mongodb", "schema", "model"]),
            ("Responsive layout for desktop and mobile screens", ["responsive", "mobile"]),
            ("Project cards with tags and descriptions", ["project", "tags", "description"]),
            ("About section with profile or background information", ["about"]),
            ("Contact section with email/social links", ["contact", "email", "github", "linkedin"]),
            ("Reusable React components for cleaner frontend structure", ["component", "react"]),
            ("Styling files for layout, colors, and visual polish", ["css", "style"])
        ]

        features = []

        for feature, keywords in checks:
            if any(keyword in text for keyword in keywords):
                features.append(feature)

        if not features:
            features = [
                "Generated project structure based on your prompt",
                "Application code organized into runnable files",
                "Basic implementation ready for preview and customization"
            ]

        return features

    def detect_technologies(self, text, files):
        file_paths = " ".join([f["path"].lower() for f in files])
        combined = text + " " + file_paths

        technologies = []

        checks = {
            "React": ["react", "jsx", "tsx", "react-scripts"],
            "Vite": ["vite"],
            "Node.js": ["node", "package.json"],
            "Express": ["express"],
            "MongoDB": ["mongoose", "mongodb"],
            "Tailwind CSS": ["tailwind"],
            "HTML": [".html"],
            "CSS": [".css"],
            "JavaScript": [".js", ".jsx"],
            "Python": [".py"],
            "FastAPI": ["fastapi"],
            "Flask": ["flask"]
        }

        for tech, keywords in checks.items():
            if any(keyword in combined for keyword in keywords):
                technologies.append(tech)

        return technologies