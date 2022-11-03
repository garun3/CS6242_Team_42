# Implementation of Linear Regression on dataset -> predict happiness score
from sklearn.linear_model import ElasticNetCV
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Read the data
data = pd.read_csv(os.path.join(os.path.dirname(__file__), 'all_data.csv'))
print(data.iloc[0])
