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
            if re.search(r"\b" + re.escape(keyword) + r"\b", question):
                return operation

    return None


def extract_filter(question, columns):
    question = question.lower()

    filter_words = ["where", "for", "in", "with"]

    for word in filter_words:
        if word in question:
            remaining_text = question.split(word, 1)[1].strip()

            for column in columns:
                column_name = column.lower()

                if column_name in remaining_text:
                    value_text = remaining_text.split(column_name, 1)[1].strip()
                    words = value_text.split()

                    if words:
                        return {
                            "column": column,
                            "value": words[0]
                        }

    return None


def extract_time(question):
    match = re.search(r"\b(19|20)\d{2}\b", question)

    if match:
        return match.group()

    return None