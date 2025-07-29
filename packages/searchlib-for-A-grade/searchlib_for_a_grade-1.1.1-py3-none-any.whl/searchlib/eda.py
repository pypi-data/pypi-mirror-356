def eda_code():
    return """
import pandas as pd

df = pd.read_csv('D:/uncleaned_diabetes.csv')  
print('First 5 rows:')
print(df.head())
print('\nLast 5 rows:')
print(df.tail())
print('\nDataset shape (rows, columns):', df.shape)
print('\nColumn names:')
print(df.columns.tolist())
print('\nDataset info:')
print(df.info())
print('\nMissing values per column:')
print(df.isnull().sum())
print('\nDescriptive statistics:')
print(df.describe())
print('\nMedian values:')
print(df.median(numeric_only=True))
"""