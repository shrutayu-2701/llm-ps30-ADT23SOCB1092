"""Build the two-page academic procedure report (requires reportlab)."""

from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer


def make_report():
    doc = SimpleDocTemplate(
        "Report.pdf", pagesize=A4, rightMargin=20 * mm, leftMargin=20 * mm,
        topMargin=15 * mm, bottomMargin=15 * mm,
        title="AI Lesson Plan Generator - Procedure Report",
        author="Shrutayu Chopade",
    )
    styles = getSampleStyleSheet()
    body = ParagraphStyle("Body12", parent=styles["BodyText"], fontName="Times-Roman",
                          fontSize=12, leading=14, spaceAfter=5, alignment=4)
    title = ParagraphStyle("Title12", parent=body, fontName="Times-Bold",
                           alignment=TA_CENTER, spaceAfter=8)
    heading = ParagraphStyle("Heading12", parent=body, fontName="Times-Bold",
                             spaceBefore=5, spaceAfter=3)
    story = [
        Paragraph("GENAI FINAL MINI PROJECT - PROCEDURE REPORT", title),
        Paragraph("AI Lesson Plan Generator for Teachers | Problem Statement 30", title),
        Paragraph("Student: Shrutayu Chopade | Roll No.: 30 | Enrollment: ADT23SOCB1092 | Class: LY CORE 2", body),
        Paragraph("1. Problem Statement", heading),
        Paragraph("School teachers need structured plans that connect learning objectives with classroom activities, suitable explanations, time allocation, and assessment. This application supports teachers by drafting a lesson plan from a topic, subject, grade, and duration.", body),
        Paragraph("2. Tools and Model", heading),
        Paragraph("The implementation uses Python 3 and Streamlit for the web interface. It sends HTTP requests with Python's standard urllib and JSON libraries to Ollama's local API at localhost:11434. The default local model is llama3.2:3b; the app can select another installed model. Markdown presents the generated plan, and Python's unittest supports offline checks.", body),
        Paragraph("3. Procedure", heading),
        Paragraph("The project folder is organized into a Streamlit interface, an Ollama service module, and a prompt module. Required packages are listed in requirements.txt. The user installs Ollama and downloads a local model, then installs the app's Python dependencies in a virtual environment. The interface collects topic, subject, grade, duration, student level, and optional teaching instructions. It validates required values before making a request.", body),
        Paragraph("The prompt builder inserts the user's details and specifies the output sections and a five-column teaching table. A system instruction guides the local model to act as an experienced teacher, preserve the topic, adjust to the grade, set measurable objectives, provide both teacher and student actions, and check total timing. The response streams progressively into the page and is then displayed as Markdown with Markdown and text download options. Generation is concise with a 1,000-token output cap. Connection, missing-model, and empty-response errors are handled with readable messages. Offline unit tests cover the five sample inputs, prompt requirements, validation, and mocked Ollama streaming.", body),
        Paragraph("4. Prompt Used", heading),
        Paragraph("The final instruction asks the local model to prepare a complete lesson plan for the specified topic, subject, grade, and total minutes; account for optional learning-level and teaching guidance; and return title and metadata, measurable objectives, prerequisites, resources, warm-up, a timed table (time, stage, teacher activity, student activity, method/resources), examples, assessment, differentiation, recap, and follow-up. It explicitly says the table times must sum exactly to the requested duration and the topic must not be changed.", body),
        Paragraph("Prompt improvement: the initial idea of asking for a general lesson plan was made more precise by enumerating required sections, table columns, and an exact timing check. This helps produce a consistent, easier-to-review classroom plan.", body),
        PageBreak(),
        Paragraph("GENAI FINAL MINI PROJECT - PROCEDURE REPORT (continued)", title),
        Paragraph("5. Results", heading),
        Paragraph("Sample input: Introduction to Artificial Intelligence; Computer Science; Grade 8; 40 minutes. The application is designed to return the requested headings and a timed activity table, then display and offer the Markdown/text downloads. A live Ollama result and screenshots are not included because no Ollama service was reachable in the development environment; this report does not claim a model response was received.", body),
        Paragraph("6. Technical Considerations", heading),
        Paragraph("Two practical considerations are connecting reliably to the local Ollama service and handling variable model responses safely. The app checks the service for installed models and provides friendly messages for connection, missing-model, and empty-response errors. Prompt instructions request exact timing, but the returned table still requires teacher review because generated output is not a guaranteed calculation.", body),
        Paragraph("7. Conclusion", heading),
        Paragraph("The application implements the core GenAI workflow: user input, prompt construction, local Ollama API request, Markdown display, and file download. Live generation requires Ollama and a model installed on the user's computer; the lesson request is sent to the local service. Model output may contain inaccurate educational details or timing, so a teacher should check each plan before classroom use. A useful future improvement is automated parsing and validation of the activity table's duration total.", body),
        Paragraph("Submission note: capture genuine screenshots after starting Ollama, installing a model, and running the app. Suggested views and filenames are listed in screenshots/README.md.", body),
    ]
    doc.build(story)


if __name__ == "__main__":
    make_report()
