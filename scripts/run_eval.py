import sys
import os
import asyncio
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.rag.pipeline import query_rag
from app.core.config import settings

from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from datasets import Dataset

# 1. DATA TEST
TEST_QUESTIONS = [
    "Siapa nama kandidat dalam CV ini?",
    "Sebutkan skill database yang dimiliki kandidat!",
    "Apa pengalaman organisasi kandidat?",
    "Apakah kandidat bisa bahasa Python?", 
]

async def generate_responses():
    print("⏳ Sedang menjawab pertanyaan menggunakan RAG Pipeline...")
    
    data = {
        # Kita ubah nama key ke standar baru RAGAS biar aman
        "user_input": [],  # Dulu "question"
        "response": [],    # Dulu "answer"
        "retrieved_contexts": [], # Dulu "contexts"
    }

    for q in TEST_QUESTIONS:
        result = await query_rag(q)
        
        data["user_input"].append(q)
        data["response"].append(result["answer"])
        
        from app.rag.pipeline import get_retriever
        retriever = get_retriever()
        docs = retriever.invoke(q)
        context_texts = [d.page_content for d in docs]
        
        data["retrieved_contexts"].append(context_texts)
        
        print(f"✅ Q: {q} | A: {result['answer'][:50]}...")

    return data

def run_evaluation():
    print("\n⚖️  Sedang melakukan penilaian oleh Juri AI...")
    
    gemini_llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash", 
        google_api_key=settings.GOOGLE_API_KEY,
        temperature=0
    )
    
    local_embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # 3. JALANKAN EVALUASI
    rag_data = asyncio.run(generate_responses())
    dataset = Dataset.from_dict(rag_data)

    metrics = [faithfulness, answer_relevancy]

    results = evaluate(
        dataset=dataset,
        metrics=metrics,
        llm=gemini_llm,
        embeddings=local_embeddings
    )

    # 4. TAMPILKAN HASIL (VERSI AMAN)
    print("\n📊 === HASIL EVALUASI RAGAS === 📊")
    df = results.to_pandas()
    
    # Kita print semua kolom yang ada, biar gak error KeyError lagi
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1000)
    
    # Print DataFrame utuh
    print(df)
    
    print("\n📈 Rata-rata Skor Keseluruhan:")
    print(results)

if __name__ == "__main__":
    run_evaluation()