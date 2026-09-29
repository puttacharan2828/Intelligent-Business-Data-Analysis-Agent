class AnalysisPlan:
    def __init__(
        self,
        analysis_type,
        target_column=None,
        group_by=None,
        operation=None,
        filter=None,
        time=None
    ):
        self.analysis_type = analysis_type
        self.target_column = target_column
        self.group_by = group_by
        self.operation = operation
        self.filter = filter
        self.time = time

    def to_dict(self):
        return {
            "analysis_type": self.analysis_type,
            "target_column": self.target_column,
            "group_by": self.group_by,
            "operation": self.operation,
            "filter": self.filter,
            "time": self.time
        }