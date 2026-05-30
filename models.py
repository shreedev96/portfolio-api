from sqlalchemy import Column,Integer,String,Float
from  database import Base

class DBInvestment(Base):
    __tablename__="investments"

    id=Column(Integer,primary_key=True,index=True)
    name=Column(String,index=True)
    investment_type=Column(String)
    amount=Column(Float)