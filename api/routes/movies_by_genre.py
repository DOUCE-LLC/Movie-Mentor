import pandas as pd
from fastapi import FastAPI, Response, APIRouter
import json

# Import the FastAPI framework
router = APIRouter()

# Read a CSV file containing movie data into a pandas DataFrame
df = pd.read_pickle('./data/cleaned/movies.pkl')

@router.get("/api/v1/movies_by_genre/{genre}")
def movies_by_genre(genre: str):
    df1 = df[df['genres'].notna() & df['genres'].str.contains(genre, case=False) & (df['vote_average'] > 5)]
    df1 = df1.sort_values(by='vote_average', ascending=False)

    data = {
        "title": df1['title'].tolist()
    }
    
    json_data = json.dumps(data, indent=4)
    
    response = Response(content=json_data, media_type="application/json")
    
    return response