import os
from datetime import date
from typing import Optional, List
from sqlmodel import Session, create_engine, select
from Models import *
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from mangum import Mangum
from pydantic import BaseModel


# Response Models
class GenderResponse(BaseModel):
    chart: str
    descriptive: str

    class Config:
        from_attributes = True

class CountryResponse(BaseModel):
    country: str
    citizenship: str

    class Config:
        from_attributes = True

class PlaceResponse(BaseModel):
    name: str
    country: CountryResponse = None

    class Config:
        from_attributes = True

class BloodTypeResponse(BaseModel):
    b_type: str

    class Config:
        from_attributes = True

class RaceResponse(BaseModel):
    name: str

    class Config:
        from_attributes = True


class CharacterResponse(BaseModel):
    id: Optional[int] = None
    first_name: str
    last_name: Optional[str] = None
    race: RaceResponse = None
    date_of_birth: date
    gender: GenderResponse = None
    height: float
    weight: float
    hair_color: str
    eye_color: str
    blood_type: BloodTypeResponse = None
    birth_place: PlaceResponse = None
    img_face: Optional[str] = None
    img_body: Optional[str] = None

    class Config:
        from_attributes = True


class PaginatedCharacterResponse(BaseModel):
    total: int
    page: int
    page_size: int
    items: List[CharacterResponse]

load_dotenv()

db_url = os.getenv('SUPABASE_URL') + os.getenv('SUPABASE_PW') + os.getenv('SUPABASE_PATH')

engine = create_engine(db_url, echo=False)

app = FastAPI(
    title="Dr. Stone API",
    description="API for accessing Dr. Stone information",
    version="1.0.0"
)

@app.get("/api/characters", response_model=PaginatedCharacterResponse)
async def read_characters(
    page: int = Query(default=1, ge=1, description="Page number"),
    page_size: int = Query(default=50, ge=1, le=100, description="Number of items per page")
):
    """
    Get a paginated array of characters.
    
    Parameters:
    - page: Page number (starts from 1)
    - page_size: Number of items per page (1-100)
    """
    try:
        with Session(engine) as session:
            # Get total count
            total_count = session.exec(select(Character)).all().__len__()
            
            # Calculate offset
            offset = (page - 1) * page_size
            
            # Get paginated results with race information
            statement = (
                select(Character, Race, BloodType, Gender, Place, Country)
                .join(Race)
                .join(BloodType)
                .join(Gender)
                .join(Place)
                .join(Country)
                .offset(offset)
                .limit(page_size)
            )
            results = session.exec(statement).all()
            
            characters = []
            for char, race, bType, gender, place, country in results:
                char_dict = char.model_dump()
                char_dict['race'] = race
                char_dict['blood_type'] = bType
                char_dict['gender'] = gender
                place_dict = place.model_dump()
                place_dict['country'] = country
                char_dict['birth_place'] = place_dict
                characters.append(CharacterResponse(**char_dict))
            
            return PaginatedCharacterResponse(
                total=total_count,
                page=page,
                page_size=page_size,
                items=characters
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/characters/{character_id}", response_model=CharacterResponse)
async def read_character_by_id(character_id: int):
    """Get a specific character by id"""
    try:
        with Session(engine) as session:
            statement = (
                select(Character, Race, BloodType, Gender, Place, Country)
                .join(Race)
                .join(BloodType)
                .join(Gender)
                .join(Place)
                .join(Country)
                .where(Character.id == character_id))
            result = session.exec(statement).first()
            
            if not result:
                raise HTTPException(status_code=404, detail=f"Character with id {character_id} not found")
            
            char, race, bType, gender, place, country = result
            char_dict = char.model_dump()
            char_dict['race'] = race
            char_dict['blood_type'] = bType
            char_dict['gender'] = gender
            place_dict = place.model_dump()
            place_dict['country'] = country
            char_dict['birth_place'] = place_dict
            return CharacterResponse(**char_dict)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


handler = Mangum(app)
