import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
import numpy as np
import joblib

df = pd.read_csv("SakuraStylishDB.csv", delimiter=";")
print(df)


df = df.drop(['Time', 'Shirts', 'Trousers', 'Shoes'], axis=1)
print(df)


df['Sex_Gender'] = df['Sex_Gender'].map({'F': 0, 'M': 1})


X = df.drop('Type_Clothing_Event', axis=1)
y = df['Type_Clothing_Event']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


categorical_cols = ['Age', 'Size', 'Weather', 'Event']
encoder = OneHotEncoder(drop='first')
X_train_encoded = encoder.fit_transform(X_train[categorical_cols])
X_test_encoded = encoder.transform(X_test[categorical_cols])

 # Concatenar las variables codificadas con las características originales
X_train_encoded = np.hstack((X_train_encoded.toarray(), X_train.drop(categorical_cols, axis=1)))
X_test_encoded = np.hstack((X_test_encoded.toarray(), X_test.drop(categorical_cols, axis=1)))

# Paso 4: Normalización de los datos
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_encoded)
X_test_scaled = scaler.transform(X_test_encoded)

# Paso 5: Entrenamiento del modelo
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)

# Paso 6: Realización de una predicción con nuevos datos
# Supongamos que tenemos un nuevo vector de datos para predecir la salida
new_data = pd.DataFrame({'Age': ['Adult'], 'Size': ['L'], 'Weather': ['Cold'], 'Sex_Gender': ['F'], 'Event': ['Marriage'], 'Satisfaction': [1] })

# Convertir la columna 'Sex' a valores numéricos
new_data['Sex_Gender'] = new_data['Sex_Gender'].map({'F': 0, 'M': 1})

# Codificar la columna 'Embarked' utilizando el mismo encoder
new_data_encoded = encoder.transform(new_data[['Age', 'Size', 'Weather', 'Event']])

# Concatenar las variables codificadas con las características originales
new_data_encoded = np.hstack((new_data_encoded.toarray(), new_data.drop(['Age', 'Size', 'Weather', 'Event'], axis=1)))

# Normalizar el nuevo vector de datos utilizando el mismo escalador
new_data_scaled = scaler.transform(new_data_encoded)

# Predecir la salida del nuevo vector de datos
prediction = model.predict(new_data_scaled)
print("Predicción:", prediction)

joblib.dump(model, "modeloPredictivo.pkl")
print("Modelo guardado correctamente.")


