class ResultInterpreter:
    """Converts analysis results into human-readable explanations."""

    def interpret(self, result, operation=None, target_column=None):
        """Interpret an analysis result."""

        if result is None:
            return "No result was produced."

        if operation == "sum":
            return f"The total {target_column} is {result:,.2f}."

        elif operation == "mean":
            return f"The average {target_column} is {result:,.2f}."

        elif operation == "min":
            return f"The minimum {target_column} is {result:,.2f}."

        elif operation == "max":
            return f"The maximum {target_column} is {result:,.2f}."

        elif operation == "count":
            return f"The number of {target_column} records is {result}."

        elif operation == "describe":
            return (
                f"The {target_column} distribution contains "
                f"{result['count']:.0f} records, with an average of "
                f"{result['mean']:,.2f}. Values range from "
                f"{result['min']:,.2f} to {result['max']:,.2f}."
            )

        return f"Analysis result: {result}"

    def interpret_from_plan(self, result, plan):
        """Interpret a result using the analysis plan."""

        if plan.get("analysis_type") == "trend":
            return self.interpret_trend(
                result,
                plan.get("target_column")
            )

        if plan.get("analysis_type") == "distribution":
            return (
                f"The {plan.get('target_column')} distribution contains "
                f"{result['count']:.0f} records, with an average of "
                f"{result['mean']:,.2f}. Values range from "
                f"{result['min']:,.2f} to {result['max']:,.2f}."
            )

        if plan.get("analysis_type") == "summary":
            return (
                f"The {plan.get('target_column')} summary contains "
                f"{result['count']:.0f} records, with an average of "
                f"{result['mean']:,.2f}. The minimum value is "
                f"{result['min']:,.2f}, while the maximum value is "
                f"{result['max']:,.2f}."
            )

        if plan.get("analysis_type") == "relationship":
            column1 = plan.get("target_column")
            column2 = plan.get("group_by")

            correlation = result.loc[column1, column2]

            if correlation == 1:
                strength = "a perfect positive"
            elif correlation >= 0.7:
                strength = "a strong positive"
            elif correlation >= 0.3:
                strength = "a moderate positive"
            elif correlation > -0.3:
                strength = "a weak"
            elif correlation > -0.7:
                strength = "a moderate negative"
            else:
                strength = "a strong negative"

            return (
                f"{column1} and {column2} have {strength} "
                f"correlation of {correlation:.2f}."
            )

        return self.interpret(
            result,
            plan.get("operation"),
            plan.get("target_column")
        )

    def interpret_grouped(self, result, operation, group_by, target_column):
        """Interpret a grouped analysis result."""

        if result is None or result.empty:
            return "No grouped result was produced."

        if not all(
            isinstance(value, (int, float))
            for value in result.tolist()
        ):
            return (
                "Unable to interpret the grouped result because "
                "it contains non-numeric values."
            )

        # Handle result with only one group
        if len(result) == 1:

            group = result.index[0]
            value = result.iloc[0]

            if operation == "sum":
                return (
                    f"{group} has total {target_column} "
                    f"of {value:,.2f}."
                )

            elif operation == "mean":
                return (
                    f"{group} has an average {target_column} "
                    f"of {value:,.2f}."
                )

            elif operation == "min":
                return (
                    f"{group} has a minimum {target_column} "
                    f"of {value:,.2f}."
                )

            elif operation == "max":
                return (
                    f"{group} has a maximum {target_column} "
                    f"of {value:,.2f}."
                )

            elif operation == "count":
                return (
                    f"{group} has {value:.0f} "
                    f"{target_column} records."
                )

        # Handle multiple groups
        if operation in ["sum", "mean", "min", "max", "count"]:

            highest_group = result.idxmax()
            highest_value = result.max()

            lowest_group = result.idxmin()
            lowest_value = result.min()

        if operation == "sum":
            return (
                f"{highest_group} has the highest {target_column} "
                f"with {highest_value:,.2f}."
            )

        elif operation == "mean":
            return (
                f"{highest_group} has the highest average "
                f"{target_column} with {highest_value:,.2f}."
            )

        elif operation == "min":
            return (
                f"{lowest_group} has the lowest {target_column} "
                f"with {lowest_value:,.2f}."
            )

        elif operation == "max":
            return (
                f"{highest_group} has the highest {target_column} "
                f"with {highest_value:,.2f}."
            )

        elif operation == "count":
            return (
                f"{highest_group} has the highest number of "
                f"{target_column} records with {highest_value}."
            )

        return f"Analysis result: {result}"

    def interpret_trend(self, result, target_column):
        """Interpret a time-based result."""

        if result is None or result.empty:
            return "No trend result was produced."

        values = result.tolist()

        if not all(
            isinstance(value, (int, float))
            for value in values
        ):
            return (
                "Unable to interpret the trend because "
                "the result contains non-numeric values."
            )

        increasing = all(
            values[i] <= values[i + 1]
            for i in range(len(values) - 1)
        )

        decreasing = all(
            values[i] >= values[i + 1]
            for i in range(len(values) - 1)
        )

        if increasing and not decreasing:
            return (
                f"{target_column} shows an increasing trend, "
                f"rising from {values[0]:,.2f} to {values[-1]:,.2f}."
            )

        elif decreasing and not increasing:
            return (
                f"{target_column} shows a decreasing trend, "
                f"falling from {values[0]:,.2f} to {values[-1]:,.2f}."
            )

        elif increasing and decreasing:
            return (
                f"{target_column} remains stable at "
                f"{values[0]:,.2f}."
            )

        return (
            f"{target_column} shows a fluctuating trend."
        )

    def interpret_relationship(self, result, column1, column2):
        """Interpret the correlation between two columns."""

        if result is None or result.empty:
            return "No relationship result was produced."

        if column1 not in result.index or column2 not in result.columns:
            return (
                f"Unable to interpret the relationship between "
                f"{column1} and {column2}."
            )

        correlation = result.loc[column1, column2]

        if correlation >= 0.7:
            strength = "strong positive"
        elif correlation >= 0.3:
            strength = "moderate positive"
        elif correlation > -0.3:
            strength = "weak or no"
        elif correlation > -0.7:
            strength = "moderate negative"
        else:
            strength = "strong negative"

        return (
            f"{column1} and {column2} have a {strength} relationship "
            f"with a correlation of {correlation:.2f}."
        )

    def interpret_visualization(self, result, chart_type, target_column):
        """Interpret a visualization result."""

        if result is None:
            return "No visualization result was produced."

        if chart_type == "bar":

            if hasattr(result, "empty") and result.empty:
                return "No bar chart result was produced."

            highest_category = result.idxmax()
            highest_value = result.max()

            lowest_category = result.idxmin()
            lowest_value = result.min()

            return (
                f"{highest_category} has the highest {target_column} "
                f"with {highest_value:,.2f}, while "
                f"{lowest_category} has the lowest {target_column} "
                f"with {lowest_value:,.2f}."
            )

        elif chart_type == "histogram":

            if hasattr(result, "empty") and result.empty:
                return "No histogram result was produced."

            if not all(
                isinstance(value, (int, float))
                for value in result.tolist()
            ):
                return (
                    "Unable to interpret the histogram because "
                    "the result contains non-numeric values."
                )

            minimum = result.min()
            maximum = result.max()
            spread = maximum - minimum

            if spread == 0:
                return (
                    f"The {target_column} values are all the same at "
                    f"{minimum:,.2f}."
                )

            return (
                f"The {target_column} values range from "
                f"{minimum:,.2f} to {maximum:,.2f}, "
                f"with a spread of {spread:,.2f}."
            )

        elif chart_type == "scatter":
            return self.interpret_relationship(
                result,
                target_column,
                "Profit"
            )

        return f"The visualization displays {target_column}."

    def generate_business_insight(
        self,
        interpretation,
        operation=None,
        target_column=None,
        analysis_type=None,
        group_by=None,
        filter_data=None
    ):
        """Generate a simple business insight."""

        if interpretation is None or interpretation == "":
            return "No business insight could be generated."

        if filter_data and operation in ["sum", "mean", "min", "max", "count"]:
            filter_column = filter_data.get("column")
            filter_value = filter_data.get("value")

            if operation == "sum":
                return (
                    f"The {filter_value} {filter_column} has total "
                    f"{target_column} of {interpretation.split()[-1]}"
                )

            elif operation == "mean":
                return (
                    f"The {filter_value} {filter_column} has an average "
                    f"{target_column} of {interpretation.split()[-1]}"
                )

            elif operation == "min":
                return (
                    f"The {filter_value} {filter_column} has the lowest "
                    f"{target_column} value of {interpretation.split()[-1]}"
                )

            elif operation == "max":
                return (
                    f"The {filter_value} {filter_column} has the highest "
                    f"{target_column} value of {interpretation.split()[-1]}"
                )

            elif operation == "count":
                count = interpretation.split()[-1].rstrip(".")

                return (
                    f"The {filter_value} {filter_column} contains "
                    f"{count} {target_column} records."
                )

        if operation == "sum":

            if group_by:
                return (
                    f"The analysis shows the total {target_column} "
                    f"for each {group_by}."
                )

            return (
                f"The analysis shows the total {target_column} "
                f"for the available data."
            )

        elif operation == "mean":
            return (
                f"The analysis shows the average {target_column} "
                f"across the available records."
            )

        elif operation == "min":
            return (
                f"The analysis identifies the lowest {target_column} "
                f"value in the data."
            )

        elif operation == "max":
            return (
                f"The analysis identifies the highest {target_column} "
                f"value in the data."
            )

        elif operation == "count":
            return (
                f"The analysis shows the number of records "
                f"available for {target_column}."
            )

        if analysis_type == "relationship":
            return (
                f"The analysis examines the relationship between "
                f"{target_column} and {group_by}."
            )

        return f"Business insight: {interpretation}"

    def generate_grouped_insight(
        self,
        result,
        operation,
        group_by,
        target_column
    ):
        """Generate a business insight from grouped results."""

        if result is None or result.empty:
            return "No grouped business insight could be generated."

        # Handle result with only one group
        if len(result) == 1:

            group = result.index[0]
            value = result.iloc[0]

            if operation == "sum":
                return (
                    f"The filtered result contains only one {group_by}: "
                    f"{group}, with total {target_column} of "
                    f"{value:,.2f}."
                )

            elif operation == "mean":
                return (
                    f"The filtered result contains only one {group_by}: "
                    f"{group}, with an average {target_column} of "
                    f"{value:,.2f}."
                )

            elif operation == "min":
                return (
                    f"The filtered result contains only one {group_by}: "
                    f"{group}, with a minimum {target_column} of "
                    f"{value:,.2f}."
                )

            elif operation == "max":
                return (
                    f"The filtered result contains only one {group_by}: "
                    f"{group}, with a maximum {target_column} of "
                    f"{value:,.2f}."
                )

            elif operation == "count":
                return (
                    f"The filtered result contains only one {group_by}: "
                    f"{group}, with {value:.0f} "
                    f"{target_column} records."
                )

        # Handle multiple groups
        highest_group = result.idxmax()
        lowest_group = result.idxmin()

        if operation in ["sum", "mean", "max", "count"]:
            return (
                f"{highest_group} is the strongest-performing "
                f"{group_by} based on {target_column}, while "
                f"{lowest_group} has the lowest value."
            )

        elif operation == "min":
            return (
                f"{lowest_group} has the lowest {target_column} "
                f"value among the {group_by} categories."
            )

        return "No grouped business insight could be generated."

    def generate_trend_insight(self, result, target_column):
        """Generate a business insight from a trend result."""

        if result is None or result.empty:
            return "No trend business insight could be generated."

        values = result.tolist()

        increasing = all(
            values[i] <= values[i + 1]
            for i in range(len(values) - 1)
        )

        decreasing = all(
            values[i] >= values[i + 1]
            for i in range(len(values) - 1)
        )

        if increasing and not decreasing:
            return (
                f"{target_column} is showing consistent growth "
                f"across the analyzed period."
            )

        elif decreasing and not increasing:
            return (
                f"{target_column} is showing a consistent decline "
                f"across the analyzed period."
            )

        elif increasing and decreasing:
            return (
                f"{target_column} remains stable across "
                f"the analyzed period."
            )

        return (
            f"{target_column} shows fluctuations across "
            f"the analyzed period."
        )

    def generate_relationship_insight(
        self,
        correlation,
        column1,
        column2
    ):
        """Generate a business insight from a correlation value."""

        if correlation is None:
            return "No relationship business insight could be generated."

        if correlation >= 0.7:
            return (
                f"{column1} and {column2} move strongly together "
                f"in the analyzed data."
            )

        elif correlation >= 0.3:
            return (
                f"{column1} and {column2} show a moderate positive "
                f"relationship in the analyzed data."
            )

        elif correlation > -0.3:
            return (
                f"{column1} and {column2} show little relationship "
                f"in the analyzed data."
            )

        elif correlation > -0.7:
            return (
                f"{column1} and {column2} show a moderate negative "
                f"relationship in the analyzed data."
            )

        else:
            return (
                f"{column1} and {column2} move strongly in opposite "
                f"directions in the analyzed data."
            )

    def combine_interpretation_and_insight(
        self,
        interpretation,
        insight
    ):
        """Combine interpretation and business insight."""

        if not interpretation:
            return insight

        if not insight:
            return interpretation

        return (
            f"{interpretation}\n"
            f"{insight}"
        )