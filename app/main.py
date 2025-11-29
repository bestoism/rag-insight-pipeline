from fastapi import FastAPI
from app.core.config import settings

# Initialize FastAPI App
app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    docs_url="/docs", # Swagger UI URL
    redoc_url="/redoc"
)

# Health Check Endpoint
@app.get("/")
def health_check():
    return {
        "status": "healthy",
        "project": settings.PROJECT_NAME,
        "version": "1.0.0"
    }


if __name__ == "__main__":
    import uvicorn
    # Jalankan server untuk debugging lokal
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)