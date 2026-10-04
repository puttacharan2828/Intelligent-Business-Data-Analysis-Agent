class FollowUpDetector:

    def is_follow_up(self, question, previous_question=None):

        if previous_question is None:
            return False

        question = question.strip().lower()
        previous_question = previous_question.strip().lower()

        if not question:
            return False

        follow_up_phrases = [
            "what about",
            "how about",
            "and what about",
            "and how about",
            "show me also",
            "show also",
            "and quantity",
            "and sales",
            "and profit",
            "what about the",
            "how about the"
        ]

        for phrase in follow_up_phrases:
            if question.startswith(phrase):
                return True

        # Short questions are often follow-ups when they
        # refer directly to the previous analysis.
        if len(question.split()) <= 4:
            if question.startswith(("and ", "also ", "what about ", "how about ")):
                return True

        return False