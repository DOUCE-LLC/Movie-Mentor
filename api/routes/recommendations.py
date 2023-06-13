import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from fastapi import FastAPI, Response, APIRouter
import json

# Import the FastAPI framework
router = APIRouter()

# Load the dataset
data = pd.read_pickle('./data/cleaned/movies.pkl')

# Select the desired columns from the dataset
data = data[['title', 'belongs_to_collection', 'original_language', 'genres', 'overview', 'popularity', 'production_companies', 'production_countries', 'release_date', 'cast', 'crew']]

# Combine the features into a single column
data['features'] = data.apply(lambda x: ' '.join(x.values.astype(str)), axis=1)

# Create the TF-IDF matrix
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(data['features'])

# Create the KNN model
knn = NearestNeighbors(metric='cosine', algorithm='brute')
knn.fit(tfidf_matrix)

@router.get("/api/v1/recommendations/{num}/{title}")
def get_movie_recommendations(title: str, num: int, knn_model=knn, data_func=lambda: data):
    """
    Endpoint to retrieve movie recommendations based on user input.

    Args:
        title (str): The title of the user's favorite movie.
        num (int): The number of recommendations to retrieve.
        knn_model (NearestNeighbors): The pre-trained KNN model for recommendation.
        data_func (function): Function to access the movie data.

    Returns:
        Response: JSON response containing the movie recommendations.

    """

    # Get the index of the movie that matches the title 
    data = data_func() # Access the data through the function to avoid the truth value error
    idx = data[data['title'] == title].index[0]

    # Find the nearest neighbors
    distances, indices = knn_model.kneighbors(tfidf_matrix[idx], n_neighbors=num+1)

    # Get the indices of the most similar movies (excluding the query movie)
    movie_indices = indices.flatten()[1:]

    # Get the titles of the recommended movies
    movies = data['title'].iloc[movie_indices].tolist()

    # Create a dictionary with the movie recommendations
    data = {
        "recommendations": movies
    }

    # Convert the data dictionary to a JSON string with proper indentation
    json_data = json.dumps(data, indent=4)

    # Create a response object with the JSON data and the appropriate media type
    response = Response(content=json_data, media_type="application/json")

    # Return the response object
    return response