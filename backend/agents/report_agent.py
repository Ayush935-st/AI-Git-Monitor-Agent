from datetime import datetime
from pathlib import Path
from html import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from backend.utils.logger import logger


class ReportAgent:

    def __init__(self):
        self.report_dir = Path("backend/reports")
        self.report_dir.mkdir(parents=True, exist_ok=True)

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------

    def _safe(self, value) -> str:
        """Convert values safely to text."""
        if value is None:
            return ""

        return escape(str(value))

    def _format_findings(self, findings: list) -> str:
        """Convert structured findings into readable Markdown."""

        if not findings:
            return "No deterministic findings detected."

        lines = []

        for finding in findings:

            if isinstance(finding, dict):

                finding_type = finding.get("type", "unknown")
                severity = finding.get("severity", "unknown")
                message = finding.get("message", "")
                count = finding.get("count")

                line = (
                    f"- **{finding_type}** "
                    f"({severity.upper()}): {message}"
                )

                if count is not None:
                    line += f" Count: {count}."

                lines.append(line)

            else:
                lines.append(f"- {finding}")

        return "\n".join(lines)

    # ---------------------------------------------------------
    # Markdown Report
    # ---------------------------------------------------------

    def generate_markdown(
        self,
        review: str,
        commit_hash: str,
        repository: str = "",
        changed_files: list[str] | None = None,
        code_analysis: dict | None = None,
        security_analysis: dict | None = None,
        risk_score: int | None = None,
    ) -> str:

        filename = self.report_dir / f"{commit_hash}.md"

        changed_files = changed_files or []
        code_analysis = code_analysis or {}
        security_analysis = security_analysis or {}

        risk_level = code_analysis.get(
            "risk_level",
            "UNKNOWN"
        )

        code_findings = code_analysis.get(
            "findings",
            []
        )

        security_findings = security_analysis.get(
            "findings",
            []
        )

        with open(filename, "w", encoding="utf-8") as file:

            file.write("# AI Git Monitoring Agent - Code Review\n\n")

            file.write(
                f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            )

            file.write("## Repository Information\n\n")

            file.write(f"- **Repository:** {repository}\n")
            file.write(f"- **Commit:** `{commit_hash}`\n")
            file.write(
                f"- **Changed Files:** {len(changed_files)}\n"
            )

            if changed_files:
                for changed_file in changed_files:
                    file.write(f"  - `{changed_file}`\n")

            file.write("\n")

            # -------------------------------------------------
            # Executive Summary
            # -------------------------------------------------

            file.write("## Executive Summary\n\n")

            file.write(
                "This section contains the AI-generated engineering "
                "assessment based on the Git diff and deterministic "
                "code and security analysis.\n\n"
            )

            file.write(review)

            file.write("\n\n")

            # -------------------------------------------------
            # Code Analysis
            # -------------------------------------------------

            file.write("## Code Analysis\n\n")

            file.write(
                f"- **Files Changed:** "
                f"{code_analysis.get('changed_file_count', 0)}\n"
            )

            file.write(
                f"- **Lines Added:** "
                f"{code_analysis.get('added_lines', 0)}\n"
            )

            file.write(
                f"- **Lines Removed:** "
                f"{code_analysis.get('removed_lines', 0)}\n"
            )

            file.write(
                f"- **Diff Size:** "
                f"{code_analysis.get('diff_size', 0)} characters\n"
            )

            file.write(
                f"- **Risk Level:** "
                f"{risk_level}\n\n"
            )

            file.write("### Code Findings\n\n")

            file.write(
                self._format_findings(code_findings)
            )

            file.write("\n\n")

            # -------------------------------------------------
            # Security Analysis
            # -------------------------------------------------

            file.write("## Security Analysis\n\n")

            file.write(
                f"Security findings detected: "
                f"**{security_analysis.get('finding_count', 0)}**\n\n"
            )

            file.write(
                self._format_findings(security_findings)
            )

            file.write("\n\n")

            # -------------------------------------------------
            # Risk Assessment
            # -------------------------------------------------

            file.write("## Risk Assessment\n\n")

            file.write(
                f"- **Risk Score:** "
                f"{risk_score if risk_score is not None else 'N/A'}/10\n"
            )

            file.write(
                f"- **Risk Level:** {risk_level}\n\n"
            )

            file.write(
                "The risk score is calculated from deterministic "
                "code and security findings. The AI review provides "
                "additional engineering interpretation of this risk.\n\n"
            )

            # -------------------------------------------------
            # Final Decision
            # -------------------------------------------------

            file.write("## Final AI Decision\n\n")

            file.write(
                "The final decision and engineering recommendations "
                "are generated by the LLM based on the supplied "
                "evidence.\n\n"
            )

            file.write(review)

        logger.info("Markdown report generated.")

        return str(filename)

    # ---------------------------------------------------------
    # PDF Report
    # ---------------------------------------------------------

    def generate_pdf(
        self,
        review: str,
        commit_hash: str,
        repository: str = "",
        changed_files: list[str] | None = None,
        code_analysis: dict | None = None,
        security_analysis: dict | None = None,
        risk_score: int | None = None,
    ) -> str:

        filename = self.report_dir / f"{commit_hash}.pdf"

        changed_files = changed_files or []
        code_analysis = code_analysis or {}
        security_analysis = security_analysis or {}

        risk_level = code_analysis.get(
            "risk_level",
            "UNKNOWN"
        )

        code_findings = code_analysis.get(
            "findings",
            []
        )

        security_findings = security_analysis.get(
            "findings",
            []
        )

        document = SimpleDocTemplate(
            str(filename),
            pagesize=A4,
            rightMargin=40,
            leftMargin=40,
            topMargin=40,
            bottomMargin=40,
        )

        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            "ReportTitle",
            parent=styles["Title"],
            alignment=TA_CENTER,
            fontSize=20,
            spaceAfter=15,
        )

        heading_style = ParagraphStyle(
            "ReportHeading",
            parent=styles["Heading2"],
            fontSize=14,
            spaceBefore=14,
            spaceAfter=8,
        )

        body_style = ParagraphStyle(
            "ReportBody",
            parent=styles["BodyText"],
            fontSize=9,
            leading=13,
            spaceAfter=7,
        )

        small_style = ParagraphStyle(
            "ReportSmall",
            parent=styles["BodyText"],
            fontSize=8,
            leading=11,
        )

        elements = []

        # -----------------------------------------------------
        # Title
        # -----------------------------------------------------

        elements.append(
            Paragraph(
                "AI Git Monitoring Agent",
                title_style,
            )
        )

        elements.append(
            Paragraph(
                "AI-Powered Code Review Report",
                styles["Heading2"],
            )
        )

        elements.append(Spacer(1, 10))

        elements.append(
            Paragraph(
                f"<b>Generated:</b> "
                f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                body_style,
            )
        )

        # -----------------------------------------------------
        # Repository Information
        # -----------------------------------------------------

        elements.append(
            Paragraph(
                "Repository Information",
                heading_style,
            )
        )

        repository_data = [
            [
                Paragraph("<b>Repository</b>", small_style),
                Paragraph(self._safe(repository), small_style),
            ],
            [
                Paragraph("<b>Commit</b>", small_style),
                Paragraph(self._safe(commit_hash), small_style),
            ],
            [
                Paragraph("<b>Changed Files</b>", small_style),
                Paragraph(str(len(changed_files)), small_style),
            ],
        ]

        repository_table = Table(
            repository_data,
            colWidths=[1.5 * inch, 5.2 * inch],
        )

        repository_table.setStyle(
            TableStyle([
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ])
        )

        elements.append(repository_table)

        # -----------------------------------------------------
        # Changed Files
        # -----------------------------------------------------

        elements.append(
            Paragraph(
                "Changed Files",
                heading_style,
            )
        )

        if changed_files:

            for changed_file in changed_files:

                elements.append(
                    Paragraph(
                        f"• {self._safe(changed_file)}",
                        body_style,
                    )
                )

        else:

            elements.append(
                Paragraph(
                    "No changed files supplied.",
                    body_style,
                )
            )

        # -----------------------------------------------------
        # Executive Summary
        # -----------------------------------------------------

        elements.append(
            Paragraph(
                "Executive Summary",
                heading_style,
            )
        )

        elements.append(
            Paragraph(
                "The following assessment was generated by the "
                "LLM using the Git diff together with deterministic "
                "code and security analysis.",
                body_style,
            )
        )

        self._add_review_to_pdf(
            elements,
            review,
            body_style,
            heading_style,
        )

        # -----------------------------------------------------
        # Code Analysis
        # -----------------------------------------------------

        elements.append(
            Paragraph(
                "Code Analysis",
                heading_style,
            )
        )

        code_data = [
            [
                Paragraph("<b>Metric</b>", small_style),
                Paragraph("<b>Value</b>", small_style),
            ],
            [
                Paragraph("Files Changed", small_style),
                Paragraph(
                    str(code_analysis.get("changed_file_count", 0)),
                    small_style,
                ),
            ],
            [
                Paragraph("Lines Added", small_style),
                Paragraph(
                    str(code_analysis.get("added_lines", 0)),
                    small_style,
                ),
            ],
            [
                Paragraph("Lines Removed", small_style),
                Paragraph(
                    str(code_analysis.get("removed_lines", 0)),
                    small_style,
                ),
            ],
            [
                Paragraph("Diff Size", small_style),
                Paragraph(
                    f"{code_analysis.get('diff_size', 0)} characters",
                    small_style,
                ),
            ],
            [
                Paragraph("Risk Level", small_style),
                Paragraph(
                    self._safe(risk_level),
                    small_style,
                ),
            ],
        ]

        code_table = Table(
            code_data,
            colWidths=[3.3 * inch, 3.4 * inch],
        )

        code_table.setStyle(
            TableStyle([
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ])
        )

        elements.append(code_table)

        elements.append(
            Paragraph(
                "Code Findings",
                heading_style,
            )
        )

        self._add_findings_to_pdf(
            elements,
            code_findings,
            body_style,
        )

        # -----------------------------------------------------
        # Security Analysis
        # -----------------------------------------------------

        elements.append(
            Paragraph(
                "Security Analysis",
                heading_style,
            )
        )

        elements.append(
            Paragraph(
                f"<b>Security Findings:</b> "
                f"{security_analysis.get('finding_count', 0)}",
                body_style,
            )
        )

        self._add_findings_to_pdf(
            elements,
            security_findings,
            body_style,
        )

        # -----------------------------------------------------
        # Risk Assessment
        # -----------------------------------------------------

        elements.append(
            Paragraph(
                "Risk Assessment",
                heading_style,
            )
        )

        elements.append(
            Paragraph(
                f"<b>Risk Score:</b> "
                f"{risk_score if risk_score is not None else 'N/A'}/10",
                body_style,
            )
        )

        elements.append(
            Paragraph(
                f"<b>Risk Level:</b> "
                f"{self._safe(risk_level)}",
                body_style,
            )
        )

        elements.append(
            Paragraph(
                "The score is calculated from deterministic findings, "
                "while the LLM provides contextual engineering judgment "
                "about the significance of those findings.",
                body_style,
            )
        )

        # -----------------------------------------------------
        # Final AI Review
        # -----------------------------------------------------

        elements.append(
            Paragraph(
                "AI Engineering Opinion",
                heading_style,
            )
        )

        self._add_review_to_pdf(
            elements,
            review,
            body_style,
            heading_style,
        )

        document.build(elements)

        logger.info("PDF report generated.")

        return str(filename)

    # ---------------------------------------------------------
    # PDF Review Parser
    # ---------------------------------------------------------

    def _add_review_to_pdf(
        self,
        elements,
        review: str,
        body_style,
        heading_style,
    ):

        sections = [
            "Engineering Assessment",
            "Code Quality",
            "Security Assessment",
            "Performance",
            "Maintainability",
            "Risk Assessment",
            "Recommendations",
            "Final Decision",
        ]

        current_section = None
        buffer = []

        def flush():

            if not buffer:
                return

            text = " ".join(buffer).strip()

            if text:
                text = text.replace(
                    "\n",
                    "<br/>"
                )

                elements.append(
                    Paragraph(
                        text,
                        body_style,
                    )
                )

            buffer.clear()

        for line in review.splitlines():

            clean_line = line.strip()

            if clean_line.startswith("## "):

                flush()

                heading = clean_line[3:].strip()

                if heading in sections:

                    current_section = heading

                    elements.append(
                        Paragraph(
                            self._safe(heading),
                            heading_style,
                        )
                    )

                continue

            if clean_line:

                buffer.append(clean_line)

        flush()

    # ---------------------------------------------------------
    # PDF Findings
    # ---------------------------------------------------------

    def _add_findings_to_pdf(
        self,
        elements,
        findings,
        body_style,
    ):

        if not findings:

            elements.append(
                Paragraph(
                    "No findings detected.",
                    body_style,
                )
            )

            return

        for finding in findings:

            if isinstance(finding, dict):

                finding_type = self._safe(
                    finding.get("type", "unknown")
                )

                severity = self._safe(
                    finding.get("severity", "unknown")
                ).upper()

                message = self._safe(
                    finding.get("message", "")
                )

                count = finding.get("count")

                text = (
                    f"<b>{finding_type}</b> "
                    f"[{severity}] — {message}"
                )

                if count is not None:
                    text += f" Count: {count}."

            else:

                text = self._safe(finding)

            elements.append(
                Paragraph(
                    f"• {text}",
                    body_style,
                )
            )