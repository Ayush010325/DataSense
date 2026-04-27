from pydantic import BaseModel

class Insight(BaseModel):
    message: str
    severity: str
    category: str
