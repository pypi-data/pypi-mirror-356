from pydantic import BaseModel


class TestCycleAttributes(BaseModel):
    folder: str
    test_cycle_status: str
    test_case_test_type: str
    cycles_number: int


class TestCycleRequest(BaseModel):
    summary: str
    description: str
    space: str
    attributes: TestCycleAttributes
