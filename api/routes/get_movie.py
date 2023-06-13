import pandas as pd
from fastapi import FastAPI, Response, APIRouter
import json

# Import the FastAPI framework
router = APIRouter()
 
# # Read a CSV file containing movie data into a pandas DataFrame
df = pd.read_pickle('./data/cleaned/movies.pkl')

@router.get("/api/v1/movie/{title}")
def get_movie(title: str):
    df1 = df[df['title'] == title]
    
    # Create the data dictionary with the updated movies list
    data = {
        "title": title,
        "release_year": pd.to_datetime(df1['release_date'].tolist()[0]).year,
        "overview": df1['overview'].tolist()[0],
        "popularity": df1['popularity'].tolist()[0],
        "vote average": df1['vote_average'].tolist()[0],
        "vote count": df1['vote_count'].tolist()[0],
        "budget": df1['budget'].tolist()[0],
        "revenue": df1['revenue'].tolist()[0],
        "ROI": df1['ROI'].tolist()[0],
        "cast": df1['cast'].tolist()[0].replace("'", "").replace('"', "").replace("[", "").replace("]", "").split(", "),
        "crew": df1['crew'].tolist()[0].replace("'", "").replace('"', "").replace("[", "").replace("]", "").split(", ")
    }
    
    json_data = json.dumps(data, indent=4)
    response = Response(content=json_data, media_type="application/json")
    
    return response