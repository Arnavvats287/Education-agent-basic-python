class GeneratorAgent:
    """
    Responsibility:
    Generate draft educational content for a given grade and topic.
    """

    def generate(self, input_json: dict, feedback: list = None) -> dict:
        grade = input_json["grade"]
        topic = input_json["topic"]

        explanation = self._generate_explanation(grade, topic)

        # One refinement pass if feedback provided
        if feedback:
            explanation = self._refine_explanation(explanation, feedback)

        mcqs = self._generate_mcqs(topic)

        return {
            "explanation": explanation,
            "mcqs": mcqs
        }

    def _is_angle_topic(self, topic: str) -> bool:
        return "angle" in topic.lower().strip()

    def _generate_explanation(self, grade, topic):
        if not self._is_angle_topic(topic):
            return "Topic not supported."

        # INTENTIONAL to get a look at refinement through this ~
        if grade <= 4:
            return (
                "An angle is formed when two rays meet at a point called the vertex. "
                "An acute angle measures less than 90 degrees. "
                "A right angle measures exactly 90 degrees. "
                "An obtuse angle measures more than 90 degrees but less than 180 degrees."
            )
        else:
            return (
                "An angle is formed when two rays meet at a common point called the vertex. "
                "Angles are measured in degrees. "
                "An acute angle measures less than 90 degrees. "
                "A right angle measures exactly 90 degrees. "
                "An obtuse angle measures more than 90 degrees but less than 180 degrees. "
                "A straight angle measures exactly 180 degrees."
            )

    def _refine_explanation(self, explanation, feedback):
        for comment in feedback:
            if "too advanced" in comment.lower():
                explanation = explanation.replace(
                    "formed when two rays meet at a point called the vertex",
                    "made when two lines meet at a point"
                )
        return explanation

    def _generate_mcqs(self, topic):
        if not self._is_angle_topic(topic):
            return []
# the questions
        return [
            {
                "question": "Which angle is exactly 90 degrees?",
                "options": [
                    "Acute angle",
                    "Right angle",
                    "Obtuse angle",
                    "Straight angle"
                ],
                "answer": "Right angle"
            },
            {
                "question": "Which angle is less than 90 degrees?",
                "options": [
                    "Acute angle",
                    "Right angle",
                    "Obtuse angle",
                    "Straight angle"
                ],
                "answer": "Acute angle"
            }
        ]
