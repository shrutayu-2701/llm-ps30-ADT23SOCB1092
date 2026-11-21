# AI Lesson Plan Generator

An educational Generative AI mini-project that creates a structured classroom lesson plan from a teacher's topic, subject, grade, duration, and optional guidance.

## Student details

- **Student:** Shrutayu Chopade
- **Roll number / problem statement:** 30
- **Enrollment number:** ADT23SOCB1092
- **Class:** LY CORE 2
- **Assignment:** GenAI (LLM) Final Mini Project

## Problem statement and objective

School teachers need practical, structured lesson plans with objectives, activities, timing, and assessment. This app uses a locally running Ollama model to draft an age-appropriate lesson plan from teacher-provided inputs and lets the user view and download it.

## Features

- Topic, subject, grade, duration, student level, and teaching guidance inputs.
- Ollama-generated lesson plan displayed as Markdown, using a model installed on the computer.
- Lesson text streams into the page while Ollama generates it, with a concise output limit to reduce waiting.
- Plan sections for objectives, prerequisites, resources, warm-up, timed teaching table, examples, assessment, differentiation, recap, and follow-up.
- Download generated content as `.md` or `.txt`.
- Validation, loading feedback, input reset, and friendly API errors.

## Technologies

Python, Streamlit, the Ollama local HTTP API, Python standard-library HTTP/JSON tools, Python `unittest`, and Markdown. The default model is `llama3.2:3b`; the app lets you choose another installed model.

## Workflow

Teacher inputs → `build_lesson_prompt()` in `prompt_template.py` → system and user instructions sent by `llm_service.py` to the local Ollama API → Markdown response shown by `app.py` → download as text or Markdown. The prompt asks the model to make the table's times add up to the selected duration; review generated content before teaching.

## Project files

```text
app.py                 Streamlit form and generated-plan display
llm_service.py         Input validation and local Ollama API calls
prompt_template.py     System instruction and prompt builder
requirements.txt       Required Python packages
tests/test_project.py  Offline tests for sample inputs and validation
build_report.py        Rebuilds the procedure report (ReportLab needed)
Report.pdf             Two-page procedure report
TESTING_RESULTS.md     Checks performed and environment limits
VIVA_PREPARATION.md    Viva questions and answers
GITHUB_SETUP.md        Commands to publish the repository
screenshots/           Checklist for genuine screenshots
.streamlit/config.toml Light theme and accessible color palette
```

## Setup and run

1. Install Python 3.10 or newer and install [Ollama for Windows](https://ollama.com/download/windows).
2. Open Ollama so its local service is running. In PowerShell, download a small starter model:

   ```powershell
   ollama pull llama3.2:3b
   ```

   You may use another local model already installed in Ollama.
3. Open a terminal in this project folder and create/activate a virtual environment:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

4. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

5. Start the app:

   ```powershell
   streamlit run app.py
   ```

The app opens in a browser. No plan is generated until **Generate Lesson Plan** is clicked. It connects to Ollama at `http://localhost:11434`; no API key is required. If Ollama is running at a different address, set `OLLAMA_BASE_URL` before launching the app. To choose the default model, set `OLLAMA_MODEL`.

## Sample input and output

Sample: Topic `Photosynthesis`, Subject `Science`, Grade `7`, Duration `45` minutes. The response is Markdown with the requested lesson-plan headings and a table containing time, stage, teacher activity, student activity, and teaching method/resources.

## Testing

Run offline checks with:

```powershell
python -m unittest discover -s tests -v
```

These tests cover all five assignment sample prompts, exact duration presence, required inputs, system-instruction requirements, and mocked Ollama API behavior. A real generation needs Ollama running locally with a model installed.

## Limitations and future scope

Generated content can contain factual or timing errors, so a teacher should review it. Local generation requires Ollama and a model downloaded on the computer; speed depends on available hardware. A future version could validate extracted table timings automatically and allow export to PDF.

## GitHub publishing

The required public repository name is `llm-ps30-ADT23SOCB1092`. See [GITHUB_SETUP.md](GITHUB_SETUP.md) for commands. Do not commit `.env`.
