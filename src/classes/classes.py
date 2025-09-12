from typing import List, Literal, TypedDict
from pydantic import BaseModel
from typing import Optional

class TestResult(BaseModel):
    test_passed: bool
    error: Optional[str] = None

class Prompt(TypedDict):
    step: str
    type: Literal["input", "none"] 