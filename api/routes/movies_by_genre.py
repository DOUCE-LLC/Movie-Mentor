import pandas as pd
from fastapi import FastAPI, Response, APIRouter
import json

# Import the FastAPI framework
router = APIRouter()

# Read a CSV file containing movie data into a pandas DataFrame
df = pd.read_pickle('./data/cleaned/movies.pkl')

@router.get("/api/v1/movies_by_genre/{genre}")
def movies_by_genre(genre: str):
    """
    Endpoint to retrieve popular movies of a specific genre.

    Args:
        genre (str): The genre of movies to retrieve.

    Returns:
        Response: JSON response containing the recommended movies.
    """

    # Filter the DataFrame to include only rows where the 'genres' column is not null,
    # contains the specified genre (case-insensitive), and has a vote average greater than 5
    df1 = df[df['genres'].notna() & df['genres'].str.contains(genre, case=False) & (df['vote_average'] > 5)]
    
    # Sort the filtered DataFrame by vote average in descending order
    df1 = df1.sort_values(by='vote_average', ascending=False)

    # Create a dictionary with the recommended movies
    data = {
        "title": df1['title'].tolist()
    }
    
    # Convert the data dictionary to a JSON string with proper indentation
    json_data = json.dumps(data, indent=4)
    
    # Create a response object with the JSON data and the appropriate media type
    response = Response(content=json_data, media_type="application/json")
    
    return response