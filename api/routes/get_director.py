import pandas as pd
from fastapi import FastAPI, Response, APIRouter
import json

# Import the FastAPI framework
router = APIRouter()
 
# # Read a CSV file containing movie data into a pandas DataFrame
df = pd.read_pickle('./data/cleaned/movies.pkl')

@router.get("/api/v1/director/{director}")
def get_director(director: str):
    """
    Endpoint to retrieve information about movies directed by a specific director.

    Args:
        director (str): The name of the director.

    Returns:
        Response: JSON response containing information about the director's movies.
    """
    
    # Filter the DataFrame to include only rows where the 'crew' column is not null and contains the specified director
    df1 = df[df['crew'].notna() & df['crew'].str.contains(director)]
    
    # Create a list to store the movie objects
    movies = []
    
    # Iterate over the rows in the filtered DataFrame
    for _, row in df1.iterrows():
        # Create a dictionary for each movie with the desired information
        movie = {
            "title": row['title'],
            "release_year": pd.to_datetime(row['release_date']).year,
            "overview": row['overview'],
            "budget": row['budget'],
            "revenue": row['revenue'],
            "ROI": row['ROI'],
            "cast": row['cast'].replace("'", "").replace('"', "").replace("[", "").replace("]", "").split(", "),
            "crew": row['crew'].replace("'", "").replace('"', "").replace("[", "").replace("]", "").split(", ")
        }
        # Append the movie dictionary to the movies list
        movies.append(movie)
    
    # Calculate the total revenue and total movies as before
    revenue = df1['revenue'].sum()
    roi = df1['ROI'].mean()
    movies_count = df1.shape[0]
    
    # Create the data dictionary with the updated movies list
    data = {
        "name": director,
        "total movies": movies_count,
        "total revenue": revenue,
        "average ROI": roi,
        "movies": movies
    }

    # Convert the data dictionary to JSON format
    json_data = json.dumps(data, indent=4)

    # Create a JSON response with the JSON data
    response = Response(content=json_data, media_type="application/json")
    
    return response