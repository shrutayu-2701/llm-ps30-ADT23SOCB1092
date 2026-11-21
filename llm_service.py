"""Local Ollama API integration, separate from the Streamlit interface."""

import json
import os
from typing import Optional
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from prompt_template import SYSTEM_INSTRUCTION, build_lesson_prompt

DEFAULT_MODEL = "llama3.2:3b"
DEFAULT_BASE_URL = "http://localhost:11434"
REQUEST_TIMEOUT_SECONDS = 180


class LessonPlanError(RuntimeError):
    """A safe, user-displayable lesson generation error."""


def validate_inputs(topic: str, subject: str, grade: str, duration: int) -> Optional[str]:
    """Return an explanation when required values are invalid; otherwise None."""
    if not topic or not topic.strip():
        return "Enter a lesson topic."
    if not subject or not subject.strip():
        return "Enter a subject."
    if not grade or not grade.strip():
        return "Enter a grade or class."
    if not isinstance(duration, int) or duration < 1 or duration > 180:
        return "Choose a lesson duration between 1 and 180 minutes."
    return None


def _base_url() -> str:
    return os.getenv("OLLAMA_BASE_URL", DEFAULT_BASE_URL).strip().rstrip("/")


def get_ollama_models() -> list[str]:
    """Return model names installed in the local Ollama instance."""
    request = Request(f"{_base_url()}/api/tags", headers={"Accept": "application/json"})
    try:
        with urlopen(request, timeout=5) as response:
            payload = json.loads(response.read().decode("utf-8"))
        return sorted({item.get("name") for item in payload.get("models", []) if item.get("name")})
    except (URLError, TimeoutError, OSError):
        raise LessonPlanError(
            "Ollama is not reachable. Open the Ollama app, then refresh this page."
        ) from None
    except (ValueError, AttributeError, TypeError):
        raise LessonPlanError("Ollama returned an unreadable model list.") from None


def stream_lesson_plan(topic: str, subject: str, grade: str, duration: int,
                       model: str = DEFAULT_MODEL, teaching_instructions: str = "",
                       learning_level: str = ""):
    """Yield Markdown as a locally installed Ollama model generates it."""
    validation_error = validate_inputs(topic, subject, grade, duration)
    if validation_error:
        raise LessonPlanError(validation_error)
    if not model or not model.strip():
        raise LessonPlanError("Select an Ollama model.")

    body = {
        "model": model.strip(),
        "stream": True,
        "messages": [
            {"role": "system", "content": SYSTEM_INSTRUCTION},
            {"role": "user", "content": build_lesson_prompt(
                topic, subject, grade, duration, teaching_instructions, learning_level
            )},
        ],
        # Bound output length and context to keep local generation responsive.
        "options": {"temperature": 0.3, "num_predict": 1000, "num_ctx": 4096},
    }
    request = Request(
        f"{_base_url()}/api/chat",
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        method="POST",
    )
    yielded_content = False
    try:
        with urlopen(request, timeout=REQUEST_TIMEOUT_SECONDS) as response:
            for raw_line in response:
                if not raw_line.strip():
                    continue
                payload = json.loads(raw_line.decode("utf-8"))
                if payload.get("error"):
                    raise LessonPlanError(
                        "Ollama could not complete the request. Check the selected model and try again."
                    )
                content = payload.get("message", {}).get("content", "")
                if content:
                    yielded_content = True
                    yield content
        if not yielded_content:
            raise LessonPlanError("Ollama returned an empty response. Try again.")
    except LessonPlanError:
        raise
    except HTTPError as exc:
        if exc.code == 404:
            raise LessonPlanError(
                f"The model '{model}' is not available. Pull it with: ollama pull {model}"
            ) from None
        raise LessonPlanError(f"Ollama returned an HTTP {exc.code} error. Check the local service and retry.") from None
    except (URLError, TimeoutError, OSError):
        raise LessonPlanError(
            "Could not connect to Ollama. Open the Ollama app and confirm it is running."
        ) from None
    except (ValueError, AttributeError, TypeError):
        raise LessonPlanError("Ollama returned an unreadable response. Try again.") from None
