import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
import numpy as np

df = pd.read_csv("SakuraStylishDB.csv", delimiter=";")
print(df)

df = df.drop(['Shirts', 'Trousers', 'Shoes'], axis=1)
print(df)


df['Sex Gender'] = df['Sex Gender'].map({'F': 0, 'M': 1})
 
