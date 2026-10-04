from .conversation_memory import ConversationMemory
from .followup_detector import FollowUpDetector
from .context_resolver import ContextResolver

class ConversationContext:

    def __init__(self, memory):
        self.memory = memory
        self.detector = FollowUpDetector()
        self.resolver = ContextResolver()

    def resolve_question(self, question):

        previous_question = self.memory.get_previous_question()

        is_follow_up = self.detector.is_follow_up(
            question,
            previous_question
        )

        if is_follow_up:
            resolved_question = self.resolver.resolve(
                question,
                previous_question
            )

            return {
                "is_follow_up": True,
                "original_question": question,
                "resolved_question": resolved_question,
                "previous_question": previous_question
            }

        return {
            "is_follow_up": False,
            "original_question": question,
            "resolved_question": question,
            "previous_question": previous_question
        }