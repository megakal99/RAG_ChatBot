# RAG_ChatBot

The RAG_ChatBot provides responses based on data extracted from documents related to risk factors in financial trade. It uses Retrieval-Augmented Generation (RAG) to enhance responses with relevant information from the provided documents.

### Features:

    * Data-Driven Responses: Answers based on data extracted from provided documents.
    * Retrieval-Augmented Generation: Combines information retrieval with generation for accurate and relevant responses.
    * Customizable: Adapt the chatbot to work with your own private documents
    * Interactive Interface: Built with Streamlit for a user-friendly experience.

### Live Demo:

Explore the live application here: https://ragchatbot-2qbgjsi9kxadmgdqreaqox.streamlit.app/

### Running Locally:

To set up and run the RAG_ChatBot locally, follow these steps:

    1- Clone the Repository
    2- Create and Activate a python Virtual Environment
    3- Install Dependencies : pip install -r requirements.txt
    4- Set Up Environment Variables: open .env then modify it by adding : TOKEN="<your-hugging-face-token>"
    Replace <your-hugging-face-token> with your Hugging Face API token. Obtain this token by creating an account on Hugging Face and generating an API token in your account    settings.
    5- Run the Application: streamlit run Scripts/App.py
    
### Customizing the Chatbot:

To specialize the chatbot for your private documents, you need to modify the code files in the Scripts folder:

    1- Prepare Your Documents: Place your private documents in the data/ directory.
    2- Modify Code Files:
        
        - Update Document Paths: In the Scripts folder, update the paths to your private documents within the relevant code files.
        - Adjust splitting Logic: Customize the document splitting to chunks logic in the scripts to suit the format and content of your private documents.
        - Adjust the Prompt Template.
        - Rebuild or Restart the Application
