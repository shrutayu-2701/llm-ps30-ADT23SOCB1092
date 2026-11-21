"""Prompt construction for the lesson-plan generator."""

SYSTEM_INSTRUCTION = """You are an experienced school teacher and lesson-planning expert. Create practical, age-appropriate lesson plans using the user's exact topic and subject. Never replace the topic. Adapt language and difficulty to the grade, create measurable learning objectives, use realistic classroom activities, include teacher and student actions, allocate time logically, and include useful assessment questions. Follow the requested duration exactly and check that all rows in the teaching-plan table add up to that duration before responding. Apply optional teaching instructions and learning-level guidance. Avoid irrelevant information. Return clear Markdown with all requested headings and a readable table."""


def build_lesson_prompt(topic: str, subject: str, grade: str, duration: int,
                        teaching_instructions: str = "", learning_level: str = "") -> str:
    """Build the user prompt from validated lesson details."""
    return f"""Prepare a complete lesson plan from the details below.

Lesson/topic: {topic.strip()}
Subject: {subject.strip()}
Grade/Class: {grade.strip()}
Total duration: {duration} minutes
Student learning level: {learning_level.strip() or 'Use typical expectations for this grade.'}
Teaching style/additional instructions: {teaching_instructions.strip() or 'None provided.'}

Use these sections in order:
1. Lesson Title
2. Subject, Grade/Class, and Duration
3. Learning Objectives (measurable)
4. Prerequisite Knowledge
5. Teaching Materials/Resources Required
6. Introduction/Warm-up
7. Detailed Teaching Plan as a Markdown table with columns: Time, Teaching Stage, Teacher Activity, Student Activity, Teaching Method/Resources
8. Examples or Demonstrations
9. Assessment/Evaluation Questions
10. Differentiation or Support for Students Who Need Help
11. Conclusion/Recap
12. Homework or Follow-up Activity (if appropriate)

Keep the table's activity times in minutes and make their sum exactly {duration}. Use 4-6 activity rows, keep each section and table cell concise, and avoid repeating ideas. Include practical teaching and student actions. Do not add unrelated topics."""
