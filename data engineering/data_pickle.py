import pandas as pd
import pickle

# Read the CSV file into a pandas DataFrame
df = pd.read_csv('../data/cleaned/movies.csv')

# Perform any necessary data preprocessing or transformations

# Save the DataFrame to a pickle file
with open('../data/cleaned/movies.pkl', 'wb') as file:
    pickle.dump(df, file)