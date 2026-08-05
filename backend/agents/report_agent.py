from datetime import datetime
from pathlib import Path

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate

from backend.utils.logger import logger


class ReportAgent:

    def __init__(self):
        self.report_dir = Path("backend/reports")
        self.report_dir.mkdir(parents=True, exist_ok=True)

    def generate_markdown(self, review: str, commit_hash: str) -> str:

        filename = self.report_dir / f"{commit_hash}.md"

        with open(filename, "w", encoding="utf-8") as file:
            file.write(f"# AI Code Review\n\n")
            file.write(f"Generated: {datetime.now()}\n\n")
            file.write(review)

        logger.info("Markdown report generated.")

        return str(filename)

    def generate_pdf(self, review: str, commit_hash: str) -> str:

        filename = self.report_dir / f"{commit_hash}.pdf"

        document = SimpleDocTemplate(str(filename))
        styles = getSampleStyleSheet()

        elements = [
            Paragraph("<b>AI Code Review</b>", styles["Heading1"]),
            Paragraph(review.replace("\n", "<br/>"), styles["BodyText"]),
        ]

        document.build(elements)

        logger.info("PDF report generated.")

        return str(filename)