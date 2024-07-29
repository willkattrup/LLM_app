from api_denial import APIClient
import streamlit as st

# Define the function to classify text using OpenAI GPT
def classify_text(input_text):
    client = APIClient()
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

# Streamlit interface
st.title("Large Language Model Classification of Climate Denial and Delay")

st.write("Enter the text you want to classify:")

user_input = st.text_area("Input text", height=150)

if st.button("Classify"):
    if user_input:
        with st.spinner('Classifying...'):
            classification_result = classify_text(user_input)
            st.success(f"Classification: {classification_result}")
    else:
        st.error("Please enter some text to classify.")


