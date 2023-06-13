import pandas as pd
from fastapi import FastAPI, Response, APIRouter
import json

# Import the FastAPI framework
router = APIRouter()
 
# Read a CSV file containing movie data into a pandas DataFrame
df = pd.read_pickle('./data/cleaned/movies.pkl')

@router.get("/api/v1/shoots_per_day/{day}")
def shoots_per_day(day: int):
    """
    Endpoint to retrieve the number of movies released on a specific day.

    Args:
        day (int): The day of the month.

    Returns:
        Response: JSON response containing the number of movies released on the specified day.
    """

    # Filter the DataFrame to include only movies released on the specified day
    df1 = df[pd.to_datetime(df["release_date"]).dt.day == day]
    
    # Create a dictionary to store the data for the API response
    data = {
        "day": day,
        "total movies": df1.shape[0]
    }
    
    # Convert the data dictionary to a JSON string with proper indentation
    json_data = json.dumps(data, indent=4)
    
    # Create a response object with the JSON data and the appropriate media type
    response = Response(content=json_data, media_type="application/json")
    
    # Return the response object
    return response
