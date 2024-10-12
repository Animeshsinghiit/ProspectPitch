import streamlit as st
import pandas as pd
from llm_callers import get_inmails, get_intent_details, get_probing_questions, extract_inputs
from st_auth import check_password,controller
def display_output_with_formatting(output):
    
    st.markdown(f"## {output['company_name']}")

    
    st.markdown("### Probing Questions")
    st.markdown("Here are some probing questions to uncover the company's needs:")
    
    
    for question in output['probing_questions']:
        st.markdown(f"- {question}")
    
    
    st.markdown("### Talking Points")
    st.markdown("Here are some talking points to address the company's needs in a personalized manner:")

    
    for point in output['talking_points']:
        st.markdown(f"- {point}")


def display_inmails(output):

    for inmail_key, inmail_value in output.items():
        if inmail_key.startswith("inmail"):

            subject = inmail_value.split('\n')[1]  
            with st.expander(subject.strip()):  
                st.markdown(inmail_value.strip())  



def main():
    login_status = check_password()

    if not login_status:
        st.stop()

    if st.button("logout", key="1"):
        logged_in_user = st.session_state.get("username", controller.get('logged_in_user'))
        if logged_in_user:
            st.write(f"Welcome, {logged_in_user}!")
            st.session_state.clear()
            controller.remove('login_status')
            controller.remove('logged_in_user')
            st.rerun()

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
