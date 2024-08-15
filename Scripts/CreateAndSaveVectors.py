# Calling necessary librairies, frameworks
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
import os
####################################################
# Load environment variables from .env file
load_dotenv()
inference_api_key= os.getenv('Token')
# Call embedding model
embeddings = HuggingFaceInferenceAPIEmbeddings(
    api_key=inference_api_key, model_name="sehf_AJYHYozZNeZCApmuYoQqyNUCtiNGmXXFrBntence-transformers/all-MiniLM-l6-v2"
)
# Load documents
loader_doc1 = PyPDFLoader("../data/consular insurance.pdf")
loader_doc2 = PyPDFLoader("../data/offering memorandum.pdf")

pages1=loader_doc1.load()
pages2=loader_doc2.load()

# Split documents into chunks, embed each chunk and load it into the vector store per document.
text_splitter = CharacterTextSplitter(chunk_size=1200, chunk_overlap=0, separator=".")
documents = text_splitter.split_documents(pages1)
documents_ = text_splitter.split_documents(pages2)
db_doc1 = FAISS.from_documents(documents,embeddings)
db_doc2 = FAISS.from_documents(documents_,embeddings)
#save stored vectores (index)in disk
db_doc1.save_local("../DBFaiss/faiss_index_Consular")
db_doc2.save_local("../DBFaiss/faiss_index_Offering")





