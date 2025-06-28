from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from langchain_ollama import OllamaLLM
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
import re

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question: str

# Load model and knowledge base at startup
llm = OllamaLLM(model="tinyllama")
pdf_path = "qonnect_knowledge.pdf"
loader = PyPDFLoader(pdf_path)
docs = loader.load()
qa_documents = []
for doc in docs:
    pairs = re.findall(r'\d+\.\s*Q:.*?\n\s*A:.*?(?=\n\d+\.|$)', doc.page_content, re.DOTALL)
    for pair in pairs:
        qa_documents.append(type(doc)(page_content=pair.strip()))
embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-MiniLM-L6-v2")
index_path = "faiss_index"
if not os.path.exists(index_path):
    vectorstore = FAISS.from_documents(qa_documents, embedding)
    vectorstore.save_local(index_path)
else:
    vectorstore = FAISS.load_local(index_path, embedding, allow_dangerous_deserialization=True)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True
)

@app.post("/ask")
async def ask_qonnect(request: QueryRequest):
    try:
        result = qa_chain.invoke({"query": request.question})
        answer = result["result"]
        source = result["source_documents"][0].page_content[:300]
        return {"answer": answer, "source": source}
    except Exception as e:
        return {"error": str(e)} 