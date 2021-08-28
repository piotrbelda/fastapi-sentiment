from pydantic import BaseModel


class SentimentPayloadSchema(BaseModel):
    content: str
    description: str


class SentimentResponseSchema(SentimentPayloadSchema):
    id: int

class SentimentUpdatePayloadSchema(SentimentPayloadSchema):
    sentiment: bool