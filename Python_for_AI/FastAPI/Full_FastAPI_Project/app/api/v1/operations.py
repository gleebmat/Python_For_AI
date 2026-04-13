from fastapi import FastAPI, APIRouter, HTTPException
from app.schemas import OperationRequest
from app.service import operations as operations_service
from app.dependency import get_db
from sqlalchemy.orm import Session
from fastapi import Depends

router = APIRouter()


@router.post("/operations/income")
def add_income(operation: OperationRequest, db: Session = Depends(get_db)):
    return operations_service.add_income(db, operation)


@router.post("/operations/expenses")
def add_expense(operation: OperationRequest, db: Session = Depends(get_db)):
    return operations_service.add_expense(db, operation)
