import pandas as pd
from fastapi import FastAPI, Response, APIRouter
import json

# Import the FastAPI framework
router = APIRouter()

# Read a CSV file containing movie data into a pandas DataFrame
df = pd.read_pickle('./data/cleaned/movies.pkl')

@router.get("/api/v1/shoots_per_month/{month}")
def shoots_per_month(month: int):
    """
    Endpoint to retrieve the number of movies released in a specific month.

    Args:
        month (int): The month of the year.

    Returns:
        Response: JSON response containing the number of movies released in the specified month.
    """

    # Filter the DataFrame to include only movies released in the specified month
    df1 = df[pd.to_datetime(df["release_date"]).dt.month == month]
    
    # Create a dictionary to store the data for the API response
    data = {
        "month": month,
        "total movies": df1.shape[0]
    }
    
    # Convert the data dictionary to a JSON string with proper indentation
    json_data = json.dumps(data, indent=4)
    
    # Create a response object with the JSON data and the appropriate media type
    response = Response(content=json_data, media_type="application/json")
    
    # Return the response object
    return response