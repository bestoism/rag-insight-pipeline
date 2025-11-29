# 🚀 RAG Insight Pipeline

> **An Enterprise-Grade GenAI Architecture: Scalable RAG Pipeline featuring Hybrid Vector Search, Full-Stack MLOps Observability, and Automated Evaluation Loops.**

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-Production-green.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)
![CI/CD](https://github.com/bestoism/rag-insight-pipeline/actions/workflows/ci.yml/badge.svg)
![Qdrant](https://img.shields.io/badge/VectorDB-Qdrant-red.svg)

## 📖 Overview

**RAG Insight Pipeline** goes beyond standard RAG tutorials by implementing **MLOps best practices** for production environments. It addresses critical challenges in Generative AI such as **hallucination monitoring**, **retrieval accuracy**, and **deployment scalability**.

Engineered to be modular, it allows users to upload complex PDF documents, automatically index them into a hybrid vector store, and perform intelligent Q&A using **Google Gemini 2.0 Flash** with strictly grounded responses.

### 🌟 Key Features

*   **🏗 Hybrid Vector Database Architecture**: Smart routing that switches between **Qdrant Local** (for fast development) and **Qdrant Cloud** (for scalable production) based on environment context.
*   **👁️ Full Observability**: Deep integration with **Langfuse** to trace every request chain, monitor latency, track token usage, and debug retrieval steps in real-time.
*   **📉 Cost-Efficient Embedding**: Utilizes optimized local **HuggingFace Embeddings** (`all-MiniLM-L6-v2`) running on CPU to eliminate embedding API costs and rate limits.
*   **🤖 Automated Evaluation Pipeline**: Includes a built-in **RAGAS** script to grade the bot's "Faithfulness" and "Relevancy" using an LLM-as-a-Judge approach.
*   **🖥️ Chat Interface**: Includes a **Streamlit** frontend for an interactive chat experience and easy document management.
*   **🚀 CI/CD Automation**: Robust **GitHub Actions** workflows that run unit tests and dependency checks on every push.
*   **🐳 Containerized Deployment**: Fully Dockerized and deployed live on **Hugging Face Spaces**.

---

## 🛠 Tech Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Backend** | **FastAPI** | High-performance, async-ready API framework. |
| **Frontend** | **Streamlit** | Interactive UI for chat and file management. |
| **LLM Engine** | **Google Gemini 2.0 Flash** | SOTA model for fast and accurate generation. |
| **Vector DB** | **Qdrant** | Hybrid setup (Local Disk / Cloud Cluster). |
| **Orchestration** | **LangChain** | Advanced chaining for retrieval and generation. |
| **Observability** | **Langfuse** | End-to-end tracing and monitoring. |
| **Evaluation** | **RAGAS** | Automated metrics calculation (Faithfulness/Relevancy). |
| **DevOps** | **Docker & GitHub Actions** | Containerization and Continuous Integration. |

---

## 🏗 Architecture

```mermaid
graph TD
    User[User / Client] -->|UI Interaction| FE[Streamlit Frontend]
    FE -->|HTTP Request| API[FastAPI Backend]
    
    subgraph "Ingestion Pipeline"
        API --> Extractor[PDF Extractor]
        Extractor --> Chunker[Text Splitter]
        Chunker --> Embedder[Local HF Embeddings]
        Embedder -->|Upsert Vectors| Qdrant[(Qdrant Hybrid DB)]
    end
    
    subgraph "RAG Pipeline"
        API --> Retriever[Retriever]
        Retriever -->|Fetch Context| Qdrant
        Retriever -->|Context + Query| LLM[Gemini 2.0 Flash]
        LLM -->|Answer| API
    end
    
    subgraph "MLOps & Monitoring"
        API -.->|Trace Data| Langfuse[Langfuse Dashboard]
        Script[Eval Script] -.->|Grade Performance| RAGAS[RAGAS Metrics]
    end
```

---

## 🚀 Live Demo

*   **API / Swagger UI**: [View API Docs](https://bestoism-rag-insight-pipeline.hf.space/docs)
    *(The backend is deployed on Hugging Face Spaces)*

---

## ⚡ Installation & Local Setup

### 1. Clone the Repository
```bash
git clone https://github.com/bestoism/rag-insight-pipeline.git
cd rag-insight-pipeline
```

### 2. Set up Virtual Environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory:
```ini
# Project Settings
PROJECT_NAME="RAG Insight Pipeline"
API_V1_STR="/api/v1"

# LLM Provider (Google Gemini)
GOOGLE_API_KEY=your_google_api_key

# Vector Database (Hybrid Config)
# Leave URL empty for Local Mode. For Cloud, fill in the details:
QDRANT_URL=
QDRANT_API_KEY=

# Observability (Langfuse)
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_HOST=https://cloud.langfuse.com
```

### 5. Run the Application
You can run the Backend and Frontend separately.

**Option A: Run Backend API**
```bash
uvicorn app.main:app --reload
```
*Access API Docs at `http://localhost:8000/docs`*

**Option B: Run Frontend UI**
```bash
streamlit run frontend/app.py
```
*Access Chat Interface at `http://localhost:8501`*

---

## 📡 API Endpoints

### 1. Ingest Document
Uploads a PDF, extracts text, chunks it, and indexes vectors.
*   **URL**: `POST /api/v1/documents/ingest`

### 2. RAG Query
Asks a question based on the indexed knowledge base.
*   **URL**: `POST /api/v1/rag/query`

### 3. Reset Memory
Clears the vector database (wipes all memory).
*   **URL**: `DELETE /api/v1/documents/reset`

---

## 🧪 Evaluation & Testing

### Running Unit Tests (CI/CD)
We use `pytest` to ensure API health and configuration integrity.
```bash
pytest tests/
```

### Running RAGAS Evaluation
To evaluate the RAG pipeline's accuracy using an automated Judge:
```bash
python scripts/run_eval.py
```

---

## 🐳 Docker & Deployment

The application is containerized using Docker and optimized for Hugging Face Spaces (Port 7860).

```bash
# Build Locally
docker build -t rag-pipeline .

# Run Container
docker run -p 7860:7860 --env-file .env rag-pipeline
```

---

**Developed by [Bestoism]**
