import os
import csv
import json
from sqlmodel import Session, create_engine, select, and_
from Models import *
from dotenv import load_dotenv
from sqlalchemy import inspect


load_dotenv()

db_url = os.getenv('SUPABASE_URL') + os.getenv('SUPABASE_PW') + os.getenv('SUPABASE_PATH')

engine = create_engine(db_url, echo=False)


def migrate_data():
    files = ['gender', 'race', 'country', 'place', 'blood_type', 'character']
    Classes = {'gender': Gender, 'race': Race, 'country': Country, 'place': Place, 'blood_type': BloodType, 'character': Character}

    for file in files:
        with open(f'./json_files/{file}.json', 'r') as f:
            data = json.load(f)

        with Session(engine) as session:
            for row in data:
                i = Classes[file](**row)
                inspector = inspect(Classes[file])
                primary_key_columns = [col.name for col in inspector.primary_key]
                conditions = []
                for key, value in row.items():
                    if key not in primary_key_columns and value is not None:
                        conditions.append(getattr(Classes[file], key) == value)
                statement = select(Classes[file]).where(and_(*conditions))
                result = session.exec(statement).first()
                if not result:
                    session.add(i)


            session.commit()

def csv_to_json(csv_file_path, json_file_path=None):
    # Read the CSV file
    with open(csv_file_path, 'r') as csvfile:
        # Use DictReader to convert each row into a dictionary
        csvreader = csv.DictReader(csvfile)

        # Convert rows to a list of dictionaries
        data = list(csvreader)

    # Convert to JSON
    json_data = json.dumps(data, indent=2)

    # If a JSON file path is provided, write to file
    if json_file_path:
        with open(json_file_path, 'w') as jsonfile:
            jsonfile.write(json_data)
        print(f"JSON file saved to {json_file_path}")
        return None

    # Otherwise, return the JSON string
    return json_data


# Example usage
if __name__ == "__main__":

    files = ['gender', 'race', 'country', 'place', 'blood_type', 'character']
    # Convert CSV to JSON and save to a file
    for file in files:
        csv_to_json(f'./migrations/{file}.csv', f'./migrations/json_files/{file}.json')

    migrate_data()