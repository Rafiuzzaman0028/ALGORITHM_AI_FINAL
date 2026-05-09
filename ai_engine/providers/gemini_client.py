from ai_engine.providers.base_provider import BaseProvider

import os
import base64
from io import BytesIO
from pathlib import Path
from datetime import datetime
from uuid import uuid4

from dotenv import load_dotenv
from PIL import Image
from google import genai
from google.genai import types


load_dotenv()


class GeminiClient(BaseProvider):
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")

        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")

        self.client = genai.Client(api_key=self.api_key)

        self.text_model = os.getenv("GEMINI_TEXT_MODEL", "gemini-2.5-flash")
        self.image_model = os.getenv(
            "GEMINI_IMAGE_MODEL",
            "gemini-3.1-flash-image-preview"
        )

    def generate_response(self, prompt, config=None):
        try:
            model = config.get("model") if config and config.get("model") else self.text_model

            response = self.client.models.generate_content(
                model=model,
                contents=prompt
            )

            output_text = getattr(response, "text", None) or ""

            return {
                "provider": "gemini",
                "status": "success",
                "output": output_text,
                "tokens_used": None
            }

        except Exception as e:
            return {
                "provider": "gemini",
                "status": "error",
                "output": str(e),
                "tokens_used": None
            }

    def generate_image(self, prompt, output_dir="generated_projects"):
        """
        Generates an image using Gemini only and saves it inside generated_projects.
        """

        try:
            Path(output_dir).mkdir(parents=True, exist_ok=True)

            safe_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"gemini_image_{safe_timestamp}_{uuid4().hex[:6]}.png"
            output_path = Path(output_dir) / filename

            response = self.client.models.generate_content(
                model=self.image_model,
                contents=[prompt],
                config=types.GenerateContentConfig(
                    response_modalities=["TEXT", "IMAGE"]
                )
            )

            text_outputs = []

            parts = getattr(response, "parts", None)

            if not parts:
                candidates = getattr(response, "candidates", []) or []
                if candidates:
                    content = getattr(candidates[0], "content", None)
                    parts = getattr(content, "parts", []) if content else []

            for part in parts or []:
                part_text = getattr(part, "text", None)
                if part_text:
                    text_outputs.append(part_text)

                image = None

                if hasattr(part, "as_image"):
                    try:
                        image = part.as_image()
                    except Exception:
                        image = None

                if image:
                    image.save(output_path)
                    return {
                        "provider": "gemini",
                        "status": "success",
                        "output": "Image generated successfully.",
                        "image_path": str(output_path),
                        "tokens_used": None
                    }

                inline_data = getattr(part, "inline_data", None)
                if inline_data:
                    image_bytes = inline_data.data

                    if isinstance(image_bytes, str):
                        image_bytes = base64.b64decode(image_bytes)

                    image = Image.open(BytesIO(image_bytes))
                    image.save(output_path)

                    return {
                        "provider": "gemini",
                        "status": "success",
                        "output": "Image generated successfully.",
                        "image_path": str(output_path),
                        "tokens_used": None
                    }

            return {
                "provider": "gemini",
                "status": "error",
                "output": "Gemini did not return an image. Response text: " + " ".join(text_outputs),
                "image_path": None,
                "tokens_used": None
            }

        except Exception as e:
            return {
                "provider": "gemini",
                "status": "error",
                "output": str(e),
                "image_path": None,
                "tokens_used": None
            }