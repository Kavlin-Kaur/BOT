import os
from langchain_ollama import OllamaLLM
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
import traceback
import re

print('Step 1: Starting QonnectBot')

# Load local model (low RAM usage)
llm = OllamaLLM(model="tinyllama")
print('Step 2: Loaded OllamaLLM')

# Updated knowledge base path
pdf_path = "qonnect_knowledge.pdf"  # Changed to match available file
print(f'Step 3: Using PDF path: {pdf_path}')

# Load PDF content
try:
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    print(f'Step 4: Loaded {len(docs)} documents from PDF')
    if not docs:
        raise ValueError("PDF is empty or not readable.")
except Exception as e:
    print(f"\n❌ Failed to load PDF: {e}\n")
    input("Press Enter to exit...")
    exit()

# Instead of splitting by chunk size, split by Q&A pairs
qa_documents = []
for doc in docs:
    # Find all Q&A pairs in the text, allowing for numbering and whitespace
    pairs = re.findall(r'\d+\.\s*Q:.*?\n\s*A:.*?(?=\n\d+\.|$)', doc.page_content, re.DOTALL)
    for pair in pairs:
        qa_documents.append(type(doc)(page_content=pair.strip()))
print(f'Step 5: Split into {len(qa_documents)} Q&A documents')

documents = qa_documents

# Create embeddings
embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-MiniLM-L6-v2")
print('Step 6: Created HuggingFaceEmbeddings')

# Create or load FAISS index
index_path = "faiss_index"
try:
    if not os.path.exists(index_path):
        print("📌 Creating new vector index...")
        vectorstore = FAISS.from_documents(documents, embedding)
        vectorstore.save_local(index_path)
        print('Step 7: New FAISS index created and saved')
    else:
        print("✅ Loading existing vector index...")
        vectorstore = FAISS.load_local(index_path, embedding, allow_dangerous_deserialization=True)
        print('Step 7: Loaded existing FAISS index')
except Exception as e:
    print(f"❌ Failed to load FAISS index: {e}")
    input("Press Enter to exit...")
    exit()

# Build retriever and chain
retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True
)
print('Step 8: QA chain ready')

# Chat loop
while True:
    query = input("\n🧠 Ask QonnectBot anything (or type 'exit'): ")
    if query.lower() in ["exit", "quit"]:
        print("👋 Byeee! QonnectBot signing off.")
        break

    try:
        result = qa_chain.invoke({"query": query})
        print("\n💬 QonnectBot says:", result["result"])
        print("\n📄 Source:\n", result["source_documents"][0].page_content[:300], "...\n")
    except Exception as e:
        print(f"⚠️ Oops! Something went wrong: {e}")
        traceback.print_exc()
