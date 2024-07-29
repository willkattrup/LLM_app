import streamlit as st
from openai import OpenAIError
from api_denial import APIClient

# Streamlit app
st.title("Large Language Model Classification of Climate Denial and Delay")

if 'api_key' not in st.session_state:
    st.session_state['api_key'] = None

# Define the function to classify text using OpenAI GPT
def classify_text(input_text, api_key):
    client = APIClient(api_key=api_key)
    result, response, claims_list = client.ACoT_pipeline(input_text)
    
    return_text = result
    
    if result == 0:
        return_text = "0, no claim."
    elif result == 1:
        return_text = "1, climate delay."
    elif result == 2:
        return_text = "2, climate denial."
    else:
        return_text = "something went wrong."
    return return_text

def validate_api_key(api_key):
    try:
        client = APIClient(api_key=api_key)
        client.validate_api_key()
        return True
    except OpenAIError:
        return False

if st.session_state['api_key'] is None:
    st.header("Login")
    api_key = st.text_input("Enter key", type="password")
    if st.button("Login"):
        if validate_api_key(api_key):
            st.session_state['api_key'] = api_key
            st.success("Login successful!")
            st.experimental_rerun()
        else:
            st.error("Invalid API key. Please try again.")
else:
    st.header("Classification")
    user_input = st.text_area("Input text", height=150)

    if st.button("Classify"):
        if user_input:
            with st.spinner('Classifying...'):
                classification_result = classify_text(user_input, st.session_state['api_key'])
                st.success(f"Classification: {classification_result}")
        else:
            st.error("Please enter some text to classify.")
