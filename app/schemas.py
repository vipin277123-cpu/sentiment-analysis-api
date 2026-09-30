from pydantic import BaseModel, Field, field_validator


class AnalyzeRequest(BaseModel):
    text: str = Field(..., min_length=1)

    @field_validator("text")
    @classmethod
    def validate_word_count(cls, value):
        word_count = len(value.split())

        if word_count > 500:
            raise ValueError("Text must not exceed 500 words.")

        return value


class SentimentResponse(BaseModel):
    text: str
    sentiment: str
    confidence: float


class BatchAnalyzeRequest(BaseModel):
    texts: list[str] = Field(..., min_length=1, max_length=10)

    @field_validator("texts")
    @classmethod
    def validate_texts(cls, values):
        for text in values:
            if not text.strip():
                raise ValueError("Text items cannot be empty.")

            word_count = len(text.split())

            if word_count > 500:
                raise ValueError("Each text must not exceed 500 words.")

        return values


class BatchSentimentResponse(BaseModel):
    results: list[SentimentResponse]