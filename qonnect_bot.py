import os
import random
from langchain_community.llms import Ollama
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# Cute bot
class CuteBot:
    def __init__(self):
        self.greetings = ["Hi! 👋", "Hello! ✨", "Hey there! 🌟"]
    
    def greet(self):
        return random.choice(self.greetings)
    
    def format_answer(self, answer):
        if "wifi" in answer.lower():
            return f"📶 {answer}"
        elif "food" in answer.lower():
            return f"🍕 {answer}"
        elif "library" in answer.lower():
            return f"📚 {answer}"
        else:
            return f"💡 {answer}"

# Initialize
cute_bot = CuteBot()

# Load model
llm = Ollama(model="tinyllama")
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Load PDF
loader = PyPDFLoader("qonnect_knowledge.pdf")
documents = loader.load()

# Split documents
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
texts = text_splitter.split_documents(documents)

# Create or load vector store
if os.path.exists("faiss_index"):
    vectorstore = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
else:
    vectorstore = FAISS.from_documents(texts, embeddings)
    vectorstore.save_local("faiss_index")

# Create QA chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever(search_kwargs={"k": 2}),
    return_source_documents=True,
    chain_type_kwargs={
        "prompt": PromptTemplate(
            input_variables=["context", "question"],
            template="""You are QonnectBot, a friendly campus assistant! 

Answer the question clearly and concisely using only the provided context.

Context: {context}
Question: {question}

Answer:"""
        )
    }
)

# Simple analytics
class SimpleAnalytics:
    def __init__(self):
        self.data = {"questions": 0, "satisfaction": []}
    
    def track(self, question, rating=None):
        self.data["questions"] += 1
        if rating:
            self.data["satisfaction"].append(rating)
    
    def get_stats(self):
        avg = sum(self.data["satisfaction"]) / len(self.data["satisfaction"]) if self.data["satisfaction"] else 0
        return f"Questions: {self.data['questions']} | Avg Rating: {avg:.1f}/5"

analytics = SimpleAnalytics()

# Main chat loop
print("🎓 QonnectBot Ready!")
print(cute_bot.greet())

while True:
    query = input("\nYou: ").strip()
    
    if not query:
        continue
    
    if query.lower() in ['quit', 'exit', 'bye']:
        print("👋 Bye!")
        break
    elif query.lower() == 'stats':
        print(f"📊 {analytics.get_stats()}")
        continue
    elif query.lower() in ['hello', 'hi', 'hey']:
        print(cute_bot.greet())
        continue
    
    try:
        print("🤔 Thinking...")
        
        # Get answer
        result = qa_chain.invoke({"query": query})
        answer = result["result"].strip()
        
        # Clean up answer
        if "Q:" in answer and "A:" in answer:
            parts = answer.split("A:")
            if len(parts) > 1:
                answer = parts[1].strip()
        
        # Format and display
        formatted_answer = cute_bot.format_answer(answer)
        print(f"Bot: {formatted_answer}")
        
        # Track
        analytics.track(query)
        
        # Simple feedback
        rating = input("Rate (1-5) or Enter to skip: ").strip()
        if rating.isdigit() and 1 <= int(rating) <= 5:
            analytics.track(query, int(rating))
            print("Thanks! 💕")
        
    except Exception as e:
        print(f"Oops! {e}") 