# import nltk
# import ast
# from nltk.corpus import stopwords
# from nltk.tokenize import word_tokenize
# from nltk.stem import WordNetLemmatizer
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.linear_model import LogisticRegression
# import pandas as pd

# df = pd.read_csv('../data/cleaned/movies.csv')

# df['overview'].fillna('a', inplace=True)
# df['genres'].dropna()
# df['tagline'].fillna('a', inplace=True)
# df['title'].fillna('a', inplace=True)

# for i, row in df.iterrows():
#     overview = row['overview']
#     tagline = row['tagline']
#     title = row['title']
#     genres = row['genres']
#     # genres_list = df['genres'][i].split(' ')
#     genres_list = ast.literal_eval(df['genres'][i])
#     genres_length = len(genres_list)
#     generes_num = [i for i in range(len(genres_list))]

#     if genres_length > 1:
#         # print(title, '\n', overview, '\n')
#         # print(genres_length, genres, generes_num)

#         # Preprocessing
#         stop_words = set(stopwords.words('english'))
#         lemmatizer = WordNetLemmatizer()

#         def preprocess_text(text):
#             tokens = word_tokenize(text.lower())
#             tokens = [lemmatizer.lemmatize(token) for token in tokens if token.isalnum() and token not in stop_words]
#             preprocessed_text = ' '.join(tokens)
#             return preprocessed_text

#         # Preprocess the plot
#         preprocessed_plot1 = preprocess_text(overview)
#         preprocessed_plot2 = preprocess_text(tagline)
#         preprocessed_plot3 = preprocess_text(title)

#         # Create hypothetical samples
#         samples = [preprocessed_plot1 + preprocessed_plot2 + preprocessed_plot3] * genres_length

#         # Vectorize the samples
#         vectorizer = TfidfVectorizer()
#         plot_vector = vectorizer.fit_transform(samples)

#         # Create labels for the samples
#         labels = generes_num

#         # Train a logistic regression classifier
#         classifier = LogisticRegression()
#         classifier.fit(plot_vector, labels)

#         # Predict the genre
#         predicted_label = classifier.predict(plot_vector)[0]
#         predicted_genre = genres_list[predicted_label]

#         print(title)
#         print(genres_list)
#         print("Predicted Genre:", predicted_genre, '\n')
