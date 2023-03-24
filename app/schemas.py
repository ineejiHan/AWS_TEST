from typing import List,Optional
from pydantic import BaseModel

class TageItem(BaseModel):
    name: str
    unit: Optional[str] = None
    description: Optional[str] = None

class EquipItem(BaseModel):
    id:Optional[int] =None
    name: str
    input: Optional[List[int]] = None
    output: Optional[List[int]] = None
    internal: Optional[List[int]] = None
    description: Optional[str] = None
