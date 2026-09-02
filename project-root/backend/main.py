from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from typing import List

import models
import schemas
import database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="API de Indicadores de Funcionários")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/records", response_model=schemas.RecordOut)
def create_record(record: schemas.RecordCreate, db: Session = Depends(database.get_db)):
    try:
        employee = db.query(models.Employee).filter(
            models.Employee.name == record.employee_name,
            models.Employee.department == record.department
        ).first()

        if not employee:
            employee = models.Employee(name=record.employee_name, department=record.department)
            db.add(employee)
            db.commit()
            db.refresh(employee)

        new_record = models.Record(
            employee_id=employee.id,
            reference_date=record.reference_date,
            deliveries=record.deliveries,
            note=record.note
        )
        db.add(new_record)
        db.commit()
        db.refresh(new_record)
        
        return new_record

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno ao salvar no banco de dados."
        )

@app.get("/records", response_model=List[schemas.RecordOut])
def get_records(db: Session = Depends(database.get_db)):
    try:
        return db.query(models.Record).order_by(models.Record.reference_date.desc()).all()
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Erro ao buscar registros.")

@app.get("/summary")
def get_summary(db: Session = Depends(database.get_db)):
    try:
        total_records = db.query(models.Record).count()
        total_deliveries = db.query(func.sum(models.Record.deliveries)).scalar() or 0
        
        dept_deliveries = db.query(
            models.Employee.department, 
            func.sum(models.Record.deliveries).label('total')
        ).join(models.Record).group_by(models.Employee.department).all()

        chart_data = [{"department": dept, "deliveries": total} for dept, total in dept_deliveries]

        return {
            "total_records": total_records,
            "total_deliveries": total_deliveries,
            "chart_data": chart_data
        }
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Erro ao gerar o resumo.")

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "API rodando perfeitamente"}