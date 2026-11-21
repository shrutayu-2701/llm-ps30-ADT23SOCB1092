# Viva Preparation

1. **What is Generative AI?** It is AI that creates new content, such as text, from patterns learned during training.
2. **What is an LLM?** A Large Language Model is an AI model trained to understand and generate language.
3. **What is prompt engineering?** It is writing clear instructions and context to guide a model's response.
4. **Why did you use Ollama?** It runs language models locally and exposes a local HTTP API, so this project can generate plans without a Gemini API key.
5. **What is an API?** An API is a defined way for one software program to request a service from another.
6. **How does the app communicate with Ollama?** `llm_service.py` sends the system instruction and lesson prompt to Ollama's local `/api/chat` endpoint and streams the generated text into the page.
7. **What is Streamlit?** It is a Python library for building interactive web apps with Python code.
8. **What is the system instruction?** It gives the local model its role and general rules for the lesson plan.
9. **How does the prompt affect output?** It specifies the exact topic, grade, duration, required sections, and timing rules, making the result more focused.
10. **What is temperature in this project?** The Ollama request sets temperature to 0.4. It controls variation in generated responses; lower values generally make outputs less varied.
11. **What is an environment variable?** It is configuration stored outside the source code and read by a program when it runs. This app can use `OLLAMA_BASE_URL` and `OLLAMA_MODEL` as optional settings.
12. **Why is an API key not in the code?** The local Ollama API does not require a cloud API key for local models.
13. **Explain the workflow.** The user enters details, Python validates them, the prompt is built, Ollama generates Markdown locally, Streamlit displays it, and the user can download it.
14. **What does `app.py` do?** It defines the Streamlit inputs, invokes the service, displays results, and offers downloads.
15. **What does `llm_service.py` do?** It validates inputs, reads configuration, calls Gemini, and turns common failures into clear messages.
16. **What does each other project file do?** `prompt_template.py` builds the prompt; `requirements.txt` lists app libraries; `.gitignore` excludes local and generated files; `tests/test_project.py` contains offline tests; `Report.pdf` is the procedure report and `build_report.py` rebuilds it; `TESTING_RESULTS.md` records checks; `screenshots/README.md` lists screenshot guidance; `GITHUB_SETUP.md` gives publishing commands; and `README.md` explains setup and use.
17. **What are the project's limitations?** Ollama and a downloaded model must be installed locally, speed depends on the computer, and generated content may need teacher review for accuracy and timing.
18. **How could the project improve?** It could automatically parse the teaching table and check whether the row times sum to the requested duration.
