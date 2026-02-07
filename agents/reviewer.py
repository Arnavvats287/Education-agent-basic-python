class ReviewerAgent:
    """
    Responsibility:
    Evaluate the Generator’s output.
    """

    def review(self, content_json: dict, grade: int) -> dict:
        feedback = []

        explanation = content_json["explanation"]
        mcqs = content_json["mcqs"]

        # Age rule
        if grade <= 4 and "vertex" in explanation.lower():
            feedback.append("The term 'vertex' is too advanced for this grade")

        # checkinmg
        if "acute angle" not in explanation.lower():
            feedback.append("Acute angle definition is missing")

        if "right angle" not in explanation.lower():
            feedback.append("Right angle definition is missing")

        if "obtuse angle" not in explanation.lower():
            feedback.append("Obtuse angle definition is missing")

        # mcq validation
        for i, question in enumerate(mcqs):
            if question["answer"] not in question["options"]:
                feedback.append(f"Question {i+1} has an invalid correct answer")

        status = "pass" if len(feedback) == 0 else "fail"

        return {
            "status": status,
            "feedback": feedback
        }
