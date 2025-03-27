from datetime import date
from sqlmodel import SQLModel, Field

class Character(SQLModel, table=True):
    __tablename__ = 'character'
    id: int | None = Field(default=None, primary_key=True)
    first_name: str = Field(nullable=False, max_length=50)
    last_name: str | None = Field(nullable=True, max_length=50)
    race: int = Field(nullable=False, foreign_key='race.id')
    date_of_birth: date = Field(nullable=False)
    gender: int = Field(nullable=False, foreign_key='gender.id')
    height: float = Field(nullable=False)
    weight: float = Field(nullable=False)
    hair_color: str = Field(nullable=False, max_length=200)
    eye_color: str = Field(nullable=False, max_length=10)
    blood_type: int = Field(nullable=False, foreign_key='blood_type.id')
    nationality: int = Field(nullable=False, foreign_key='nationality.id')


class Gender(SQLModel, table=True):
    __tablename__ = 'gender'
    id: int | None = Field(default=None, primary_key=True)
    chart: str = Field(nullable=False, max_length=2)
    descriptive: str = Field(nullable=False, max_length=15)


class BloodType(SQLModel, table=True):
    __tablename__ = 'blood_type'
    id: int | None = Field(default=None, primary_key=True)
    b_type: str = Field(nullable=False, max_length=3)


class Nationality(SQLModel, table=True):
    __tablename__ = 'nationality'
    id: int | None = Field(default=None, primary_key=True)
    citizenship: str = Field(nullable=False, max_length=20)
    country: str = Field(nullable=False, max_length=20)


class Race(SQLModel, table=True):
    __tablename__ = 'race'
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(nullable=False, max_length=20)