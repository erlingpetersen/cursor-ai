from pydantic import BaseModel

class Plato(BaseModel):
    id: int
    name: str
    precio: float 