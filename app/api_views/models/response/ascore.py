from pydantic import BaseModel, Field

class ascorerisk201(BaseModel):
    status: str = Field(default="Created!", description="Status response when data has been inserted!")