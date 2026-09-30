import matplotlib.pyplot as plt


def create_bar_chart(data, x_column, y_column):
    fig, ax = plt.subplots()

    ax.bar(data[x_column], data[y_column])

    ax.set_xlabel(x_column)
    ax.set_ylabel(y_column)
    ax.set_title(f"{y_column} by {x_column}")

    return fig


def create_line_chart(data, x_column, y_column):
    fig, ax = plt.subplots()

    ax.plot(data[x_column], data[y_column])

    ax.set_xlabel(x_column)
    ax.set_ylabel(y_column)
    ax.set_title(f"{y_column} over {x_column}")

    return fig


def create_scatter_plot(data, x_column, y_column):
    fig, ax = plt.subplots()

    ax.scatter(data[x_column], data[y_column])

    ax.set_xlabel(x_column)
    ax.set_ylabel(y_column)
    ax.set_title(f"{y_column} vs {x_column}")

    return fig


def create_histogram(data, column):
    fig, ax = plt.subplots()

    ax.hist(data[column])

    ax.set_xlabel(column)
    ax.set_ylabel("Frequency")
    ax.set_title(f"Distribution of {column}")

    return fig


def validate_visualization_data(
    data,
    analysis_type,
    x_column=None,
    y_column=None
):
    if data is None or data.empty:
        raise ValueError("No data available for visualization.")

    if analysis_type == "distribution":

        if y_column not in data.columns:
            raise ValueError(
                f"Column '{y_column}' not found in the dataset."
            )

    elif analysis_type in [
        "comparison",
        "trend",
        "relationship"
    ]:

        if x_column not in data.columns:
            raise ValueError(
                f"Column '{x_column}' not found in the dataset."
            )

        if y_column not in data.columns:
            raise ValueError(
                f"Column '{y_column}' not found in the dataset."
            )


def create_visualization(
    data,
    analysis_type,
    x_column=None,
    y_column=None
):
    validate_visualization_data(
        data,
        analysis_type,
        x_column,
        y_column
    )

    if analysis_type == "distribution":
        return create_histogram(data, y_column)

    elif analysis_type == "comparison":
        return create_bar_chart(
            data,
            x_column,
            y_column
        )

    elif analysis_type == "relationship":
        return create_scatter_plot(
            data,
            x_column,
            y_column
        )

    elif analysis_type == "trend":
        return create_line_chart(
            data,
            x_column,
            y_column
        )

    else:
        raise ValueError("Unsupported analysis type.")