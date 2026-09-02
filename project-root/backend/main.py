from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List

import models
import schemas
import database

# Cria as tabelas no banco de dados assim que a aplicação iniciar
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="API de Indicadores de Funcionários")

# Configuração de CORS para permitir que Angular e React conversem com a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/records", response_model=schemas.RecordOut)
def create_record(record: schemas.RecordCreate, db: Session = Depends(database.get_db)):
    # Busca ou cria o funcionário
    employee = db.query(models.Employee).filter(
        models.Employee.name == record.employee_name,
        models.Employee.department == record.department
    ).first()

    if not employee:
        employee = models.Employee(name=record.employee_name, department=record.department)
        db.add(employee)
        db.commit()
        db.refresh(employee)

    # Cria o registro de entregas.
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

@app.get("/records", response_model=List[schemas.RecordOut])
def get_records(db: Session = Depends(database.get_db)):
    # Retorna todos os registros ordenados pela data de referência (mais recentes primeiro)
    records = db.query(models.Record).order_by(models.Record.reference_date.desc()).all()
    return records

@app.get("/summary")
def get_summary(db: Session = Depends(database.get_db)):
    # Totais para os "cartões de resumo" do React
    total_records = db.query(models.Record).count()
    total_deliveries = db.query(func.sum(models.Record.deliveries)).scalar() or 0
    
    # Agrupa a quantidade de entregas por departamento para o gráfico
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