from pydantic import BaseModel

class SentimentPayloadSchema(BaseModel):
    content: str
    description: str