import streamlit as st
import requests
import pandas as pd
import subprocess
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

df = pd.read_pickle('./data/cleaned/movies.pkl')
df1 = df

movies = df['title'].astype(str).tolist()
movies = sorted(movies)

genres = df['genres'].astype(str).str.replace("[", "").str.replace("]", "").str.replace("'", "").str.replace(",", "").str.split(' ').tolist()
genres = sorted(list(set([item for sublist in genres for item in sublist])))

cast = df['cast'].astype(str).str.replace("[", "").str.replace("]", "").str.replace("'", "").str.split(', ').tolist()
cast = sorted(list(set([item for sublist in cast for item in sublist])))

crew = df['crew'].astype(str).str.split(', ').replace("[", "").replace("]", "").replace("'", "").replace('"', "")
crew = sorted(list(set([item for sublist in crew for item in sublist])))

df = df[['title', 'belongs_to_collection', 'original_language', 'genres', 'overview', 'popularity', 'production_companies', 'production_countries', 'release_date', 'cast', 'crew']]

# Combinar las características en una sola columna
df.loc[:, 'features'] = df.apply(lambda x: ' '.join(x.values.astype(str)), axis=1)

# # Crear la matriz TF-IDF
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['features'])

# # Crear el modelo de vecinos más cercanos
knn = NearestNeighbors(metric='cosine', algorithm='brute')
knn.fit(tfidf_matrix)

def main():
    st.title("MovieMentor")
    st.subheader("Are you tired of endlessly browsing through countless movies, unsure of what to watch next?")
    st.write("Say goodbye to decision fatigue and let our advanced algorithms do the work for you. Our powerful recommendation engine, fueled by machine learning, will suggest the perfect movies tailored to your unique tastes.")

    default_movie_index = movies.index("Star Wars")
    # Collect user input
    user_input = st.selectbox("Select your favourite movie:", movies, index=default_movie_index)
    num_recommendations = st.selectbox("Select the number of recommended movies:", [5, 10, 20, 50], index=0)

    if st.button("Get Recommendations"):
        recommendations = get_movie_recommendations(user_input, num_recommendations)
        st.write("Recommendations:")
        st.json(recommendations)

    st.subheader("Acquire the details about the recommended movie...")
    st.write("Please select one of the recommended movies to get all the juicy details about it, my distinguished friend!")
    default_movie_index = movies.index("The Empire Strikes Back")
    user_input = st.selectbox("Select the recommended movie:", movies, index=default_movie_index)

    if st.button("Get Movie"):
        recommendations = get_movie(user_input)
        st.write("Details:")
        st.json(recommendations)

    st.subheader("Perhaps you're in pursuit of popular movies sorted by genre...")
    st.write("Choose the genre you're looking for and receive a curated list of popular movies from that genre.")
    user_input = st.selectbox("Select the Genre:", genres)
    num_recommendations = st.selectbox("Select the number of recommended movies:", [10, 25, 50, 100, 500], index=0)

    if st.button("Get the movies"):
        recommendations = movies_by_genre(user_input, num_recommendations)
        st.write("Recommendations:")
        st.json(recommendations)

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
    # Get the index of the movie that matches the title
    idx = data[data['title'] == title].index[0]

    # Find the nearest neighbors
    distances, indices = knn_model.kneighbors(tfidf_matrix[idx], n_neighbors=num+1)

    # Get the indices of the most similar movies (excluding the query movie)
    movie_indices = indices.flatten()[1:]

    movies = data['title'].iloc[movie_indices].tolist()

    data = {
        "recommendations": movies
    }

    return data

@st.cache_data
def movies_by_genre(genre: str, num: int, data=df):
    df1 = df[df['genres'].notna() & df['genres'].str.contains(genre, case=False)]
    df1 = df1.sort_values(by='popularity', ascending=False)
    df1 = df1.head(num)

    data = {
        "title": df1['title'].tolist()
    }
    return data

@st.cache_data
def get_movie(title: str):
    df1 = df[df['title'] == title]
    
    # Create the data dictionary with the updated movies list
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
            "cast": row['cast'].replace("'", "").replace('"', "").replace("[", "").replace("]", "").split(", "),
            "crew": row['crew'].replace("'", "").replace('"', "").replace("[", "").replace("]", "").split(", ")
        }
        # Append the movie dictionary to the movies list
        movies.append(movie)
    
    movies_count = df1.shape[0]
    
    # Create the data dictionary with the updated movies list
    data = {
        "name": director,
        "total movies": movies_count,
        "movies": movies
    }
    return data

@st.cache_data
def get_actor(actor: str):
    # Filter the DataFrame to include only rows where the 'cast' column is not null and contains the specified actor
    df1 = df[df['cast'].notna() & df['cast'].str.contains(actor)]
    
    # Calculate the total number of movies in which the actor appears
    movies_count = df1.shape[0]
    
    # Create a list to store the movie objects
    movies = []
    # Iterate over the rows in the filtered DataFrame
    for _, row in df1.iterrows():
        # Create a dictionary for each movie with the desired information
        movie = {
            "title": row['title'],
            "release_year": pd.to_datetime(row['release_date']).year,
            "overview": row['overview'],
            "cast": row['cast'].replace("'", "").replace('"', "").replace("[", "").replace("]", "").split(", "),
            "crew": row['crew'].replace("'", "").replace('"', "").replace("[", "").replace("]", "").split(", ")
        }
        # Append the movie dictionary to the movies list
        movies.append(movie)
    
    # Create a dictionary to store the data for the API response
    data = {
        "name": actor,
        "total movies": movies_count,
        "movies": movies
    }
    return data

if __name__ == "__main__":
    main()