from fastapi import FastAPI
from app.model import analyze_sentiment
from app.schemas import AnalyzeRequest, SentimentResponse


app = FastAPI(
    title="Sentiment Analysis API",
    description="API for analyzing sentiment of English text.",
    version="1.0.0"
)


@app.get("/api/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.post("/api/analyze", response_model=SentimentResponse)
def analyze(request: AnalyzeRequest):
    result = analyze_sentiment(request.text)

    return {
        "text": request.text,
        "sentiment": result["sentiment"],
        "confidence": result["confidence"]
    }
from app.schemas import (
    AnalyzeRequest,
    SentimentResponse,
    BatchAnalyzeRequest,
    BatchSentimentResponse
)
@app.post("/api/analyze/batch", response_model=BatchSentimentResponse)
def analyze_batch(request: BatchAnalyzeRequest):
    results = []

    for text in request.texts:
        result = analyze_sentiment(text)

        results.append({
            "text": text,
            "sentiment": result["sentiment"],
            "confidence": result["confidence"]
        })

    return {
        "results": results
    }