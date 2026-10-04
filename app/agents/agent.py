try:
    from .agent_state import AgentState
    from ..nlu.question_parser import parse_question
    from .planner import create_analysis_plan
    from .code_generator import generate_code
    from .code_validator import validate_code
    from ..analysis.executor import execute_code
    from ..visualization.visualizer import create_visualization
    from .interpreter import ResultInterpreter

except ImportError:
    from agents.agent_state import AgentState
    from nlu.question_parser import parse_question
    from agents.planner import create_analysis_plan
    from agents.code_generator import generate_code
    from agents.code_validator import validate_code
    from analysis.executor import execute_code
    from visualization.visualizer import create_visualization
    from agents.interpreter import ResultInterpreter

class AnalysisAgent:
    def __init__(self):
        self.state = AgentState()
        self.interpreter = ResultInterpreter()

    def reset(self):
        self.state = AgentState()

    def recover(self, execution):
        self.state.recovery_attempted = True

        if execution["error_type"] == "MissingResult":
            self.state.error = (
                "Analysis failed because the generated code "
                "did not produce a result."
            )
        elif execution["error_type"] == "KeyError":

            columns = self.state.dataset.columns.tolist()

            self.state.error = (
                "Analysis failed because the generated code "
                "used a column that does not exist. "
                f"Available columns: {', '.join(columns)}."
            )
        else:
            self.state.error = execution["error"]

        return False

    def run(self, question, dataset, columns):
        self.reset()

        self.state.question = question
        self.state.dataset = dataset

        self.state.nlu_result = parse_question(question, columns)

        self.state.analysis_plan = create_analysis_plan(
            self.state.nlu_result
        )

        try:
            self.state.generated_code = generate_code(
                self.state.analysis_plan.to_dict()
            )
        except Exception as e:
            self.state.error = str(e)
            self.state.error_type = "generation_error"
            self.state.recovery_attempted = True
            return self.state
        
        if not validate_code(self.state.generated_code):
            self.state.error = "Generated code failed validation."
            self.state.error_type = "validation_error"
            return self.state

        execution = execute_code(
            self.state.generated_code,
            self.state.dataset
        )

        self.state.execution_result = execution

        if not execution["success"]:
            self.state.error_type = "execution_error"
            self.state.specific_error_type = execution["error_type"]

            self.recover(execution)

            retry_execution = execute_code(
                self.state.generated_code,
                self.state.dataset
            )

            self.state.execution_result = retry_execution

            if not retry_execution["success"]:
                self.state.specific_error_type = retry_execution["error_type"]
                self.recover(retry_execution)
                return self.state

            execution = retry_execution
        
        self.state.interpretation = self.interpreter.interpret(
            execution["result"]
        )

        self.state.business_insight = (
            self.interpreter.combine_interpretation_and_insight(
                self.state.interpretation,
                self.interpreter.generate_business_insight(
                    self.state.interpretation,
                    self.state.analysis_plan.operation,
                    self.state.analysis_plan.target_column,
                    self.state.analysis_plan.analysis_type,
                    self.state.analysis_plan.group_by,
                    self.state.analysis_plan.filter
                )
            )
        )

        if self.state.analysis_plan.analysis_type == "grouped_aggregation":
            result = execution["result"]

            visualization_data = result.reset_index()

            self.state.visualization = create_visualization(
                visualization_data,
                "comparison",
                self.state.analysis_plan.group_by,
                self.state.analysis_plan.target_column
            )

        elif self.state.analysis_plan.analysis_type == "distribution":
            metric = self.state.analysis_plan.target_column

            visualization_data = self.state.dataset[[metric]]

            self.state.visualization = create_visualization(
                visualization_data,
                "distribution",
                y_column=metric
            )

        elif self.state.analysis_plan.analysis_type == "trend":
            result = execution["result"]

            visualization_data = result.reset_index()

            self.state.visualization = create_visualization(
                visualization_data,
                "trend",
                self.state.analysis_plan.time,
                self.state.analysis_plan.target_column
            )

        elif self.state.analysis_plan.analysis_type == "relationship":
            x_column = self.state.analysis_plan.group_by
            y_column = self.state.analysis_plan.target_column

            visualization_data = self.state.dataset[
                [x_column, y_column]
            ]

            self.state.visualization = create_visualization(
                visualization_data,
                "relationship",
                x_column,
                y_column
            )

        return self.state