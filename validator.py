from pydantic import BaseModel, validator
from typing import Literal

class StructuredDataModel(BaseModel):
    file_path: str
    second_file_path : str | None
    operation: Literal['basic-math', 'aggregation', 'joins','pivot','date-operations']
    query: str
    
    @validator('operation')
    def operation_must_be_valid(cls, v):
        valid_operations = {'basic-math', 'aggregation', 'joins','pivot','date-operations'}
        if v not in valid_operations:
            raise ValueError(f'Invalid operation. Choose from {valid_operations}')
        return v

class UnstructuredDataModel(BaseModel):
    file_path: str
    query: str
