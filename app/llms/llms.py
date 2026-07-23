from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from app.schemas.schemas import *

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

# question = "Give me last week's international men's cricket news in medium format."
# structured_llm = llm_groq.with_structured_output(NewsRequest)

question = """
Generate 2 sample news articles about international men's cricket from last week.
Populate every field realistically.
"""

structured_llm = llm_groq.with_structured_output(NewsArticleCollection)
response = structured_llm.invoke(question)

print(response)
print(type(response))