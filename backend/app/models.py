from pydantic import BaseModel
from typing import List

class CriterionScore(BaseModel):
    criteria: str  
    score: float
    feedback: str

class ScoreRequest(BaseModel):
    transcript: str

class ScoreResponse(BaseModel):
    overall_score: float
    word_count: int
    per_criterion_scores: List[CriterionScore]