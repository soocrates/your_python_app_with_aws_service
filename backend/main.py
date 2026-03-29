from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
import models
from routers import auth, applications

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="ATS-lite API")

origins = [
    "http://localhost:5173", # Default Vite
    "http://localhost:3000", # Default CRA
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(applications.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to ATS-lite API"}
