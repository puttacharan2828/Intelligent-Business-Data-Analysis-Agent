import re


def extract_metric(question, columns):
    question = question.lower()

    group_words = ["by", "per", "each"]

    for word in group_words:
        match = re.search(r"\b" + re.escape(word) + r"\b", question)

        if match:
            question = question[:match.start()]
            break

    # Prefer numeric columns as metrics
    numeric_columns = ["sales", "quantity", "revenue", "profit", "amount"]

    for column in columns:
        if column.lower() in numeric_columns and column.lower() in question:
            return column

    # Fallback: return any column mentioned in the question
    for column in columns:
        if column.lower() in question:
            return column

    return None


def extract_group_by(question, columns):
    question = question.lower()

    # Handle relationship questions
    if "between" in question and "and" in question:

        relationship_part = question.split("between", 1)[1]

        first_part, second_part = relationship_part.split("and", 1)

        for column in columns:
            if column.lower() in second_part:
                 return column
    # Handle grouped questions
    group_words = ["by", "per", "each"]

    for word in group_words:
        match = re.search(r"\b" + re.escape(word) + r"\b", question)

        if match:
            remaining_text = question[match.end():]

            for column in columns:
                if column.lower() in remaining_text:
                    return column

    return None


OPERATION_KEYWORDS = {
    "sum": ["total", "sum"],
    "mean": ["average", "mean"],
    "max": ["maximum", "highest", "largest", "max"],
    "min": ["minimum", "lowest", "smallest", "min"],
    "count": ["count", "number", "how many"]
}


def extract_operation(question):
    question = question.lower()

    for operation, keywords in OPERATION_KEYWORDS.items():

        for keyword in keywords:

            if re.search(
                r"\b" + re.escape(keyword) + r"\b",
                question
            ):
                return operation

    return None


def extract_filter(question, columns):
    question = question.lower()

    filter_words = ["where", "for", "in", "with", "of"]

    for word in filter_words:

        match = re.search(
            r"\b" + re.escape(word) + r"\b",
            question
        )

        if match:

            remaining_text = question[match.end():].strip()

            # "of" should be treated as a filter
            # only when a filter column follows it.
            if word == "of":

                has_filter_column = any(
                    re.search(
                        r"\b" + re.escape(column.lower()) + r"\b",
                        remaining_text
                    )
                    and column.lower() != extract_metric(question, columns).lower()
                    for column in columns
                )

                if not has_filter_column:
                    continue

            # Case 1:
            # Filter column is explicitly mentioned.
            #
            # Example:
            # "total Sales for Category Electronics"
            for column in columns:

                column_name = column.lower()

                if re.search(
                    r"\b" + re.escape(column_name) + r"\b",
                    remaining_text
                ):

                    value_text = re.split(
                        r"\b" + re.escape(column_name) + r"\b",
                        remaining_text,
                        maxsplit=1
                    )[1].strip()

                    words = value_text.split()

                    if words:

                        value = words[0].strip(".,!?;:")

                        return {
                            "column": column,
                            "value": value
                        }

            # Case 2:
            # Example:
            # "What is the total Sales for Electronics?"
            if word == "for":

                for column in columns:

                    if column.lower() == "category":

                        words = remaining_text.split()

                        if words:

                            value = words[0].strip(".,!?;:")

                            return {
                                "column": column,
                                "value": value
                            }

    return None


def extract_time(question, columns):
    time_keywords = [
        "date",
        "time",
        "year",
        "month",
        "day"
    ]

    question_lower = question.lower()

    for column in columns:
        column_lower = column.lower()

        if column_lower in time_keywords:
            return column

        if column_lower in question_lower and any(
            keyword in column_lower for keyword in time_keywords
        ):
            return column

    return None