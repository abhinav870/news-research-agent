from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

llm_model = HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.1-8B-Instruct",
    temperature=0,
)

llm_hf = ChatHuggingFace(llm=llm_model)

llm_groq = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    max_tokens=1000,
)

question = 'What is the capital of India'
response = llm_groq.invoke(question)

print(response)