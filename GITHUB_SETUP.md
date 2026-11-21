# Publish to GitHub

The public repository is `https://github.com/shrutayu-2701/llm-ps30-ADT23SOCB1092`. Open a terminal in this folder and use:

```powershell
git init
git add .
git status
git commit -m "Create AI lesson plan generator mini project"
git branch -M main
git remote add origin https://github.com/shrutayu-2701/llm-ps30-ADT23SOCB1092.git
git push -u origin main
```

Review `git status` before committing. The local `.env` file pattern is ignored by Git; this local Ollama setup does not need a cloud API key.
