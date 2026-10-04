class ContextResolver:

    def resolve(self, question, previous_question):

        if previous_question is None:
            return question

        question = question.strip()
        previous_question = previous_question.strip()

        lower_question = question.lower()

        if lower_question.startswith("what about "):
            new_value = question[11:].strip().rstrip("?")
            return self._replace_metric(previous_question, new_value)

        if lower_question.startswith("how about "):
            new_value = question[10:].strip().rstrip("?")
            return self._replace_metric(previous_question, new_value)

        if lower_question.startswith("and "):
            new_value = question[4:].strip().rstrip("?")
            return self._replace_metric(previous_question, new_value)

        if lower_question.startswith("also "):
            new_value = question[5:].strip().rstrip("?")
            return self._replace_metric(previous_question, new_value)

        return question

    def _replace_metric(self, previous_question, new_value):

        metric_words = [
            "sales",
            "quantity",
            "profit",
            "revenue",
            "cost"
        ]

        result = previous_question

        for metric in metric_words:

            if metric in result.lower():

                start = result.lower().find(metric)

                result = (
                    result[:start]
                    + new_value
                    + result[start + len(metric):]
                )

                return result

        return previous_question