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
# Get the directory of the current script
current_directory = os.path.dirname(os.path.abspath(__file__))
# Construct the path to the PDF file by moving up one directory and then into the 'data' subdirectory
current_dir = os.path.dirname(__file__)
# Reach the main project directory
main_dir = os.path.abspath(os.path.join(current_dir, '..'))
pdf1_path = os.path.join(main_dir,'data', 'consular insurance.pdf')
pdf2_path = os.path.join(main_dir,'data', 'offering memorandum.pdf')
# Load documents
loader_doc1 = PyPDFLoader(pdf1_path)
loader_doc2 = PyPDFLoader(pdf2_path)

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





