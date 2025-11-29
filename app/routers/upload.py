from fastapi import APIRouter, UploadFile, File, HTTPException
from app.ingestion.extractor import extract_text_from_file
from app.ingestion.embedder import index_document # <--- Import baru

router = APIRouter()

@router.post("/ingest", summary="Upload document for ingestion")
async def ingest_document(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(('.pdf', '.txt')):
        raise HTTPException(status_code=400, detail="Only PDF and TXT files are supported")
    
    try:
        content = await file.read()
        extracted_text = extract_text_from_file(content, file.filename)
        
        if not extracted_text:
            raise HTTPException(status_code=400, detail="Failed to extract text")
            
        # --- PROSES BARU: Indexing ke Qdrant ---
        num_chunks = await index_document(extracted_text, file.filename)
        
        return {
            "filename": file.filename,
            "status": "success",
            "message": f"Successfully indexed {num_chunks} chunks to Vector DB",
        }

    except Exception as e:
        print(f"Error: {e}") # Debugging
        raise HTTPException(status_code=500, detail=str(e))