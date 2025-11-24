from fastapi import FastAPI
from .models import ScoreRequest, ScoreResponse, CriterionScore
from fastapi.middleware.cors import CORSMiddleware
from .logic.scoring import calculate_scores

app = FastAPI(
    title="Transcript Scoring API",
    description="API for scoring student self-introductions using a predefined rubric.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

@app.post("/score", response_model=ScoreResponse)
async def score_transcript(request: ScoreRequest):
    # --- REPLACE DUMMY LOGIC WITH REAL LOGIC ---
    
    # 1. Call the main scoring orchestrator
    per_criterion_results, overall_score, word_count = calculate_scores(
        transcript=request.transcript,
        duration_sec=request.duration_sec
    )
    
    # 2. Format the results into the Pydantic response model
    criterion_scores = [
        CriterionScore(
            criteria=criterion,
            score=result['score'],
            feedback=result['feedback']
        )
        for criterion, result in per_criterion_results.items()
    ]
    
    return ScoreResponse(
        overall_score=round(overall_score, 2),
        word_count=word_count,
        per_criterion_scores=criterion_scores
    )

@app.get("/")
def read_root():
    return {"message": "Welcome to the Transcript Scoring API."}