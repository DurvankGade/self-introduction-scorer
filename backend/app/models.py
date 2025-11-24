from pydantic import BaseModel, Field
from typing import List, Optional

class CriterionScore(BaseModel):
    criteria: str  
    score: float
    feedback: str

class ScoreRequest(BaseModel):
    transcript: str
    # Duration is optional, if not provided, I'm considering default
    duration_sec: Optional[int] = Field(None, example=52, description="Optional duration of the speech in seconds.")

class ScoreResponse(BaseModel):
    overall_score: float
    word_count: int
    per_criterion_scores: List[CriterionScore]