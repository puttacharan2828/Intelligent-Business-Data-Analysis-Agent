class ConversationMemory:
    def __init__(self):
        self.history = []

    def add(
    self,
    question,
    result=None,
    interpretation=None,
    is_follow_up=False,
    original_question=None
):
        entry = {
            "question": question,
            "result": result,
            "interpretation": interpretation,
            "is_follow_up": is_follow_up,
            "original_question": original_question

        }

        self.history.append(entry)

    def get_last(self):
        if not self.history:
            return None

        return self.history[-1]

    def get_history(self):
        return self.history

    def get_previous_question(self):
        last = self.get_last()

        if last is None:
            return None

        return last["question"]

    def get_previous_result(self):
        last = self.get_last()

        if last is None:
            return None

        return last["result"]

    def get_previous_interpretation(self):
        last = self.get_last()

        if last is None:
            return None

        return last["interpretation"]

    def clear(self):
        self.history = []