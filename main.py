from fastapi import FastAPI
from routers.preprocess_router import router as preprocess_router


app = FastAPI()
app.include_router(preprocess_router)

from fastapi.middleware.cors import CORSMiddleware


# Add this middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
async def home():
    return {"status": "API Running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)