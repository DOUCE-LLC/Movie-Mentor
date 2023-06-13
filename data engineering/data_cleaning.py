import pandas as pd
import numpy as np
import ast
import re

"""
The script starts by importing necessary libraries and setting display options for Pandas.
It then reads two CSV files, "movies_dataset.csv" and "credits.csv", into separate DataFrames.
The script defines various utility functions to remove null values, convert values to strings,
extract names from string values, fill null values with zeros, clean date columns, calculate
return on investment (ROI), drop columns, and perform inner joins.

After defining the functions, the script proceeds to execute a series of operations on the DataFrame.
It performs an inner join between the two DataFrames based on the "id" column.
Then, it drops several unnecessary columns from the DataFrame.
Next, it fills null values in the "revenue" and "budget" columns with zeros.
It removes rows with null values in the "release_date" column.

The script further cleans the "release_date" column by converting it to
a standard format and creating a new column with only the year component.
It calculates the ROI by dividing the "revenue" by the "budget" and stores the result in a new "ROI" column.

Next, the script iterates over each column in the DataFrame and checks if there are occurrences of "{" character.
If a column has at least two occurrences, it applies string conversion and extracts multiple names from the values.
If a column has at least one occurrence, it applies string conversion and extracts a single name.

Finally, the transformed DataFrame is saved as a CSV file named "movies.csv" in the "./transformedData/" directory.

Overall, this script performs various data preprocessing and transformation tasks,
including data cleaning, feature extraction, and column manipulation, to transform the movie datasets into a more structured and usable format.

"""
pd.set_option('display.max_columns', None)

df = pd.read_csv('../data/not cleaned/movies_dataset.csv', sep=',', quotechar='"', dtype={'overview': str})
df2 = pd.read_csv('../data/not cleaned/credits1.csv')
df3 = pd.read_csv('../data/not cleaned/credits2.csv')
df4 = pd.read_csv('../data/not cleaned/credits3.csv')

def combineDataframes(df1, df2):
    """
    Combines two DataFrames into a single one by vertically concatenating them.

    This function takes two DataFrames (`df1` and `df2`) as input and uses the pandas `concat()` function
    to vertically concatenate them into a single DataFrame called `df_combined`.

    Parameters
    ----------
    df1 : pandas DataFrame
        The first DataFrame to be combined.
    df2 : pandas DataFrame
        The second DataFrame to be combined.

    Returns
    -------
    pandas DataFrame
        The resulting DataFrame after vertical concatenation.

    """
    df = pd.concat([df1, df2], ignore_index=True)
    return df

def removeNulls(column):
    """
    Removes null values from a specific column in a DataFrame.

    This function takes a column name as input and removes any null
    values from that column in the DataFrame `df`. It modifies the
    DataFrame in-place by using the `dropna()` method of the column.

    Parameters
    ----------
    column : str
        The name of the column to remove null values from.

    Returns
    -------
    None

    """
    # Use the `dropna()` method of the specified column to remove null values
    df[column].dropna(inplace=True)

def stringConverter(value):
    """
    Converts a value to a string representation.

    This function takes a value as input and converts it to a string.
    If the value is a list or a dictionary, it is first converted to a JSON string
    using the `json.dumps()` function. For other types of values, the `str()` function
    is used for the conversion.

    Parameters
    ----------
    value : any
        The value to be converted to a string.

    Returns
    -------
    str
        The string representation of the value.

    """
    # Check if the value is an instance of a list or a dictionary
    if isinstance(value, (list, dict)):
        # If it is, convert the value to a JSON string and return it
        return json.dumps(value)
    return str(value)

def extractNames(value):
    """
    Extracts a single name from a given string value.

    This function uses regular expressions to find and extract
    a name that matches the pattern "'name': '([^']*)'" from
    the provided value. The first matching name is returned.

    Parameters
    ----------
    value : str
        The string value to extract the name from.

    Returns
    -------
    str or None
        The extracted name if a match is found, otherwise returns None.

    """
    # Define the regular expression pattern to match a name
    pattern = r"'name': '([^']*)'"

    # Find all matches of the pattern in the value
    matches = re.findall(pattern, value)

    # If any matches are found, assign the first match to the names variable and return it
    if len(matches) > 0:
        names = matches[0]
        return names
    else:
        # If no matches are found, return None
        return None
    
def extractMultipleNames(value):
    """
    Extracts multiple names from a given string value.

    This function uses regular expressions to find and extract
    names that match the pattern "'name': '([^']*)'" from the
    provided value. The names are returned as a list.

    Parameters
    ----------
    value : str
        The string value to extract names from.

    Returns
    -------
    list or None
        A list containing the extracted names if any are found,
        otherwise returns None.

    """
    # Define the regular expression pattern to match names
    pattern = r"'name': '([^']*)'"

    # Find all matches of the pattern in the value
    matches = re.findall(pattern, value)

    # If any matches are found, assign them to the names variable and return the list of names
    if len(matches) > 0:
        names = matches
        return names
    else:
        # If no matches are found, return None
        return None

def fillNull0(column):
    """
    Fills null values in a specific column of a DataFrame with zero.

    This function takes a column name as input and fills any null
    values in that column of the DataFrame `df` with zero. It uses
    the `fillna()` method of the column to perform the operation.

    Parameters
    ----------
    column : str
        The name of the column to fill null values in.

    Returns
    -------
    None

    """
    # Fill null values in the specified column with zero using the `fillna()` method
    return df[column].fillna(0, inplace=True)

def cleanDate(column):
    """
    Cleans a column containing date values in a DataFrame.

    This function takes a column name as input and performs three
    operations to clean the date values in that column of the DataFrame `df`.

    1. Convert the values in the column to datetime format using `pd.to_datetime()`.
       Any values that cannot be converted to datetime are set to NaT (Not a Time).

    2. Convert the datetime values in the column to a specific string format '%Y-%m-%d'
       using the `.dt.strftime()` method. This formats the dates as 'YYYY-MM-DD'.

    3. Create a new column in the DataFrame with the column name appended by '_year',
       which contains only the year component extracted from the datetime values using
       `pd.to_datetime().dt.year`.

    Parameters
    ----------
    column : str
        The name of the column containing date values to be cleaned.

    Returns
    -------
    None

    """
    # Convert the column values to datetime format
    df[column] = pd.to_datetime(df[column], errors='coerce')

    # Format the datetime values as 'YYYY-MM-DD'
    df[column] = df[column].dt.strftime('%Y-%m-%d')

    # Extract the year component and create a new column with the name '{column}_year'
    df[f'{column}_year'] = pd.to_datetime(df[column], errors='coerce').dt.year

    # Replace any missing values (NaN) in the '{column}_year' column with 0 and convert the column to integer type
    df[f'{column}_year'] = df[f'{column}_year'].fillna(0).astype(int)

def roiColumn(column1, column2, column3):
    """
    Calculates the return on investment (ROI) and assigns it to a new column.

    This function takes three column names as input and calculates the ROI
    by dividing the values in `column2` by the values in `column3`. The calculated
    ROI is assigned to `column1` in the DataFrame `df`.

    Before the calculation, the function performs the following data preprocessing steps:

    1. Converts the values in `column2` to numeric format using `pd.to_numeric()`.
       Any values that cannot be converted are set to NaN (Not a Number), and then
       filled with 0 using the `.fillna()` method.

    2. Converts the values in `column3` to numeric format using `pd.to_numeric()`.
       Any values that cannot be converted are set to NaN, and then filled with 0.

    The calculation is done using the `np.where()` function, which checks if the values
    in `column3` are equal to 0. If they are, the corresponding ROI in `column1` is set to 0.
    Otherwise, the ROI is calculated as the division of the values in `column2` by the values
    in `column3`.

    Parameters
    ----------
    column1 : str
        The name of the column to store the calculated ROI.
    column2 : str
        The name of the column containing the numerator for ROI calculation.
    column3 : str
        The name of the column containing the denominator for ROI calculation.

    Returns
    -------
    None

    """
    # Convert column2 values to numeric format, replace non-convertible values with NaN, and fill NaN with 0
    df[column2] = pd.to_numeric(df[column2], errors='coerce').fillna(0)

    # Convert column3 values to numeric format, replace non-convertible values with NaN, and fill NaN with 0
    df[column3] = pd.to_numeric(df[column3], errors='coerce').fillna(0)

    # Calculate ROI and assign it to column1 using np.where()
    df[column1] = np.where(df[column3] == 0, 0, df[column2] / df[column3])

def dropColumns(df, columns):
    """
    Drops specified columns from a DataFrame.

    This function takes a DataFrame (`df`) and a list of column names (`columns`) as input.
    It removes the specified columns from the DataFrame using the `drop()` method, and
    returns the modified DataFrame.

    Parameters
    ----------
    df : pandas DataFrame
        The DataFrame from which columns are to be dropped.
    columns : list of str
        The names of the columns to be dropped.

    Returns
    -------
    pandas DataFrame
        The DataFrame with the specified columns dropped.

    """
    # Drop the specified columns from the DataFrame using the `drop()` method
    df = df.drop(columns=columns)

    # Return the modified DataFrame
    return df

def innerJoin(df1, df2, id):
    """
    Performs an inner join between two DataFrames based on a common ID column.

    This function takes two DataFrames (`df1` and `df2`) and an ID column name (`id`) as input.
    It performs an inner join operation between the two DataFrames using the ID column as the key,
    and returns the resulting merged DataFrame.

    Before the join operation, the function performs several data preprocessing steps:

    1. It converts the values in the ID column of `df1` to numeric format using `pd.to_numeric()`.
       Any values that cannot be converted to numeric are set to NaN (Not a Number).

    2. It converts the values in the ID column of `df2` to numeric format using `pd.to_numeric()`.
       Any values that cannot be converted to numeric are set to NaN.

    3. It drops any rows from `df1` and `df2` where the ID column contains NaN values,
       using the `dropna()` method with the `subset` parameter set to `[id]`.

    4. It converts the values in the ID column of `df1` and `df2` to integers using `.astype(int)`.
       This ensures that the ID column is represented as integer values.

    Finally, the function performs the inner join operation by using the `pd.merge()` function,
    merging `df1` and `df2` based on the ID column using `on=id` and `how='inner'`.

    Parameters
    ----------
    df1 : pandas DataFrame
        The first DataFrame to be joined.
    df2 : pandas DataFrame
        The second DataFrame to be joined.
    id : str
        The name of the common ID column used for the join operation.

    Returns
    -------
    pandas DataFrame
        The resulting DataFrame after the inner join operation.

    """
    # Convert ID column values in df1 to numeric format, replace non-convertible values with NaN
    df1.loc[:, id] = pd.to_numeric(df1[id], errors='coerce')

    # Convert ID column values in df2 to numeric format, replace non-convertible values with NaN
    df2.loc[:, id] = pd.to_numeric(df2[id], errors='coerce')

    # Drop rows with NaN values in the ID column of df1 and df2
    df1 = df1.dropna(subset=[id])
    df2 = df2.dropna(subset=[id])

    # Convert ID column values in df1 and df2 to integers
    df1.loc[:, id] = df1[id].astype(int)
    df2.loc[:, id] = df2[id].astype(int)

    # Perform inner join between df1 and df2 based on the ID column
    df = pd.merge(df1, df2, on=id, how='inner')

    # Return the resulting merged DataFrame
    return df

# Combine df2, df3 and df4 DataFrames by vertically concatenating them
df2 = combineDataframes(df2, df3)
df2 = combineDataframes(df2, df4)

# Perform an inner join operation between `df` and `df2` based on the 'id' column
df = innerJoin(df, df2, 'id')

# Define a list of column names to be dropped from the DataFrame
columns_to_drop = ['video', 'imdb_id', 'adult', 'original_title', 'poster_path', 'homepage']

# Drop the specified columns from the DataFrame using the `dropColumns` function
df = dropColumns(df, columns_to_drop)

# Fill null values in the 'revenue' column with 0
fillNull0('revenue')

# Fill null values in the 'budget' column with 0
fillNull0('budget')

# Remove rows with null values in the 'release_date' column
removeNulls('release_date')

# Clean the 'release_date' column by converting it to a standard format
cleanDate('release_date')

# Calculate the Return on Investment (ROI) and store the result in the 'ROI' column
roiColumn('ROI', 'revenue', 'budget')

# Iterate over each column in the DataFrame
for column in df.columns:
    if column != 'overview':
        # Check if the column has at least 2 occurrences of '{' character
        if df[column].astype(str).str.count('{').ge(2).sum():
            # Apply string conversion and extract multiple names from the column values
            df[column] = df[column].apply(stringConverter).apply(extractMultipleNames)

        # Check if the column has at least 1 occurrence of '{' character
        if df[column].astype(str).str.count('{').ge(1).sum():
            # Apply string conversion and extract a single name from the column values
            df[column] = df[column].apply(stringConverter).apply(extractNames)

# Save the DataFrame as a CSV file in the specified path
df.to_csv('../data/cleaned/movies.csv')


def print_column_info(df):
    print(df.head())
    for column in df.columns:
        data_type = df[column].dtype
        null_count = df[column].isnull().sum()
        print(f"Column: {column}\nData Type: {data_type}\nNull Count: {null_count}\n")

print_column_info(df)