from io import BytesIO

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    ListFlowable,
    ListItem
)


class InterviewPreparationPDFService:

    def generate_pdf(
        self,
        interview_mode: str,
        difficulty: str,
        questions: list
    ):

        buffer = BytesIO()

        doc = SimpleDocTemplate(

            buffer,

            rightMargin=0.6 * inch,
            leftMargin=0.6 * inch,
            topMargin=0.6 * inch,
            bottomMargin=0.6 * inch

        )

        styles = getSampleStyleSheet()

        story = []

        # ==========================================
        # Title
        # ==========================================

        story.append(
            Paragraph(
                "<b>CareerPrep</b>",
                styles["Title"]
            )
        )

        story.append(
            Paragraph(
                "AI Interview Preparation Guide",
                styles["Heading1"]
            )
        )

        story.append(Spacer(1, 20))

        story.append(
            Paragraph(
                f"<b>Interview Mode:</b> {interview_mode}",
                styles["Normal"]
            )
        )

        story.append(
            Paragraph(
                f"<b>Difficulty:</b> {difficulty}",
                styles["Normal"]
            )
        )

        story.append(
            Paragraph(
                f"<b>Total Questions:</b> {len(questions)}",
                styles["Normal"]
            )
        )

        story.append(Spacer(1, 25))

        # ==========================================
        # Questions
        # ==========================================

        for index, question in enumerate(questions, start=1):

            story.append(

                Paragraph(

                    f"<b>Question {index}</b>",

                    styles["Heading2"]

                )

            )

            story.append(

                Paragraph(

                    f"<b>Category:</b> {question.category}",

                    styles["Normal"]

                )

            )

            story.append(

                Paragraph(

                    f"<b>Difficulty:</b> {question.difficulty}",

                    styles["Normal"]

                )

            )

            story.append(Spacer(1, 8))

            story.append(

                Paragraph(

                    f"<b>Question</b><br/>{question.question}",

                    styles["BodyText"]

                )

            )

            story.append(Spacer(1, 8))

            story.append(

                Paragraph(

                    f"<b>Interviewer's Intent</b><br/>{question.interviewer_intent}",

                    styles["BodyText"]

                )

            )

            story.append(Spacer(1, 8))

            story.append(

                Paragraph(

                    f"<b>Candidate Answer</b><br/>{question.candidate_answer}",

                    styles["BodyText"]

                )

            )

            story.append(Spacer(1, 8))

            story.append(

                Paragraph(

                    "<b>Key Points</b>",

                    styles["Heading3"]

                )

            )

            story.append(

                ListFlowable(

                    [

                        ListItem(

                            Paragraph(point, styles["BodyText"])

                        )

                        for point in question.key_points

                    ],

                    bulletType="bullet"

                )

            )

            story.append(Spacer(1, 8))

            story.append(

                Paragraph(

                    "<b>Common Mistakes</b>",

                    styles["Heading3"]

                )

            )

            story.append(

                ListFlowable(

                    [

                        ListItem(

                            Paragraph(point, styles["BodyText"])

                        )

                        for point in question.common_mistakes

                    ],

                    bulletType="bullet"

                )

            )

            story.append(Spacer(1, 24))

        doc.build(story)

        pdf = buffer.getvalue()

        buffer.close()

        return pdf