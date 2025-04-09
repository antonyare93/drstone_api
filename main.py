import os
import csv
import json
from sqlmodel import Session, create_engine, select, and_
from Models import *
from dotenv import load_dotenv
from fastapi import FastAPI


load_dotenv()

db_url = os.getenv('SUPABASE_URL') + os.getenv('SUPABASE_PW') + os.getenv('SUPABASE_PATH')

engine = create_engine(db_url, echo=False)

app = FastAPI()

@app.get("/api/characters")
def read_characters():
    with Session(engine) as session:
        statement = select(Character)
        return session.exec(statement).all()


@app.get("/api/characters/{character_id}")
def read_character_by_id(character_id: int):
    with Session(engine) as session:
        statement = select(Character).where(Character.id == character_id)
        return session.exec(statement).one()