"""Offline tests for prompt construction, validation, and Ollama API handling."""

import json
import unittest
from io import BytesIO
from unittest.mock import patch
from urllib.error import URLError

from llm_service import (
    LessonPlanError,
    get_ollama_models,
    stream_lesson_plan,
    validate_inputs,
)
from prompt_template import SYSTEM_INSTRUCTION, build_lesson_prompt


SAMPLES = [
    ("Introduction to Artificial Intelligence", "Computer Science", "8", 40),
    ("Photosynthesis", "Science", "7", 45),
    ("Fractions", "Mathematics", "5", 30),
    ("Cyber Safety", "Computer Science", "9", 40),
    ("Water Cycle", "Science", "6", 60),
]


class ProjectTests(unittest.TestCase):
    def test_five_sample_prompts_preserve_input_and_duration(self):
        for topic, subject, grade, duration in SAMPLES:
            with self.subTest(topic=topic):
                prompt = build_lesson_prompt(topic, subject, grade, duration)
                self.assertIn(topic, prompt)
                self.assertIn(subject, prompt)
                self.assertIn(f"Grade/Class: {grade}", prompt)
                self.assertIn(f"sum exactly {duration}", prompt)
                self.assertIn("Teacher Activity", prompt)
                self.assertIn("Assessment/Evaluation Questions", prompt)

    def test_system_instruction_covers_timing_and_topic(self):
        self.assertIn("Never replace the topic", SYSTEM_INSTRUCTION)
        self.assertIn("add up to that duration", SYSTEM_INSTRUCTION)

    def test_input_validation(self):
        self.assertIsNone(validate_inputs("Fractions", "Math", "5", 30))
        self.assertEqual(validate_inputs("  ", "Math", "5", 30), "Enter a lesson topic.")
        self.assertIn("duration", validate_inputs("Topic", "Science", "5", 0))

    def test_model_list_uses_local_tags_endpoint(self):
        payload = {"models": [{"name": "llama3.2:3b"}, {"name": "mistral:7b"}]}
        response = BytesIO(json.dumps(payload).encode())
        with patch("llm_service.urlopen") as open_url:
            open_url.return_value.__enter__.return_value = response
            models = get_ollama_models()
        self.assertEqual(models, ["llama3.2:3b", "mistral:7b"])
        self.assertIn("/api/tags", open_url.call_args.args[0].full_url)

    def test_mock_ollama_chat_stream_returns_markdown(self):
        events = [
            {"message": {"role": "assistant", "content": "# Fractions"}},
            {"message": {"role": "assistant", "content": " lesson"}},
            {"message": {"role": "assistant", "content": " plan"}, "done": True},
        ]
        response = BytesIO(b"".join((json.dumps(event) + "\n").encode() for event in events))
        with patch("llm_service.urlopen") as open_url:
            open_url.return_value.__enter__.return_value = response
            result = "".join(stream_lesson_plan(
                "Fractions", "Mathematics", "5", 30, model="llama3.2:3b"
            ))
        self.assertEqual(result, "# Fractions lesson plan")
        request = open_url.call_args.args[0]
        body = json.loads(request.data.decode())
        self.assertEqual(body["model"], "llama3.2:3b")
        self.assertTrue(body["stream"])
        self.assertEqual(body["options"]["num_predict"], 1000)
        self.assertEqual(body["messages"][0]["role"], "system")
        self.assertIn("sum exactly 30", body["messages"][1]["content"])

    def test_unreachable_ollama_has_friendly_error(self):
        with patch("llm_service.urlopen", side_effect=URLError("offline")):
            with self.assertRaisesRegex(LessonPlanError, "not reachable"):
                get_ollama_models()


if __name__ == "__main__":
    unittest.main()
