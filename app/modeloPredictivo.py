import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import numpy as np
import joblib

<<<<<<< HEAD
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
=======
def load_data(file_path):
    # Cargar datos desde un archivo CSV
    df = pd.read_csv(file_path, delimiter=";")
    return df

def preprocess_data(df):
    # Eliminar columnas irrelevantes
    df = df.drop(['Shirts', 'Trousers', 'Shoes'], axis=1)
    
    # Mapear la columna 'Sex_Gender' a valores numéricos
    df['Sex_Gender'] = df['Sex_Gender'].map({'F': 0, 'M': 1})
    
    return df

def encode_and_scale_data(X_train, X_test, categorical_cols):
    # Codificar variables categóricas
    encoder = OneHotEncoder(drop='first')
    X_train_encoded = encoder.fit_transform(X_train[categorical_cols])
    X_test_encoded = encoder.transform(X_test[categorical_cols])

    # Concatenar variables codificadas con características originales
    X_train_encoded = np.hstack((X_train_encoded.toarray(), X_train.drop(categorical_cols, axis=1)))
    X_test_encoded = np.hstack((X_test_encoded.toarray(), X_test.drop(categorical_cols, axis=1)))

    # Normalizar los datos
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train_encoded)
    X_test_scaled = scaler.transform(X_test_encoded)

    return X_train_scaled, X_test_scaled

def train_model(X_train, y_train):
    # Entrenar un modelo de clasificación de bosque aleatorio
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test):
    # Evaluar el modelo con datos de prueba
    with np.errstate(divide='warn', invalid='warn'):
        y_pred = model.predict(X_test)
        report = classification_report(y_test, y_pred, zero_division=0)
    return report
>>>>>>> c679fe1e2f3bff023ad1c550def9f233a9e25a90

joblib.dump(model, "modeloPredictivo.pkl")
print("Modelo guardado correctamente.")

def save_model(model, file_path):
    # Guardar el modelo entrenado en un archivo
    joblib.dump(model, file_path)
    print("Modelo guardado correctamente.")

if __name__ == "__main__":
    # Paso 1: Cargar y preprocesar los datos
    file_path = "SakuraStylishDB.csv"
    df = load_data(file_path)
    df = preprocess_data(df)
    
    # Separar características y etiquetas
    X = df.drop('Type_Clothing_Event', axis=1)
    y = df['Type_Clothing_Event']
    
    # Dividir datos en conjuntos de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Paso 2: Codificar y escalar los datos
    categorical_cols = ['Age', 'Size', 'Weather', 'Time', 'Event']
    X_train_scaled, X_test_scaled = encode_and_scale_data(X_train, X_test, categorical_cols)
    
    # Paso 3: Entrenar un modelo
    model = train_model(X_train_scaled, y_train)
    
    # Paso 4: Evaluar el modelo
    report = evaluate_model(model, X_test_scaled, y_test)
    print("Informe de clasificación:\n", report)
    
    # Paso 5: Guardar el modelo entrenado
    model_file_path = "modeloPredictivo.pkl"
    save_model(model, model_file_path)
