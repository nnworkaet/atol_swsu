from pydantic import BaseModel


class Inputdata(BaseModel):
    port: str
    receiptBody: dict
