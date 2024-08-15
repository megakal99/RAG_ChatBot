import streamlit as st
from RAG_Setup import GenerateResponse

#################### Build sample ChatBot interface ######################

st.set_page_config(
    page_title="Documents Chat Challenge",
    page_icon="../static/favicon.png",  
)

# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": """To discuss documents, please begin your message with either #1 or #2: 
                                  #1 for the Consular Insurance document, and #2 for the Offering Memorandum document."""}]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Function for generating LLM response
def generate_response(prompt_input):
    return GenerateResponse(prompt_input)

# User-provided prompt
if prompt := st.chat_input():
    if '#1' == prompt[:2] or '#2' == prompt[:2]:
      st.session_state.messages.append({"role": "user", "content": prompt})
      with st.chat_message("user"):
        st.write(prompt)
    else:
        st.warning('Please begin your request by #1 or #2')

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_response(prompt) 
            st.write(response) 
    message = {"role": "assistant", "content": response}
    st.session_state.messages.append(message)