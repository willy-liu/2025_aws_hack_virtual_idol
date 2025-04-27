from pydantic import BaseModel

class ResponseInput(BaseModel):
    above: str
    below: str