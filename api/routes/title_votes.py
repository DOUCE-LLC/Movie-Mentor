import pandas as pd
from fastapi import FastAPI, Response, APIRouter
import json

# Import the FastAPI framework
router = APIRouter()

# Read a CSV file containing movie data into a pandas DataFrame
df = pd.read_pickle('./data/cleaned/movies.pkl')

@router.get("/api/v1/title_votes/{title}")
def title_votes(title: str):
    # Filter the DataFrame to include only rows where the 'title' column is not null, matches the specified title,
    # and has a vote count of at least 2000
    df1 = df[df['title'].notna() & (df['title'] == title) & (df['vote_count'] >= 2000)]

    # Create a dictionary to store the data for the API response
    data = {
        "title": df1['title'].tolist()[0],
        "vote count": df1['vote_count'].tolist()[0],
        "vote average": df1['vote_average'].tolist()[0]
    }
    
    # Convert the data dictionary to a JSON string with proper indentation
    json_data = json.dumps(data, indent=4)
    
    # Create a response object with the JSON data and the appropriate media type
    response = Response(content=json_data, media_type="application/json")
    
    # Return the response object
    return response
