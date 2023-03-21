from pydantic import BaseModel
from typing import Optional
class Tag(BaseModel):
    id:int
    name:str