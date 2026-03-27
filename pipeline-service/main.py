from fastapi import FastAPI, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from database import engine, get_db, Base
from models.customer import Customer
from services.ingestion import ingest_data

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Pipeline Service API")

@app.post("/api/ingest")
def ingest(db: Session = Depends(get_db)):
    try:
        records_processed = ingest_data(db)
        return {"status": "success", "records_processed": records_processed}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/customers")
def get_customers(page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=100), db: Session = Depends(get_db)):
    skip = (page - 1) * limit
    total = db.query(Customer).count()
    customers = db.query(Customer).offset(skip).limit(limit).all()
    
    return {
        "data": customers,
        "total": total,
        "page": page,
        "limit": limit
    }

@app.get("/api/customers/{customer_id}")
def get_customer(customer_id: str, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer
