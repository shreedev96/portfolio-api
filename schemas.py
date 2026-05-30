from pydantic import BaseModel,Field

class Investment(BaseModel):
    name:str
    type:str
    amount:float=Field(...,gt=0,description="You cannot add negative or zero amounts !")