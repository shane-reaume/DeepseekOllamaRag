import streamlit as st
from langchain_community.document_loaders import PDFPlumberLoader
from langchain_experimental.text_splitter import SemanticChunker
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from utils.config_loader import OLLAMA_CONFIG

# Define color palette with improved contrast
primary_color = "#007BFF"  # Bright blue for primary buttons
secondary_color = "#FFC107"  # Amber for secondary buttons
background_color = "#F8F9FA"  # Light gray for the main background
sidebar_background = "#2C2F33"  # Dark gray for sidebar (better contrast)
text_color = "#212529"  # Dark gray for content text
sidebar_text_color = "#FFFFFF"  # White text for sidebar
header_text_color = "#000000"  # Black headings for better visibility

st.markdown("""
    <style>
    /* Main Background */
    .stApp {{
        background-color: #F8F9FA;
        color: #212529;
    }}

    /* Sidebar Styling */
    [data-testid="stSidebar"] {{
        background-color: #2C2F33 !important;
        color: #FFFFFF !important;
    }}
    [data-testid="stSidebar"] * {{
        color: #FFFFFF !important;
        font-size: 16px !important;
    }}

    /* Headings */
    h1, h2, h3, h4, h5, h6 {{
        color: #000000 !important;
        font-weight: bold;
    }}

    /* Fix Text Visibility */
    p, span, div {{
        color: #212529 !important;
    }}

    /* File Uploader */
    .stFileUploader>div>div>div>button {{
        background-color: #FFC107;
        color: #000000;
        font-weight: bold;
        border-radius: 8px;
    }}

    /* Fix Navigation Bar (Top Bar) */
    header {{
        background-color: #1E1E1E !important;
    }}
    header * {{
        color: #FFFFFF !important;
    }}
    </style>
""", unsafe_allow_html=True)


# App title
st.title("📄 Build a RAG System with Ollama")

# Add near the top of the file, after imports
def get_model_name(llm):
    """Extract readable model name from Ollama config"""
    return llm.model if hasattr(llm, 'model') else 'Unknown'

def get_ollama_host(llm):
    """Extract host from Ollama config"""
    return llm.base_url if hasattr(llm, 'base_url') else 'localhost:11434'

# Define the LLM before the sidebar
llm = OllamaLLM(
    model=OLLAMA_CONFIG["model"],
    base_url=OLLAMA_CONFIG["base_url"]
)

# Sidebar for instructions and settings
with st.sidebar:
    st.header("Instructions")
    st.markdown("""
    1. Upload a PDF file using the uploader below.
    2. Ask questions related to the document.
    3. The system will retrieve relevant content and provide a concise answer.
    """)

    st.header("Settings")
    st.markdown(f"""
    - **Embedding Model**: HuggingFace
    - **Retriever Type**: Similarity Search
    - **LLM Model**: {get_model_name(llm)}
    - **Ollama Host**: {get_ollama_host(llm)}
    """)

# Main file uploader section
st.header("📁 Upload a PDF Document")
uploaded_file = st.file_uploader("Upload your PDF file here", type="pdf")

if uploaded_file is not None:
    st.success("PDF uploaded successfully! Processing...")

    # Save the uploaded file
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.getvalue())

    # Load the PDF
    loader = PDFPlumberLoader("temp.pdf")
    docs = loader.load()

    # Split the document into chunks
    st.subheader("📚 Splitting the document into chunks...")
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    text_splitter = SemanticChunker(embeddings)
    documents = text_splitter.split_documents(docs)

    # Create vector store and retriever
    st.subheader("🔍 Creating embeddings and setting up the retriever...")
    vector = FAISS.from_documents(documents, embeddings)
    retriever = vector.as_retriever(search_type="similarity", search_kwargs={"k": 3})

    # Define the prompt
    prompt = PromptTemplate.from_template("""
    1. Use the following pieces of context to answer the question at the end.
    2. If you don't know the answer, just say that "I don't know" but don't make up an answer on your own.\n
    3. You are a helpful assistant that uses dialog that improves the users memory and understanding of the context in under 500 words.
    4. You convert abstract concepts into vivid spatial narratives when explaining the context as needed.
    Context: {context}
    Question: {input}
    Helpful Answer:""")  # Changed {question} to {input}

    # Create the chain using modern patterns
    document_chain = create_stuff_documents_chain(
        llm=llm,
        prompt=prompt,
        document_variable_name="context"
    )

    qa_chain = create_retrieval_chain(
        retriever,
        document_chain
    )

    # Question input and response display
    st.header("❓ Ask a Question")
    user_input = st.text_input("Type your question related to the document:")

    if user_input:
        with st.spinner("Processing your query..."):
            try:
                response = qa_chain.invoke({"input": user_input})
                st.success("✅ Response:")
                st.write(response["answer"])
            except Exception as e:
                st.error(f"An error occurred: {e}")
else:
    st.info("Please upload a PDF file to start.")


