# MovieMentor

## Are you tired of endlessly browsing through countless movies, unsure of what to watch next?

Say goodbye to decision fatigue and let our advanced algorithms do the work for you. Our powerful recommendation engine, fueled by **Machine learning**, will suggest the perfect movies tailored to your unique tastes.

https://douce-llc-movie-mentor-streamlit-11cpts.streamlit.app/

<iframe width="560" height="315" src="https://www.youtube.com/embed/JAFnMTVfkM8" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

## Table of Contents

- [Features](#features)
- [Api Routes](#example-api-routes)
- [Machine Learning System](#machine-learning-system)
- [Installation](#installation)
- [Usage](#usage)
- [Example API Response](#example-api-response)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Movie Recommendations**: Get movie recommendations based on a given movie title.
- **Movies by Genre**: Retrieve popular movies within a specific genre.
- **Movie Information**: Fetch detailed information about a specific movie.
- **Actor Information**: Retrieve information about movies in which a specific actor appears.
- **Director Information**: Get information about movies directed by a specific director.

## Example API Routes

- **Movie Recommendations**: `/api/v1/recommendations/{num}/{movie_title}`
- **Movies by Genre**: `/api/v1/movies_by_genre/{genre}`
- **Movie Information**: `/api/v1/movie/{movie_title}`
- **Actor Information**: `/api/v1/actor/{actor_name}`
- **Director Information**: `/api/v1/director/{director_name}`
- **Title Score**: `/api/v1/title_score/{movie_title}`
- **Title Votes**: `/api/v1/title_votes/{movie_title}`
- **Shoots per Month**: `/api/v1/shoots_per_month/{month}`
- **Shoots per Day**: `/api/v1/shoots_per_day/{day}`

## Machine Learning System

The machine learning system utilizes a K-nearest neighbors **(KNN)** model and the **TF-IDF** vectorization technique to provide movie recommendations based on similarity. The system also leverages the movie dataset (`df`) containing various movie attributes such as title, release year, overview, cast, and crew.

## Installation

To install and set up the project, follow these steps:

1. Clone the repository:

   ```shell
   git clone https://github.com/DOUCE-LLC/Movie-Mentor.git
   ```

2. Navigate to the project directory:

   ```shell
   cd Movie-Mentor
   ```

3. Install the required dependencies:

   ```shell
   pip install -r requirements.txt
   ```

4. Set up any specific dependencies or prerequisites that may be required. [Add any additional instructions or links to external resources if necessary.]

## Usage

To use the project, follow these steps:

1. Start the API by running the following command:

   ```shell
   uvicorn main:app
   ```

2. Launch the web interface by executing the following command:

   ```shell
   streamlit run ./streamlit.py
   ```

3. Explore the different features and functionalities of the application.
   - [Provide specific instructions or examples on how to interact with the project]

## Example API Response

Below is an example response structure for the API routes:

### Movie Recommendations

Endpoint: `/api/v1/recommendations/{num}/{movie_title}`

```json
{
  "recommendations": [
    "Movie 1",
    "Movie 2",
    "Movie 3",
    ...
  ]
}
```

### Movies by Genre

Endpoint: `/api/v1/movies_by_genre/{genre}`

```json
{
  "title": [
    "Movie 1",
    "Movie 2",
    "Movie 3",
    ...
  ]
}
```

### Movie Information

Endpoint: `/api/v1/movie/{movie_title}`

```json
{
  "title": "Movie Title",
  "release_year": 2022,
  "overview": "Movie overview...",
  "popularity": 7.8,
  "cast": ["Actor 1", "Actor 2", "Actor 3", ...],
  "crew": ["Director 1", "Director 2", "Director 3", ...]
}
```

### Actor Information

Endpoint: `/api/v1/actor/{actor_name}`

```json
{
  "name": "Actor Name",
  "total movies": 10,
  "movies": [
    {
      "title": "Movie 1",
      "release_year": 2020,
      "overview": "Movie 1 overview...",
      "cast": ["Actor 1", "Actor 2", "Actor 3", ...],
      "crew": ["Director 1", "Director 2", "Director 3", ...]
    },
    ...
  ]
}
```

### Director Information

Endpoint: `/api/v1/director/{director_name}`

```json
{
  "name": "Director Name",
  "total movies": 5,
  "movies": [
    {
      "title": "Movie 1",
      "release_year": 2018,
      "overview": "Movie 1 overview...",
      "cast": ["Actor 1", "Actor 2", "Actor 3", ...],
      "crew": ["Director 1", "Director 2", "Director 3", ...]
    },
    ...
  ]
}
```

###### Please note that the above examples are placeholders and need to be replaced with actual movie titles, actor names, director names, etc.

If you need further assistance, feel free to ask!

## Description of the Main Files

- api/app.py: This file contains the main application of the API used to expose the application's endpoints.

- api/routes: This directory contains the files that define the API routes and the associated controllers for each route.

- data/cleaned: This directory contains the CSV and PKL files that contain the cleaned and preprocessed movie data.

- data/not cleaned: This directory contains the CSV files that contain the raw, uncleaned movie data.
data engineering/data_cleaning.py: This file contains the code for cleaning and transforming the raw movie data.

- main.py: This file is the main entry point of the application and is responsible for running the command-line interface (CLI) and the API.

- README.md: This file is the main README file of the project that provides information about the project structure and how to run it.

- streamlit.py: This file contains the code for the Streamlit-based web user interface that allows users to interact with the movie recommendation system.

## Contributing

Contributions are welcome! If you wish to contribute to this project, please follow these guidelines:

1. Fork the repository and create a new branch.
2. Make your changes and ensure they follow the coding conventions.
3. Test your changes thoroughly.
4. Submit a pull request, clearly describing the changes you've made.

## License

This project is licensed under the [License Name] License - see the [LICENSE](LICENSE) file for details.

Please let me know if there's anything else I can assist you with!