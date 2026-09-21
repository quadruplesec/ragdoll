from pydantic import BaseModel

class AskRequest(BaseModel):
    query: str

class AskResponse(BaseModel):
    answer: str

class IngestRequest(BaseModel):
    text: str

class IngestResponse(BaseModel):
    status: str