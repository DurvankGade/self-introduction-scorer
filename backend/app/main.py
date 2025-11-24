from fastapi import FastAPI
from .models import ScoreRequest, ScoreResponse, CriterionScore
from .logic.scoring_config import scoring_guide_data

app = FastAPI(
    title="Transcript Scoring API",
    description="API for scoring student self-introductions using a predefined rubric.",
    version="1.0.0"
)

# Confirm rubric was loaded correctly
if scoring_guide_data:
    print("Scoring configuration loaded successfully.")
    import json
    print(json.dumps(scoring_guide_data, indent=2))
else:
    print("ERROR: Scoring configuration is missing.")

@app.post("/score", response_model=ScoreResponse)
async def score_transcript(request: ScoreRequest):
    word_count = len(request.transcript.split())

    # Temporary placeholder scores until scoring logic is added
    dummy_scores = [
        CriterionScore(criteria="Content & Structure", score=8.5, feedback="Good structure."),
        CriterionScore(criteria="Speech Rate", score=10.0, feedback="Ideal speech rate."),
        CriterionScore(criteria="Language & Grammar", score=7.0, feedback="Some minor grammatical issues."),
        CriterionScore(criteria="Clarity", score=9.0, feedback="Clear and concise delivery."),
        CriterionScore(criteria="Engagement", score=8.0, feedback="Friendly and engaging tone.")
    ]

    overall_score = 85.0

    return ScoreResponse(
        overall_score=overall_score,
        word_count=word_count,
        per_criterion_scores=dummy_scores
    )

@app.get("/")
def read_root():
    return {"message": "Welcome to the Transcript Scoring API."}
