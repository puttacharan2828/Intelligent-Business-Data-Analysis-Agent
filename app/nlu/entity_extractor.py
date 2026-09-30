import re


def extract_metric(question, columns):
    question = question.lower()

    group_words = ["by", "per", "each"]

    for word in group_words:
        match = re.search(r"\b" + re.escape(word) + r"\b", question)

        if match:
            question = question[:match.start()]
            break

    for column in columns:
        if column.lower() in question:
            return column

    return None


def extract_group_by(question, columns):
    question = question.lower()

    # Handle relationship questions
    if "between" in question and "and" in question:

        parts = question.split("between", 1)[1]
        parts = parts.split("and", 1)

        if len(parts) == 2:
            second_part = parts[1]

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

    filter_words = ["where", "for", "in", "with"]

    for word in filter_words:

        match = re.search(
            r"\b" + re.escape(word) + r"\b",
            question
        )

        if match:

            remaining_text = question[match.end():].strip()

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


def extract_time(question):
    match = re.search(r"\b(19|20)\d{2}\b", question)

    if match:
        return match.group()

    return None
