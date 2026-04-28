import os
import pickle
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Load environment variables
load_dotenv()

# Load FAISS vectorstore
with open("faiss_index.pkl", "rb") as f:
    vectorstore = pickle.load(f)

# Initialize LLM (Groq) - API key now comes from .env
llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.1-8b-instant",
    temperature=0
)

def query_kb(question):

    docs = vectorstore.similarity_search_with_score(question, k=3)

    # ❌ STRICT FAIL CONDITION (IMPORTANT FIX)
    if not docs:
        return None

    best_score = docs[0][1]

    # ❌ if weak match → force no answer
    if best_score > 1.5:
        return None

    context = "\n".join([d.page_content for d, _ in docs])

    prompt = f"""
Use ONLY this agricultural knowledge:

{context}

Question: {question}

If answer is not present, return empty response.
"""

    result = llm.invoke(prompt).content

    # ❌ avoid fake answers
    if not result or len(result.strip()) < 5:
        return None

    return result