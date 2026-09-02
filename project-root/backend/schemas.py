from pydantic import BaseModel, Field, ConfigDict
from datetime import date, datetime
from typing import Optional

class RecordCreate(BaseModel):
    employee_name: str
    department: str
    reference_date: date
    deliveries: int = Field(..., ge=0, description="Quantidade não pode ser negativa")
    note: Optional[str] = None

class EmployeeOut(BaseModel):
    id: int
    name: str
    department: str

    model_config = ConfigDict(from_attributes=True)

class RecordOut(BaseModel):
    id: int
    reference_date: date
    deliveries: int
    note: Optional[str]
    created_at: datetime
    employee: EmployeeOut

    model_config = ConfigDict(from_attributes=True)