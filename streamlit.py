'''
This script serves the purpose of deploying a web application using Streamlit. 
It showcases the main functionalities of a movie recommendation system powered by machine learning. 

'''
import streamlit as st
import requests
import pandas as pd
import subprocess
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

# Load the preprocessed movie data
df = pd.read_pickle('./data/cleaned/movies.pkl')
df1 = df

# Extract movie titles and sort them
movies = df['title'].astype(str).tolist()
movies = sorted(movies)

# Extract genres and sort them
genres = df['genres'].astype(str).str.replace("[", "").str.replace("]", "").str.replace("'", "").str.replace(",", "").str.split(' ').tolist()
genres = sorted(list(set([item for sublist in genres for item in sublist])))

# Extract cast members and sort them
cast = df['cast'].astype(str).str.replace("[", "").str.replace("]", "").str.replace("'", "").str.split(', ').tolist()
cast = sorted(list(set([item for sublist in cast for item in sublist])))

# Extract crew members and sort them
crew = df['crew'].astype(str).str.split(', ').replace("[", "").replace("]", "").replace("'", "").replace('"', "")
crew = sorted(list(set([item for sublist in crew for item in sublist])))

# Prepare the dataframe with relevant features for recommendation
df = df[['title', 'belongs_to_collection', 'original_language', 'genres', 'overview', 'popularity', 'production_companies', 'production_countries', 'release_date', 'cast', 'crew']]

# Combine features into a single column for TF-IDF vectorization
df.loc[:, 'features'] = df.apply(lambda x: ' '.join(x.values.astype(str)), axis=1)

# Apply TF-IDF vectorization to the combined features
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['features'])

# Build the K-Nearest Neighbors model for recommendation
knn = NearestNeighbors(metric='cosine', algorithm='brute')
knn.fit(tfidf_matrix)

def main():
    '''
    This main function serves as the entry point and orchestrator for the Streamlit web application. 
    It defines the main logic and user interface of the MovieMentor app.
    Let's go through the code and explain its functionality.

    '''

    # Set the title and introductory text
    st.title("MovieMentor")
    st.subheader("Are you tired of endlessly browsing through countless movies, unsure of what to watch next?")
    st.write("Say goodbye to decision fatigue and let our advanced algorithms do the work for you. Our powerful recommendation engine, fueled by machine learning, will suggest the perfect movies tailored to your unique tastes.")

    # Get user input for the favorite movie and the number of recommendations
    default_movie_index = movies.index("Star Wars")
    user_input = st.selectbox("Select your favourite movie:", movies, index=default_movie_index)
    num_recommendations = st.selectbox("Select the number of recommended movies:", [5, 10, 20, 50], index=0)

    # Retrieve movie recommendations based on user input
    if st.button("Get Recommendations"):
        recommendations = get_movie_recommendations(user_input, num_recommendations)
        st.write("Recommendations:")
        st.json(recommendations)

    # Get user input for a recommended movie to get detailed information
    st.subheader("Acquire the details about the recommended movie...")
    st.write("Please select one of the recommended movies to get all the juicy details about it, my distinguished friend!")
    default_movie_index = movies.index("The Empire Strikes Back")
    user_input = st.selectbox("Select the recommended movie:", movies, index=default_movie_index)

    # Retrieve detailed information about the selected movie
    if st.button("Get Movie"):
        recommendations = get_movie(user_input)
        st.write("Details:")
        st.json(recommendations)

    # Get popular movies from a selected genre
    st.subheader("Perhaps you're in pursuit of popular movies sorted by genre...")
    st.write("Choose the genre you're looking for and receive a curated list of popular movies from that genre.")
    user_input = st.selectbox("Select the Genre:", genres)
    num_recommendations = st.selectbox("Select the number of recommended movies:", [10, 25, 50, 100, 500], index=0)

    if st.button("Get the movies"):
        recommendations = movies_by_genre(user_input, num_recommendations)
        st.write("Recommendations:")
        st.json(recommendations)

    # Get movies featuring a selected director or actor
    st.subheader("Maybe you're eager to watch movies featuring your favourite director or actor...")
    director_actor = ['', 'director', 'actor']
    user_input = st.selectbox("Select Director or Actor:", director_actor)

    if user_input == 'director':
        default_movie_index = crew.index("'George Lucas'")
        user_director = st.selectbox("Select the director:", crew, index=default_movie_index)
        
        if st.button("Get the director"):
            recommendations = get_director(user_director)
            st.write("Director:")
            st.json(recommendations)

    elif user_input == 'actor':
        default_movie_index = cast.index("Mark Hamill")
        user_director = st.selectbox("Select the actor:", cast, index=default_movie_index)
        
        if st.button("Get the actor"):
            recommendations = get_actor(user_director)
            st.write("Actor:")
            st.json(recommendations)

@st.cache_data
def get_movie_recommendations(title, num, knn_model=knn, data=df):
    '''
    Function to retrieve movie recommendations based on user input.
    
    Args:
        title (str): The title of the user's favorite movie.
        num (int): The number of recommendations to retrieve.
        knn_model (NearestNeighbors): The pre-trained KNN model for recommendation.
        data (DataFrame): The preprocessed movie data.

    Returns:
        dict: A dictionary containing the movie recommendations.

    '''

    # Find the index of the user's favorite movie
    idx = data[data['title'] == title].index[0]

    # Perform KNN search to get similar movies
    distances, indices = knn_model.kneighbors(tfidf_matrix[idx], n_neighbors=num+1)
    movie_indices = indices.flatten()[1:]

    # Retrieve the recommended movies
    movies = data['title'].iloc[movie_indices].tolist()
    data = {
        "recommendations": movies
    }

    return data

@st.cache_data
def movies_by_genre(genre: str, num: int, data=df):
    '''
    Function to retrieve popular movies of a specific genre.

    Args:
        genre (str): The genre of movies to retrieve.
        num (int): The number of movies to recommend.
        data (DataFrame): The preprocessed movie data.

    Returns:
        dict: A dictionary containing the recommended movies.

    '''

    # Filter movies by the specified genre
    df1 = df[df['genres'].notna() & df['genres'].str.contains(genre, case=False)]

    # Sort movies by popularity and select the desired number of movies
    df1 = df1.sort_values(by='popularity', ascending=False)
    df1 = df1.head(num)

    data = {
        "title": df1['title'].tolist()
    }
    return data

@st.cache_data
def get_movie(title: str):
    '''
    Function to retrieve detailed information about a movie.

    Args:
        title (str): The title of the movie to retrieve.

    Returns:
        dict: A dictionary containing the movie details.
        
    '''

    # Filter the DataFrame to get the movie details
    df1 = df[df['title'] == title]
    
    data = {
        "title": title,
        "release_year": pd.to_datetime(df1['release_date'].tolist()[0]).year,
        "overview": df1['overview'].tolist()[0],
        "popularity": df1['popularity'].tolist()[0],
        "cast": df1['cast'].tolist()[0].replace("'", "").replace('"', "").replace("[", "").replace("]", "").split(", "),
        "crew": df1['crew'].tolist()[0].replace("'", "").replace('"', "").replace("[", "").replace("]", "").split(", ")
    }
    return data

@st.cache_data
def get_director(director: str):
    '''
    Function to retrieve information about a director and their movies.

    Args:
        director (str): The name of the director.

    Returns:
        dict: A dictionary containing the director's information and movies.
        
    '''

    # Filter the DataFrame to get movies directed by the specified director
    df1 = df[df['crew'].notna() & df['crew'].str.contains(director)]
    
    movies = []
    
    for _, row in df1.iterrows():
        # Create a movie dictionary with details
        movie = {
            "title": row['title'],
            "release_year": pd.to_datetime(row['release_date']).year,
            "overview": row['overview'],
            "cast": row['cast'].replace("'", "").replace('"', "").replace("[", "").replace("]", "").split(", "),
            "crew": row['crew'].replace("'", "").replace('"', "").replace("[", "").replace("]", "").split(", ")
        }
        movies.append(movie)
    
    movies_count = df1.shape[0]
    
    data = {
        "name": director,
        "total movies": movies_count,
        "movies": movies
    }
    return data

@st.cache_data
def get_actor(actor: str):
    '''
    Function to retrieve information about an actor and their movies.

    Args:
        actor (str): The name of the actor.

    Returns:
        dict: A dictionary containing the actor's information and movies.
        
    '''

    # Filter the DataFrame to get movies featuring the specified actor
    df1 = df[df['cast'].notna() & df['cast'].str.contains(actor)]
    
    movies_count = df1.shape[0]
    
    movies = []
    for _, row in df1.iterrows():
        # Create a movie dictionary with details    
        movie = {
            "title": row['title'],
            "release_year": pd.to_datetime(row['release_date']).year,
            "overview": row['overview'],
            "cast": row['cast'].replace("'", "").replace('"', "").replace("[", "").replace("]", "").split(", "),
            "crew": row['crew'].replace("'", "").replace('"', "").replace("[", "").replace("]", "").split(", ")
        }
        movies.append(movie)
    
    data = {
        "name": actor,
        "total movies": movies_count,
        "movies": movies
    }
    return data

if __name__ == "__main__":
    main()