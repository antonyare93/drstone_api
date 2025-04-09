from dotenv import load_dotenv
import os
from Models import *
from sqlmodel import create_engine

load_dotenv()

db_url = os.getenv('SUPABASE_URL') + os.getenv('SUPABASE_PW') + os.getenv('SUPABASE_PATH')

engine = create_engine(db_url, echo=False)


drop = True # True if need to drop tables and create them again; False to skip dropping
if drop:
    SQLModel.metadata.drop_all(engine)
SQLModel.metadata.create_all(engine)