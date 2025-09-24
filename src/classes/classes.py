from typing import List, Literal, TypedDict
from pydantic import BaseModel
from typing import Optional

class TestResult(BaseModel):
    test_passed: bool
    error: Optional[str] = None

class StepResultArray(BaseModel):
    sesion_id: str
    act_id: str
    num_steps_executed: int
    prompt: str
    parsed_step: TestResult


class Prompt(TypedDict):
    step: str
    type: Literal["input", "none"] 