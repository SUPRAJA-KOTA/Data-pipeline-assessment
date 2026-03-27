import requests
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from models.customer import Customer
from datetime import datetime
import os

def ingest_data(db: Session):
    page = 1
    limit = 10
    base_url = os.getenv("MOCK_SERVER_URL", "http://mock-server:5000/api/customers")
    records_processed = 0
    
    while True:
        try:
            response = requests.get(base_url, params={"page": page, "limit": limit})
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch data from mock server: {str(e)}")
            
        data = response.json()
        customers = data.get("data", [])
        
        if not customers:
            break
            
        for c in customers:
            # Parse dates
            dob = None
            if c.get('date_of_birth'):
                try:
                    dob = datetime.strptime(c['date_of_birth'], "%Y-%m-%d").date()
                except ValueError:
                    pass
                    
            created_at = None
            if c.get('created_at'):
                try:
                    created_str = c['created_at'].replace('Z', '+00:00')
                    created_at = datetime.fromisoformat(created_str).replace(tzinfo=None)
                except ValueError:
                    pass

            stmt = insert(Customer).values(
                customer_id=c['customer_id'],
                first_name=c['first_name'],
                last_name=c['last_name'],
                email=c['email'],
                phone=c.get('phone'),
                address=c.get('address'),
                date_of_birth=dob,
                account_balance=c.get('account_balance'),
                created_at=created_at
            )
            
            upsert_stmt = stmt.on_conflict_do_update(
                index_elements=['customer_id'],
                set_={
                    'first_name': stmt.excluded.first_name,
                    'last_name': stmt.excluded.last_name,
                    'email': stmt.excluded.email,
                    'phone': stmt.excluded.phone,
                    'address': stmt.excluded.address,
                    'date_of_birth': stmt.excluded.date_of_birth,
                    'account_balance': stmt.excluded.account_balance,
                    'created_at': stmt.excluded.created_at
                }
            )
            
            db.execute(upsert_stmt)
            records_processed += 1
            
        db.commit()
        
        if len(customers) < limit:
            break
        page += 1
        
    return records_processed
