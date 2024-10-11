import streamlit as st
import pandas as pd
from llm_callers import get_inmails, get_intent_details, get_probing_questions, extract_inputs

def display_output_with_formatting(output):
    # Display the company name as a heading
    st.markdown(f"## {output['company_name']}")

    # Display the Probing Questions section
    st.markdown("### Probing Questions")
    st.markdown("Here are some probing questions to uncover the company's needs:")
    
    # Display each probing question as a bullet point
    for question in output['probing_questions']:
        st.markdown(f"- {question}")
    
    # Display the Talking Points section
    st.markdown("### Talking Points")
    st.markdown("Here are some talking points to address the company's needs in a personalized manner:")

    # Display each talking point as a bullet point
    for point in output['talking_points']:
        st.markdown(f"- {point}")


def display_inmails(output):

    for inmail_key, inmail_value in output.items():
        if inmail_key.startswith("inmail"):

            subject = inmail_value.split('\n')[1]  
            with st.expander(subject.strip()):  
                st.markdown(inmail_value.strip())  



def main():
    st.title("ProspectPitch")
    st.write("Focuses on pitching solutions to potential clients.")

    option = st.sidebar.selectbox(
        "Select function to run",
        ("Extract Inputs", "Get Intent Details", "Get Probing Questions", "Get Inmails")
    )

    if option == "Extract Inputs":
        st.subheader("Extract Inputs")
        output = extract_inputs()
        st.write(output)

    elif option == "Get Intent Details":
        st.subheader("Intent Score Details")
        output = get_intent_details()
        df = pd.DataFrame([output])  # Convert dict output to DataFrame
        st.table(df)

    elif option == "Get Probing Questions":
        st.subheader("Probing Questions")
        output = get_probing_questions()
        display_output_with_formatting(output)  

    elif option == "Get Inmails":
        st.subheader("Inmails")
        output = get_inmails()
        display_inmails(output) 


if __name__ == "__main__":
    main()
