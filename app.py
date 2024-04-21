import os
import uvicorn

from fastapi import FastAPI
from fastapi.responses import Response
from starlette.responses import RedirectResponse

from instamarket.pipeline.prediction import PredictionPipeline

app = FastAPI()

@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def training():
    try:
        os.system("python main_pipeline.py")
        return Response("Training Succcessful!!")
    except Exception as e:
        return Response(f"Error Ocuirred: {e}")

@app.post("/predict")
async def prediction(store:str, optimal_start_time:str, optimal_end_time:str):
    try:
        obj = PredictionPipeline()
        delays = obj.predict(store, optimal_start_time, optimal_end_time)
        return {"start_delay": float(delays[0][0]),
                "end_delay": float(delays[0][1])}
    except Exception as e:
        raise e
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)