from fastapi import FastAPI
from .models import ScoreRequest, ScoreResponse, CriterionScore

# Create the FastAPI app instance
app = FastAPI(
    title="Transcript Scoring API",
    description="An API to score student self-introduction transcripts based on rubrics.",
    version="1.0.0"
)

# Define the /score endpoint
@app.post("/score", response_model=ScoreResponse)
async def score_transcript(request: ScoreRequest):
    """
    Accepts a transcript text and returns a rubric-based score.

    - **transcript**: The student's self-introduction text.
    """
    # --- DUMMY LOGIC (to be replaced in Step 4) ---

    # 1. Calculate word count (this is a real calculation)
    word_count = len(request.transcript.split())

    # 2. Create placeholder scores for each criterion
    dummy_scores = [
        CriterionScore(criteria="Content & Structure", score=8.5, feedback="Good structure, but could include more details about goals."),
        CriterionScore(criteria="Speech Rate", score=10.0, feedback="Ideal speech rate."),
        CriterionScore(criteria="Language & Grammar", score=7.0, feedback="Minor grammatical errors found."),
        CriterionScore(criteria="Clarity", score=9.0, feedback="Very few filler words used."),
        CriterionScore(criteria="Engagement", score=8.0, feedback="Positive and engaging tone.")
    ]

    # 3. Calculate a dummy overall score
    overall_score = sum(s.score for s in dummy_scores) / len(dummy_scores) * 10 # Scale to 100

    # --- END OF DUMMY LOGIC ---

    # Return the response object that matches the ScoreResponse model
    return ScoreResponse(
        overall_score=overall_score,
        word_count=word_count,
        per_criterion_scores=dummy_scores
    )

@app.get("/")
def read_root():
    return {"message": "Welcome to the Transcript Scoring API. Use the /score endpoint to get started."}