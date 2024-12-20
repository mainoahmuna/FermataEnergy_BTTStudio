# -*- coding: utf-8 -*-
"""Fermatametadata_stats.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/15ZA1glMQCllI4pkJLO1-yn7S612bb1ln

Processing data based on states and heating type

By Ananya Hota
"""

# Importing libraries (code block credit to Victoria)
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
import plotly.graph_objects as go
import os

from google.colab import files
import pandas as pd

uploaded = files.upload()

df = pd.read_csv('metadata.csv')

df.head()

phoenix_mask = df['in.cluster_name'] == 'Phoenix Area'
phoenix_data = df[phoenix_mask]

print(f"Number of buildings in Phoenix Area: {len(phoenix_data)}")
print("Filtered data rows, columns:", phoenix_data.shape)

# Distribution of Building Types in Phoenix Area
building_type_counts_phoenix = phoenix_data['in.comstock_building_type'].value_counts()
print("\nDistribution of Building Types in Phoenix Area:")
print(building_type_counts_phoenix)

# Visualization
fig = px.bar(building_type_counts_phoenix, x=building_type_counts_phoenix.index, y=building_type_counts_phoenix.values,
             title="Distribution of Building Types in Phoenix Area", labels={'x':'Building Type', 'y':'Count'})
fig.show()

# Distribution of Heating Sources in Phoenix Area
heating_fuel_counts_phoenix = phoenix_data['in.heating_fuel'].value_counts()
print("\nDistribution of Heating Sources in Phoenix Area:")
print(heating_fuel_counts_phoenix)

# Visualization
fig = px.bar(heating_fuel_counts_phoenix, x=heating_fuel_counts_phoenix.index, y=heating_fuel_counts_phoenix.values,
             title="Distribution of Heating Sources in Phoenix Area", labels={'x':'Heating Fuel', 'y':'Count'})
fig.show()

print("rows, columns")
df.shape

from sklearn.model_selection import train_test_split

df = pd.read_csv('metadata.csv')

phoenix_mask = df['in.cluster_name'] == 'Phoenix Area'
phoenix_data = df[phoenix_mask]

print(f"Number of buildings in Phoenix Area: {len(phoenix_data)}")
print("Filtered data rows, columns:", phoenix_data.shape)

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

X = phoenix_data.drop(columns=['in.cluster_name', 'in.heating_fuel'])
y = phoenix_data['in.heating_fuel']

label_encoders = {}
for col in X.select_dtypes(include=['object']).columns:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col])
    label_encoders[col] = le

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Training set shape:", X_train.shape, y_train.shape)
print("Test set shape:", X_test.shape, y_test.shape)

from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)



from sklearn.metrics import classification_report, confusion_matrix

y_pred = model.predict(X_test)

print(classification_report(y_test, y_pred))

cm = confusion_matrix(y_test, y_pred)
print("Confusion Matrix:\n", cm)

import seaborn as sns
import matplotlib.pyplot as plt

cm = confusion_matrix(y_test, y_pred)

unique_labels = np.unique(np.concatenate((y_test, y_pred)))

plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=unique_labels, yticklabels=unique_labels)
plt.xlabel("Predicted Label")
plt.ylabel("True Label")
plt.title("Confusion Matrix for Heating Fuel Prediction")
plt.show()

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

if 'energy_consumption' in phoenix_data.columns:
    X_regression = phoenix_data.drop(columns=['in.cluster_name', 'in.heating_fuel', 'energy_consumption'])
    y_regression = phoenix_data['energy_consumption']

    for col in X_regression.select_dtypes(include=['object']).columns:
        le = LabelEncoder()
        X_regression[col] = le.fit_transform(X_regression[col])

    X_train_reg, X_test_reg, y_train_reg, y_test_reg = train_test_split(
        X_regression, y_regression, test_size=0.2, random_state=42
    )

    reg_model = LinearRegression()
    reg_model.fit(X_train_reg, y_train_reg)

    y_pred_reg = reg_model.predict(X_test_reg)

    mse = mean_squared_error(y_test_reg, y_pred_reg)
    r2 = r2_score(y_test_reg, y_pred_reg)

    print("Mean Squared Error (MSE):", mse)
    print("R-squared (R²):", r2)

    plt.figure(figsize=(8, 6))
    plt.scatter(y_test_reg, y_pred_reg, alpha=0.7)
    plt.plot([min(y_test_reg), max(y_test_reg)], [min(y_test_reg), max(y_test_reg)], color='red', linestyle='--')
    plt.xlabel("Actual Values")
    plt.ylabel("Predicted Values")
    plt.title("Actual vs Predicted Energy Consumption")
    plt.show()
else:
    print("The 'energy_consumption' column is not available in the dataset.")