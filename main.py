from fastapi import FastAPI
from routers.preprocess_router import router as preprocess_router

app = FastAPI()
app.include_router(preprocess_router)

@app.get("/")
async def home():
    return {"status": "API Running"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)