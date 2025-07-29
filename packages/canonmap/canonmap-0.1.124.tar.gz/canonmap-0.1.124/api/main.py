# File: api/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from api.routes.generation import router as generate_router
from api.routes.mapping    import router as mapping_router

app = FastAPI(
    title="CanonMap API",
    description="API for entity matching and artifact generation",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

app.include_router(
    generate_router,
    prefix="/api/v1/generate",
    tags=["generation"],
)
app.include_router(
    mapping_router,
    prefix="/api/v1/mapping",
    tags=["mapping"],
)

@app.get("/")
async def root():
    return {
        "name": "CanonMap API",
        "version": "1.0.0",
        "description": "API for entity matching and artifact generation",
        "endpoints": {
            "generate": "/api/v1/generate/",
            "mapping":  "/api/v1/mapping/",
        }
    }

if __name__ == "__main__":
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)