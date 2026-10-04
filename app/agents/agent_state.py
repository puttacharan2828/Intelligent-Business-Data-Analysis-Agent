class AgentState:
    def __init__(self):
        self.question = None
        self.dataset = None

        self.nlu_result = None
        self.analysis_plan = None

        self.generated_code = None
        self.execution_result = None

        self.visualization = None
        self.interpretation = None
        self.business_insight = None

        self.error = None
        self.recovery_attempted = False