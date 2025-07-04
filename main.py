from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from schemas import Plato
from settings import Settings

settings = Settings()

app = FastAPI(
    title=settings.app_title,
    description=settings.app_description,
    version=settings.app_version,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory database simulation
platos_db: List[Plato] = [
    Plato(id=1, name="Milanesa con papas", precio=12.5),
    Plato(id=2, name="Ensalada César", precio=9.0),
    Plato(id=3, name="Pizza Margarita", precio=15.0),
    Plato(id=4, name="Sopa de tomate", precio=7.5),
    Plato(id=5, name="Hamburguesa clásica", precio=13.0),
    Plato(id=6, name="Tacos al pastor", precio=11.0),
    Plato(id=7, name="Paella valenciana", precio=18.0),
    Plato(id=8, name="Pollo al curry", precio=14.0),
    Plato(id=9, name="Sushi variado", precio=20.0),
    Plato(id=10, name="Lasaña de carne", precio=16.5),
]
plato_id_counter = 11

def get_next_plato_id() -> int:
    """Get the next available Plato ID and increment the counter."""
    global plato_id_counter
    next_id = plato_id_counter
    plato_id_counter += 1
    return next_id

@app.get("/platos", response_model=List[Plato], summary="List all dishes")
def listar_platos() -> List[Plato]:
    """Return the list of all dishes."""
    return platos_db

@app.get("/platos/{plato_id}", response_model=Plato, summary="Get a dish by ID")
def obtener_plato(plato_id: int) -> Plato:
    """Return a dish by its ID."""
    for plato in platos_db:
        if plato.id == plato_id:
            return plato
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dish not found")

@app.post("/platos", response_model=Plato, status_code=status.HTTP_201_CREATED, summary="Create a new dish")
def crear_plato(plato: Plato) -> Plato:
    """Create a new dish and add it to the database."""
    new_plato = Plato(id=get_next_plato_id(), name=plato.name, precio=plato.precio)
    platos_db.append(new_plato)
    return new_plato

@app.put("/platos/{plato_id}", response_model=Plato, summary="Update an existing dish")
def actualizar_plato(plato_id: int, plato: Plato) -> Plato:
    """Update the data of an existing dish."""
    for idx, existing_plato in enumerate(platos_db):
        if existing_plato.id == plato_id:
            updated_plato = Plato(id=plato_id, name=plato.name, precio=plato.precio)
            platos_db[idx] = updated_plato
            return updated_plato
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dish not found")

@app.delete("/platos/{plato_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a dish")
def eliminar_plato(plato_id: int) -> None:
    """Delete a dish from the database."""
    for idx, plato in enumerate(platos_db):
        if plato.id == plato_id:
            platos_db.pop(idx)
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dish not found")

@app.get("/", summary="Welcome")
def root():
    """Welcome endpoint."""
    return {"message": "Welcome to FastAPI App!", "status": "running"}

@app.get("/health", summary="Health check")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": settings.app_version}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.host, port=settings.port, reload=settings.debug) 