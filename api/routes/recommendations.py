import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from fastapi import FastAPI, Response, APIRouter
import json

# Import the FastAPI framework
router = APIRouter()

# Cargar el dataset
data = pd.read_pickle('./data/cleaned/movies.pkl')

data = data[['title', 'belongs_to_collection', 'original_language', 'genres', 'overview', 'popularity', 'production_companies', 'production_countries', 'release_date', 'cast', 'crew']]

# Combinar las características en una sola columna
data['features'] = data.apply(lambda x: ' '.join(x.values.astype(str)), axis=1)

# Crear la matriz TF-IDF
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(data['features'])

# Crear el modelo de vecinos más cercanos
knn = NearestNeighbors(metric='cosine', algorithm='brute')
knn.fit(tfidf_matrix)

@router.get("/api/v1/recommendations/{num}/{title}")
def get_movie_recommendations(title: str, num: int, knn_model=knn, data_func=lambda: data):
    # Get the index of the movie that matches the title
    data = data_func() # Access the data through the function to avoid the truth value error
    idx = data[data['title'] == title].index[0]

    # Find the nearest neighbors
    distances, indices = knn_model.kneighbors(tfidf_matrix[idx], n_neighbors=num+1)

    # Get the indices of the most similar movies (excluding the query movie)
    movie_indices = indices.flatten()[1:]

    movies = data['title'].iloc[movie_indices].tolist()

    data = {
        "recommendations": movies
    }

    # Convert the data dictionary to a JSON string with proper indentation
    json_data = json.dumps(data, indent=4)

    # Create a response object with the JSON data and the appropriate media type
    response = Response(content=json_data, media_type="application/json")

    # Return the response object
    return response