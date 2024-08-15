from langchain_huggingface import HuggingFaceEndpoint
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain_core.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferWindowMemory
from dotenv import load_dotenv
import os
# Load environment variables from .env file
load_dotenv()
# Call and Setup LLM model
llm = HuggingFaceEndpoint(
    repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1",
    task="text-generation",
    max_new_tokens=512,
    temperature=0.01,
    huggingfacehub_api_token=os.getenv('Token')
)

# Define Embedding model
embeddings = HuggingFaceInferenceAPIEmbeddings(
    api_key=os.getenv('Token'), model_name="sentence-transformers/all-MiniLM-l6-v2"
)

# Call stored vectors of documents chunks
current_dir = os.path.dirname(__file__)
# Reach the main project directory
main_dir = os.path.abspath(os.path.join(current_dir, '..'))
db1 = FAISS.load_local(os.path.join(main_dir,'DBFaiss','faiss_index_Consular'), embeddings,allow_dangerous_deserialization=True)
db2 = FAISS.load_local(os.path.join(main_dir, 'DBFaiss','faiss_index_Offering'), embeddings,allow_dangerous_deserialization=True)

# Build our Langchain chain instance (Prompt Template, MemoryBuffer, Conversational chain)
systemPrompt = (
    """Act as expert assistant for question-answer task based strictly on this following rule to generate
    suitable answer related to the context:
    Rule: Review the question and check if it related to the given context or not.
    If the question is unrelated to the given context, which means it talk about out of the context topic, 
    you should answer without verbose with 'Sorry, your query is out of 
    the context. Please ask relevant questions!'.
    Else your answer should strictly 
    adhere to the given context and chat history.
    
   """
    """You find below the given context and chat history, also the question: 
    Context: {context} 
    Chat history: {chat_history} 
    Question: {question} 
    """
)
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", systemPrompt),
        ("human", "{question}"),
    ]
)

memory = ConversationBufferWindowMemory(
    k=2,
    memory_key="chat_history",
    output_key="answer",
    return_messages=True,
)

# Create function that act as chatbot (it combines all defined chains)
def GenerateResponse(query):
    qa_conversation = ConversationalRetrievalChain.from_llm(
        llm=llm,
        combine_docs_chain_kwargs={"prompt": prompt},
        chain_type='stuff',
        retriever = db1.as_retriever(search_kwargs={"k": 2, "fetch_k": 3},search_type = "mmr") if query.startswith('#1') else db2.as_retriever(search_kwargs={"k": 2, "fetch_k": 3},search_type = "mmr"),
        memory=memory)
    return qa_conversation.invoke({'question': f"{query[2:]}"}) ['answer'][11:]
    
    
