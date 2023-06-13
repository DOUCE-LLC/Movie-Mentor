import sys
import os
import json
from fastapi import FastAPI, Response, APIRouter

# Get the path of the main directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add the path to sys.path
sys.path.append(BASE_DIR)

# Import the FastAPI framework and other necessary modules
from fastapi import FastAPI
from api.routes import get_actor, get_director, shoots_per_day, shoots_per_month, title_score, title_votes, movies_by_genre, recommendations, get_movie, recommendations2

app = FastAPI()

@app.get("/api/v1")
def read_root():
    data = {
        "message": "Welcome to the API! Below, we present you with a range of exciting pathways to explore, along with some fascinating Star Wars examples for you to delve into.",
        "routesInfo": [{
            "Recommendations based on a movie": '/api/v1/recommendations/5/Star%20Wars',
            "Information about an actor": '/api/v1/actor/Mark%20Hamill',
            "Information about a director": '/api/v1/director/George%20Lucas',
            "Popular movies by genre": '/api/v1/movies_by_genre/Cience%20Fiction',
            "Get a movie": "/api/v1/movie/Star%20Wars",
            "Shoots per month": '/api/v1/shoots_per_month/5',
            "Shoots per day": '/api/v1/shoots_per_day/4',
        }]
    }
    
    # Convert the data dictionary to a JSON string with proper indentation
    json_data = json.dumps(data, indent=4)
    
    # Create a response object with the JSON data and the appropriate media type
    response = Response(content=json_data, media_type="application/json")

    # Return the response object
    return response

app.include_router(get_actor.router) # /api/v1/actor/Mark%20Hamill
app.include_router(get_director.router)  # /api/v1/director/George%20Lucas
app.include_router(shoots_per_day.router) # /api/v1/shoots_per_day/13
app.include_router(shoots_per_month.router) # /api/v1/shoots_per_month/1
app.include_router(title_score.router) # /api/v1/title_score/Star%20Wars
app.include_router(title_votes.router) # /api/v1/title_votes/Star%20Wars
app.include_router(movies_by_genre.router) # /api/v1/movies_by_genre/Cience%20Fiction
app.include_router(recommendations.router) # /api/v1/recommendations/5/Star%20Wars
app.include_router(recommendations2.router) # /api/v1/recommendations2/5/Star%20Wars
app.include_router(get_movie.router) # /api/v1/recommendations/Star%20Wars