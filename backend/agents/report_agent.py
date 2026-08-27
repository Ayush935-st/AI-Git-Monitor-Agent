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
    """
    Generates structured Markdown and PDF reports from:

    - Deterministic code analysis
    - Deterministic security analysis
    - Calculated risk score
    - LLM-generated engineering review
    """

    def __init__(self):
        self.report_dir = Path("backend/reports")
        self.report_dir.mkdir(parents=True, exist_ok=True)

    # =========================================================
    # Helpers
    # =========================================================

    def _safe(self, value) -> str:
        """Convert a value to HTML-safe text."""

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
                    f"({str(severity).upper()}): {message}"
                )

                if count is not None:
                    line += f" Count: {count}."

                lines.append(line)

            else:
                lines.append(f"- {finding}")

        return "\n".join(lines)

    def _extract_review_sections(self, review: str) -> dict:
        """
        Extract structured sections from the LLM review.

        Expected headings:

        ## Engineering Assessment
        ## Code Quality
        ## Security Assessment
        ## Performance
        ## Maintainability
        ## Risk Assessment
        ## Recommendations
        ## Final Decision
        """

        expected_sections = [
            "Engineering Assessment",
            "Code Quality",
            "Security Assessment",
            "Performance",
            "Maintainability",
            "Risk Assessment",
            "Recommendations",
            "Final Decision",
        ]

        sections = {
            section: ""
            for section in expected_sections
        }

        current_section = None
        buffer = []

        def save_current():
            nonlocal buffer

            if current_section in sections:
                text = " ".join(buffer).strip()

                if text:
                    sections[current_section] = text

            buffer = []

        for line in review.splitlines():

            clean_line = line.strip()

            if clean_line.startswith("## "):

                save_current()

                heading = clean_line[3:].strip()

                if heading in sections:
                    current_section = heading
                else:
                    current_section = None

                continue

            if current_section and clean_line:
                buffer.append(clean_line)

        save_current()

        return sections

    # =========================================================
    # Markdown Report
    # =========================================================

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
            "UNKNOWN",
        )

        code_findings = code_analysis.get(
            "findings",
            [],
        )

        security_findings = security_analysis.get(
            "findings",
            [],
        )

        review_sections = self._extract_review_sections(review)

        engineering_assessment = review_sections.get(
            "Engineering Assessment",
            "",
        )

        code_quality = review_sections.get(
            "Code Quality",
            "",
        )

        security_assessment = review_sections.get(
            "Security Assessment",
            "",
        )

        performance = review_sections.get(
            "Performance",
            "",
        )

        maintainability = review_sections.get(
            "Maintainability",
            "",
        )

        ai_risk_assessment = review_sections.get(
            "Risk Assessment",
            "",
        )

        recommendations = review_sections.get(
            "Recommendations",
            "",
        )

        final_decision = review_sections.get(
            "Final Decision",
            "",
        )

        with open(filename, "w", encoding="utf-8") as file:

            file.write(
                "# AI Git Monitoring Agent - Code Review Report\n\n"
            )

            file.write(
                f"**Generated:** "
                f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            )

            # -------------------------------------------------
            # Repository Information
            # -------------------------------------------------

            file.write("## Repository Information\n\n")

            file.write(
                f"- **Repository:** {repository}\n"
            )

            file.write(
                f"- **Commit:** `{commit_hash}`\n"
            )

            file.write(
                f"- **Changed Files:** {len(changed_files)}\n"
            )

            for changed_file in changed_files:
                file.write(
                    f"  - `{changed_file}`\n"
                )

            file.write("\n")

            # -------------------------------------------------
            # Executive Summary
            # -------------------------------------------------

            file.write("## Executive Summary\n\n")

            file.write(
                "This report combines deterministic analysis with "
                "an independent AI engineering assessment. "
                "Deterministic scanners provide evidence-based "
                "findings, while the LLM interprets the change "
                "in its engineering context.\n\n"
            )

            if engineering_assessment:
                file.write(
                    f"**AI Engineering Assessment:**\n\n"
                    f"{engineering_assessment}\n\n"
                )
            else:
                file.write(
                    "No structured Engineering Assessment was "
                    "returned by the LLM.\n\n"
                )

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
                f"- **Risk Level:** {risk_level}\n\n"
            )

            file.write("### Deterministic Code Findings\n\n")

            file.write(
                self._format_findings(code_findings)
            )

            file.write("\n\n")

            if code_quality:
                file.write("### AI Code Quality Opinion\n\n")
                file.write(
                    f"{code_quality}\n\n"
                )

            # -------------------------------------------------
            # Security Analysis
            # -------------------------------------------------

            file.write("## Security Analysis\n\n")

            file.write(
                f"**Security Findings:** "
                f"{security_analysis.get('finding_count', 0)}\n\n"
            )

            file.write(
                self._format_findings(security_findings)
            )

            file.write("\n\n")

            if security_assessment:
                file.write(
                    "### AI Security Assessment\n\n"
                )

                file.write(
                    f"{security_assessment}\n\n"
                )

            # -------------------------------------------------
            # Performance
            # -------------------------------------------------

            if performance:

                file.write("## Performance\n\n")

                file.write(
                    f"{performance}\n\n"
                )

            # -------------------------------------------------
            # Maintainability
            # -------------------------------------------------

            if maintainability:

                file.write("## Maintainability\n\n")

                file.write(
                    f"{maintainability}\n\n"
                )

            # -------------------------------------------------
            # Risk Assessment
            # -------------------------------------------------

            file.write("## Risk Assessment\n\n")

            file.write(
                f"- **Deterministic Risk Score:** "
                f"{risk_score if risk_score is not None else 'N/A'}/10\n"
            )

            file.write(
                f"- **Deterministic Risk Level:** "
                f"{risk_level}\n\n"
            )

            file.write(
                "The deterministic risk score is calculated from "
                "the evidence produced by the analysis pipeline. "
                "The AI does not replace this calculation; instead, "
                "it provides contextual engineering judgment about "
                "whether the calculated risk is appropriate.\n\n"
            )

            if ai_risk_assessment:

                file.write(
                    "### AI Risk Interpretation\n\n"
                )

                file.write(
                    f"{ai_risk_assessment}\n\n"
                )

            # -------------------------------------------------
            # Recommendations
            # -------------------------------------------------

            if recommendations:

                file.write("## Recommendations\n\n")

                file.write(
                    f"{recommendations}\n\n"
                )

            # -------------------------------------------------
            # Final Decision
            # -------------------------------------------------

            file.write("## Final Decision\n\n")

            if final_decision:

                file.write(
                    f"{final_decision}\n\n"
                )

            else:

                file.write(
                    "No structured final decision was returned "
                    "by the LLM.\n\n"
                )

            # -------------------------------------------------
            # Complete AI Review
            # -------------------------------------------------

            file.write(
                "## Complete AI Review\n\n"
            )

            file.write(review)

        logger.info("Markdown report generated.")

        return str(filename)

    # =========================================================
    # PDF Report
    # =========================================================

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
            "UNKNOWN",
        )

        code_findings = code_analysis.get(
            "findings",
            [],
        )

        security_findings = security_analysis.get(
            "findings",
            [],
        )

        review_sections = self._extract_review_sections(review)

        engineering_assessment = review_sections.get(
            "Engineering Assessment",
            "",
        )

        code_quality = review_sections.get(
            "Code Quality",
            "",
        )

        security_assessment = review_sections.get(
            "Security Assessment",
            "",
        )

        performance = review_sections.get(
            "Performance",
            "",
        )

        maintainability = review_sections.get(
            "Maintainability",
            "",
        )

        ai_risk_assessment = review_sections.get(
            "Risk Assessment",
            "",
        )

        recommendations = review_sections.get(
            "Recommendations",
            "",
        )

        final_decision = review_sections.get(
            "Final Decision",
            "",
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
            spaceAfter=10,
        )

        subtitle_style = ParagraphStyle(
            "ReportSubtitle",
            parent=styles["Heading2"],
            alignment=TA_CENTER,
            fontSize=12,
            spaceAfter=15,
        )

        heading_style = ParagraphStyle(
            "ReportHeading",
            parent=styles["Heading2"],
            fontSize=14,
            spaceBefore=16,
            spaceAfter=8,
        )

        subheading_style = ParagraphStyle(
            "ReportSubHeading",
            parent=styles["Heading3"],
            fontSize=11,
            spaceBefore=10,
            spaceAfter=6,
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

        decision_style = ParagraphStyle(
            "DecisionStyle",
            parent=styles["BodyText"],
            fontSize=11,
            leading=15,
            spaceAfter=8,
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
                subtitle_style,
            )
        )

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
                Paragraph(
                    self._safe(repository),
                    small_style,
                ),
            ],
            [
                Paragraph("<b>Commit</b>", small_style),
                Paragraph(
                    self._safe(commit_hash),
                    small_style,
                ),
            ],
            [
                Paragraph("<b>Changed Files</b>", small_style),
                Paragraph(
                    str(len(changed_files)),
                    small_style,
                ),
            ],
        ]

        repository_table = Table(
            repository_data,
            colWidths=[1.5 * inch, 5.2 * inch],
        )

        repository_table.setStyle(
            TableStyle(
                [
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        colors.grey,
                    ),
                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "TOP",
                    ),
                    (
                        "BACKGROUND",
                        (0, 0),
                        (0, -1),
                        colors.lightgrey,
                    ),
                    (
                        "LEFTPADDING",
                        (0, 0),
                        (-1, -1),
                        6,
                    ),
                    (
                        "RIGHTPADDING",
                        (0, 0),
                        (-1, -1),
                        6,
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        5,
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        5,
                    ),
                ]
            )
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
                "This assessment combines deterministic evidence "
                "from the code and security scanners with an "
                "independent AI engineering interpretation. "
                "The deterministic scanners establish concrete "
                "findings, while the LLM evaluates their practical "
                "engineering significance.",
                body_style,
            )
        )

        if engineering_assessment:

            elements.append(
                Paragraph(
                    "<b>AI Engineering Assessment</b>",
                    subheading_style,
                )
            )

            elements.append(
                Paragraph(
                    self._safe(engineering_assessment),
                    body_style,
                )
            )

        else:

            elements.append(
                Paragraph(
                    "No structured Engineering Assessment was "
                    "returned by the LLM.",
                    body_style,
                )
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
                    str(
                        code_analysis.get(
                            "changed_file_count",
                            0,
                        )
                    ),
                    small_style,
                ),
            ],
            [
                Paragraph("Lines Added", small_style),
                Paragraph(
                    str(
                        code_analysis.get(
                            "added_lines",
                            0,
                        )
                    ),
                    small_style,
                ),
            ],
            [
                Paragraph("Lines Removed", small_style),
                Paragraph(
                    str(
                        code_analysis.get(
                            "removed_lines",
                            0,
                        )
                    ),
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
            TableStyle(
                [
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        colors.grey,
                    ),
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.lightgrey,
                    ),
                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "TOP",
                    ),
                    (
                        "LEFTPADDING",
                        (0, 0),
                        (-1, -1),
                        6,
                    ),
                    (
                        "RIGHTPADDING",
                        (0, 0),
                        (-1, -1),
                        6,
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        5,
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        5,
                    ),
                ]
            )
        )

        elements.append(code_table)

        elements.append(
            Paragraph(
                "Deterministic Code Findings",
                subheading_style,
            )
        )

        self._add_findings_to_pdf(
            elements,
            code_findings,
            body_style,
        )

        if code_quality:

            elements.append(
                Paragraph(
                    "AI Code Quality Opinion",
                    subheading_style,
                )
            )

            elements.append(
                Paragraph(
                    self._safe(code_quality),
                    body_style,
                )
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

        if security_assessment:

            elements.append(
                Paragraph(
                    "AI Security Assessment",
                    subheading_style,
                )
            )

            elements.append(
                Paragraph(
                    self._safe(security_assessment),
                    body_style,
                )
            )

        # -----------------------------------------------------
        # Performance
        # -----------------------------------------------------

        if performance:

            elements.append(
                Paragraph(
                    "Performance",
                    heading_style,
                )
            )

            elements.append(
                Paragraph(
                    self._safe(performance),
                    body_style,
                )
            )

        # -----------------------------------------------------
        # Maintainability
        # -----------------------------------------------------

        if maintainability:

            elements.append(
                Paragraph(
                    "Maintainability",
                    heading_style,
                )
            )

            elements.append(
                Paragraph(
                    self._safe(maintainability),
                    body_style,
                )
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

        risk_data = [
            [
                Paragraph(
                    "<b>Assessment</b>",
                    small_style,
                ),
                Paragraph(
                    "<b>Result</b>",
                    small_style,
                ),
            ],
            [
                Paragraph(
                    "Deterministic Risk Score",
                    small_style,
                ),
                Paragraph(
                    f"{risk_score if risk_score is not None else 'N/A'}/10",
                    small_style,
                ),
            ],
            [
                Paragraph(
                    "Deterministic Risk Level",
                    small_style,
                ),
                Paragraph(
                    self._safe(risk_level),
                    small_style,
                ),
            ],
        ]

        risk_table = Table(
            risk_data,
            colWidths=[3.3 * inch, 3.4 * inch],
        )

        risk_table.setStyle(
            TableStyle(
                [
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        colors.grey,
                    ),
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.lightgrey,
                    ),
                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "TOP",
                    ),
                    (
                        "LEFTPADDING",
                        (0, 0),
                        (-1, -1),
                        6,
                    ),
                    (
                        "RIGHTPADDING",
                        (0, 0),
                        (-1, -1),
                        6,
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        5,
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        5,
                    ),
                ]
            )
        )

        elements.append(risk_table)

        elements.append(Spacer(1, 6))

        elements.append(
            Paragraph(
                "The risk score is produced from deterministic "
                "analysis. The AI review provides contextual "
                "judgment about whether that risk level is "
                "appropriate given the actual change.",
                body_style,
            )
        )

        if ai_risk_assessment:

            elements.append(
                Paragraph(
                    "AI Risk Interpretation",
                    subheading_style,
                )
            )

            elements.append(
                Paragraph(
                    self._safe(ai_risk_assessment),
                    body_style,
                )
            )

        # -----------------------------------------------------
        # Recommendations
        # -----------------------------------------------------

        if recommendations:

            elements.append(
                Paragraph(
                    "Recommendations",
                    heading_style,
                )
            )

            elements.append(
                Paragraph(
                    self._safe(recommendations),
                    body_style,
                )
            )

        # -----------------------------------------------------
        # Final Decision
        # -----------------------------------------------------

        elements.append(
            Paragraph(
                "Final Decision",
                heading_style,
            )
        )

        if final_decision:

            elements.append(
                Paragraph(
                    self._safe(final_decision),
                    decision_style,
                )
            )

        else:

            elements.append(
                Paragraph(
                    "No structured final decision was returned "
                    "by the LLM.",
                    body_style,
                )
            )

        # -----------------------------------------------------
        # Complete AI Review
        # -----------------------------------------------------

        elements.append(
            Paragraph(
                "Complete AI Review",
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

    # =========================================================
    # PDF Review Parser
    # =========================================================

    def _add_review_to_pdf(
        self,
        elements,
        review: str,
        body_style,
        heading_style,
    ):
        """
        Render the structured LLM review into the PDF.
        """

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

                elements.append(
                    Paragraph(
                        self._safe(text),
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

                else:

                    current_section = None

                continue

            if current_section and clean_line:

                buffer.append(clean_line)

        flush()

    # =========================================================
    # PDF Findings
    # =========================================================

    def _add_findings_to_pdf(
        self,
        elements,
        findings,
        body_style,
    ):
        """
        Render deterministic findings into the PDF.
        """

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
                    finding.get(
                        "type",
                        "unknown",
                    )
                )

                severity = self._safe(
                    finding.get(
                        "severity",
                        "unknown",
                    )
                ).upper()

                message = self._safe(
                    finding.get(
                        "message",
                        "",
                    )
                )

                count = finding.get("count")

                text = (
                    f"<b>{finding_type}</b> "
                    f"[{severity}] — {message}"
                )

                if count is not None:

                    text += (
                        f" Count: {count}."
                    )

            else:

                text = self._safe(finding)

            elements.append(
                Paragraph(
                    f"• {text}",
                    body_style,
                )
            )