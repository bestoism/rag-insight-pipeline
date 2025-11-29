from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from app.core.config import settings
from langfuse.langchain import CallbackHandler
from app.core.database import get_qdrant_client

# --- FIX: GLOBAL VARIABLE ---
# Kita simpan koneksi database di sini supaya tidak dibuka-tutup terus

def get_retriever():
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # PANGGIL DARI IMPORT
    client = get_qdrant_client()
    
    vector_store = QdrantVectorStore(
        client=client,
        collection_name=settings.QDRANT_COLLECTION_NAME,
        embedding=embeddings,
    )
    return vector_store.as_retriever(search_kwargs={"k": 6})

def get_llm():
    if not settings.GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY is missing")
    
    return ChatGoogleGenerativeAI(
        model="gemini-2.0-flash", 
        google_api_key=settings.GOOGLE_API_KEY,
        temperature=0.1
    )

async def query_rag(question: str):
    retriever = get_retriever()
    llm = get_llm()
    
    langfuse_handler = CallbackHandler() 
    
    template = """You are a helpful HR Assistant reviewing a CV/Document. 
    Answer the user's question based on the context below. 
    If the answer is not explicitly in the context, just say "I don't find that information in the document."
    
    Context:
    {context}
    
    Question: {question}
    
    Answer:"""
    
    prompt = ChatPromptTemplate.from_template(template)
    
    def format_docs(docs):
        return "\n\n".join([d.page_content for d in docs])

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    response = await chain.ainvoke(
        question,
        config={"callbacks": [langfuse_handler]} 
    )
    
    source_docs = retriever.invoke(question)
    sources = [doc.metadata.get("source", "Unknown") for doc in source_docs]
    
    return {
        "answer": response,
        "sources": list(set(sources))
    }