from pydantic import BaseModel

class PerplexityInput(BaseModel):
    prompt: str
