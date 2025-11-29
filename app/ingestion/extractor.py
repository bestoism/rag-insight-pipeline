from typing import Optional
from io import BytesIO
from pypdf import PdfReader

def extract_text_from_pdf(file_content: bytes) -> Optional[str]:
    try:
        pdf_reader = PdfReader(BytesIO(file_content))
        text = ""
        
        # Cek apakah PDF terenkripsi
        if pdf_reader.is_encrypted:
            print("❌ Error: PDF is encrypted/password protected.")
            return None

        count = 0
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
                count += 1
        
        # Debugging: Cek apakah teks kosong
        if not text.strip():
            print("⚠️ Warning: PDF opened successfully but NO TEXT found. It might be a scanned image.")
            return None
            
        print(f"✅ Extracted text from {count} pages.")
        return text.strip()
    
    except Exception as e:
        # Ini akan muncul di Logs Hugging Face
        print(f"❌ CRITICAL ERROR in extraction: {e}")
        return None

def extract_text_from_file(file_content: bytes, filename: str) -> Optional[str]:
    if filename.lower().endswith(".pdf"):
        return extract_text_from_pdf(file_content)
    elif filename.lower().endswith(".txt"):
        return file_content.decode("utf-8")
    else:
        print(f"❌ Unsupported format: {filename}")
        return None