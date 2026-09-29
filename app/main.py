import streamlit as st
from data.understanding import understand_dataset
from nlu.question_parser import parse_question
from nlu.nlu_validator import validate_nlu
from agents.planner import create_analysis_plan
from agents.plan_validator import validate_analysis_plan
from agents.code_generator import generate_code
from analysis.executor import execute_code

from config import APP_NAME, APP_ICON, PAGE_LAYOUT
from data.loader import load_dataset


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

            parsed_result = parse_question(
                question,
                df.columns.tolist()
            )

            validation_result = validate_nlu(
            parsed_result,
            df.columns.tolist()
            )
            analysis_plan = create_analysis_plan(parsed_result)

            plan_valid = validate_analysis_plan(analysis_plan)

            st.success("Question submitted successfully!")
            st.write("Your question:", question)

            st.subheader("Parsed Question")
            st.json(parsed_result)

            st.subheader("NLU Validation")
            st.json(validation_result)  

            st.subheader("Analysis Plan")
            st.json(analysis_plan.to_dict()) 

            st.subheader("Plan Validation")
            st.write(plan_valid)

            if not plan_valid:
                st.warning(
                    "Unable to create a valid analysis plan. "
                    "Please provide more details in your question."
                )

            else:
                generated_code = generate_code(analysis_plan.to_dict())

                st.subheader("Generated Python Code")
                st.code(generated_code, language="python")

                execution_result = execute_code(
                generated_code,
                df
                )

                st.subheader("Execution Result")

                if execution_result["success"]:
                    st.success("Code executed successfully!")

                    st.write("Result:")
                    st.write(execution_result["result"])

                    if execution_result["output"]:
                        st.write("Output:")
                        st.text(execution_result["output"])

                else:
                    st.error("Code execution failed.")

                    st.write("Error Type:")
                    st.write(execution_result["error_type"])

                    st.write("Error:")
                    st.write(execution_result["error"])
        else:
            st.warning("Please upload a dataset first.")

    else:
        st.warning("Please enter a question first.")