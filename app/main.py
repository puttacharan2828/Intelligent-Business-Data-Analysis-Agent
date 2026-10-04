import streamlit as st
from data.understanding import understand_dataset
from agents.agent import AnalysisAgent
from memory.conversation_memory import ConversationMemory
from memory.conversation_context import ConversationContext

from config import APP_NAME, APP_ICON, PAGE_LAYOUT
from data.loader import load_dataset


agent = AnalysisAgent()
if "conversation_memory" not in st.session_state:
    st.session_state.conversation_memory = ConversationMemory()

conversation_context = ConversationContext(
    st.session_state.conversation_memory
)


st.set_page_config(
    page_title=APP_NAME,
    page_icon=APP_ICON,
    layout=PAGE_LAYOUT
)


st.title("📊 Intelligent Business Data Analysis Agent")

st.write(
    "Upload your dataset and ask questions about your data "
    "using natural language."
)


st.header("1. Upload Your Dataset")


uploaded_file = st.file_uploader(
    "Choose a CSV or Excel file",
    type=["csv", "xlsx"]
)


if uploaded_file is not None:

    try:
        df = load_dataset(uploaded_file)

        understanding = understand_dataset(df)

        profile = understanding["profile"]
        numerical_analysis = understanding["numerical_analysis"]
        categorical_analysis = understanding["categorical_analysis"]
        quality_report = understanding["quality"]
        column_classification = understanding["column_classification"]

        st.subheader("Dataset Profile")

        st.write("Rows:", profile["rows"])
        st.write("Columns:", profile["columns"])
        st.write("Column Names:", profile["column_names"])
        st.write("Data Types:", profile["data_types"])
        st.write("Missing Values:", profile["missing_values"])
        st.write("Duplicate Rows:", profile["duplicate_rows"])

        st.subheader("Numerical Analysis")
        st.dataframe(numerical_analysis)

        st.subheader("Categorical Analysis")
        st.write(categorical_analysis)

        st.subheader("Data Quality")
        st.write(quality_report)

        st.subheader("Column Classification")
        st.write(column_classification)

        st.success("Dataset uploaded successfully!")

        st.subheader("Dataset Preview")
        st.dataframe(df)

    except ValueError as e:
        st.error(str(e))

    except Exception:
        st.error(
            "Something went wrong while loading the dataset. "
            "Please check that the file is valid and try again."
        )


st.header("2. Ask a Question")


question = st.text_input(
    "What would you like to know about the data?"
)


analyze_button = st.button("Analyze")


if analyze_button:

    if question:

        if uploaded_file is not None:

            context = conversation_context.resolve_question(question)

            if context["is_follow_up"]:
                st.info(
                    f"Follow-up detected. Interpreting as: "
                    f"{context['resolved_question']}"
                )

            agent_state = agent.run(
                context["resolved_question"],
                df,
                df.columns.tolist()
            )

            st.subheader("Agent Result")

            if agent_state.error is not None:

                st.error("Analysis could not be completed.")

                st.write(
                    "Error:",
                    agent_state.error
                )

                if agent_state.recovery_attempted:
                    st.info(
                        "The agent attempted error recovery."
                    )

            else:

                st.subheader("Analysis Result")
                st.write(agent_state.interpretation)

                st.subheader("Business Insight")
                st.write(agent_state.business_insight)

                st.session_state.conversation_memory.add(
                    context["resolved_question"],
                    agent_state.execution_result["result"],
                    agent_state.interpretation,
                    context["is_follow_up"],
                    context["original_question"]
                )

                if agent_state.visualization is not None:

                    st.subheader("Visualization")
                    st.pyplot(agent_state.visualization)

                with st.expander("Agent Details"):

                    st.write("Analysis Plan:")
                    st.json(
                        agent_state.analysis_plan.to_dict()
                    )

                    st.write("Generated Code:")
                    st.code(
                        agent_state.generated_code,
                        language="python"
                    )

                    st.write("Execution Result:")
                    st.write(
                        agent_state.execution_result["result"]
                    )                

        else:

            st.warning(
                "Please upload a dataset first."
            )

    else:

        st.warning(
            "Please enter a question first."
        )


st.header("3. Conversation Memory")

if st.button("Clear Conversation"):
    st.session_state.conversation_memory.clear()
    st.rerun()

memory_history = st.session_state.conversation_memory.get_history()

if memory_history:

    for index, entry in enumerate(memory_history, start=1):

        st.write(f"### Conversation {index}")

        st.write(
            "Question:",
            entry["question"]
        )

        st.write(
            "Result:",
            entry["result"]
        )

        st.write(
            "Interpretation:",
            entry["interpretation"]
        )

        if entry["is_follow_up"]:

            st.write(
                "Follow-up:",
                entry["original_question"]
            )

else:

    st.write("No conversation history yet.")