from fastapi import FastAPI,HTTPException,Depends
from fastapi.responses import StreamingResponse
import schemas
import models
from sqlalchemy.orm import Session
from database import SessionLocal,engine
import io
import csv

models.Base.metadata.create_all(bind=engine)


app = FastAPI()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()    

@app.get("/")
def read_root():
    return {"message": "Welcome to the Investment Portfolio API!"}

@app.post("/investment")
def create_investment(new_investment:schemas.Investment,db:Session=Depends(get_db)):
    db_item=models.DBInvestment(name=new_investment.name,
                                investment_type=new_investment.type,
                                amount=new_investment.amount)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)  
    return{
        "message":"Investment Received Successfully",
        "data":db_item
    }
@app.get("/investment/exportToCsv")
def get_investments_csv(db:Session=Depends(get_db)):
    db_items=db.query(models.DBInvestment).all()

    output=io.StringIO()
    writer=csv.writer(output)

    writer.writerow(["Investment ID","Name","Type","Amount"])

    for item in db_items:
        writer.writerow([item.id,item.name,item.investment_type,item.amount])

    output.seek(0)

    headers={
        'Content-Disposition':'attachment; filename="portfolio-summary.csv"' 
    }    

    return StreamingResponse(output,media_type="text/csv",headers=headers)
@app.get("/investment/getAll")
def show_all(db:Session=Depends(get_db)):
    db_items=db.query(models.DBInvestment).all()
    return {"investments":db_items}

@app.get("/investment/{investment_id}")
def get_an_investment(investment_id:int,db:Session=Depends(get_db)):
    db_item=db.query(models.DBInvestment).filter(models.DBInvestment.id==investment_id).first()
    if db_item is None:
        raise HTTPException(status_code=404,detail="Investment not found")
    
    return db_item

@app.delete("/investment/delete/{investment_id}")
def delete_investment(investment_id:int,db:Session=Depends(get_db)):
    db_item=db.query(models.DBInvestment).filter(models.DBInvestment.id==investment_id).first()
    if db_item is None:
        raise HTTPException(status_code=404,detail=f"Couldn't find an investment of the id {investment_id}")
    db.delete(db_item)
    db.commit()

    return {"message":"Deleted the investment",
            "investment":db_item}

@app.put("/investment/update/{investment_id}")
def update_investment(investment_id:int,updated_investment:schemas.Investment,db:Session=Depends(get_db)):
    db_item=db.query(models.DBInvestment).filter(models.DBInvestment.id==investment_id).first()
    if db_item is None:
        raise HTTPException(status_code=404,detail=f"Investment with id {investment_id} is not found ")
    db_item.name=updated_investment.name
    db_item.investment_type=updated_investment.type
    db_item.amount=updated_investment.amount

    db.commit()
    db.refresh(db_item)
    return {"message":f"Investment with id {investment_id} updated with {updated_investment}"
            }

