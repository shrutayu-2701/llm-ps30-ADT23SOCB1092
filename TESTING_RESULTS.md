# Verification results

| Check | Input or method | Expected behavior | Actual result | Status |
|---|---|---|---|---|
| AI lesson prompt | Introduction to Artificial Intelligence, Computer Science, Grade 8, 40 min | Preserve topic and include requested sections and duration | Prompt includes topic, subject, grade, duration, table, and assessment requirements | PASS |
| Science prompt | Photosynthesis, Science, Grade 7, 45 min | Preserve topic and duration | Prompt assertions passed | PASS |
| Mathematics prompt | Fractions, Mathematics, Grade 5, 30 min | Preserve topic and duration | Prompt assertions passed | PASS |
| Safety prompt | Cyber Safety, Computer Science, Grade 9, 40 min | Preserve topic and duration | Prompt assertions passed | PASS |
| Water-cycle prompt | Water Cycle, Science, Grade 6, 60 min | Preserve topic and duration | Prompt assertions passed | PASS |
| Required-input validation | Blank topic and valid other values | Return a clear validation message | Returned `Enter a lesson topic.` | PASS |
| Duration validation | 0 minutes | Reject invalid duration | Returned a duration error | PASS |
| Local model listing | Mock response from `/api/tags` | Return installed local model names | Parsed and sorted two model names | PASS |
| Mock Ollama chat stream | Mock chunked response from `/api/chat` | Send model and prompt, yield Markdown chunks, cap output | Request payload and streamed Markdown assertions passed | PASS |
| Ollama unavailable | Mock connection failure | Friendly error without a crash | Raised `LessonPlanError` advising to start Ollama | PASS |
| Python syntax | `py_compile` on app, service, prompt, tests, report builder | No syntax errors | Completed without errors | PASS |
| Procedure report | `pypdf` page count | Exactly two pages | 2 pages | PASS |
| Ollama local service | GET `http://localhost:11434/api/tags` from development runtime | Connect to the user's local Ollama service | Service was unreachable from this runtime; no live generation performed | NOT RUN |
| Streamlit launch | `python -m streamlit run app.py` in bundled runtime | Start local web app | Streamlit is not installed in the bundled runtime | BLOCKED |

Run offline tests with:

```powershell
python -m unittest discover -s tests -v
```

Run the application with Ollama open and a model installed:

```powershell
streamlit run app.py
```
