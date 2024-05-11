from flask import Flask, request, jsonify, render_template
import joblib
import pandas as pd
import numpy as np
from modeloPredictivo import encoder, scaler

app = Flask(__name__)

# Cargar el modelo entrenado al inicio de la aplicación
model = joblib.load('modeloPredictivo.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Obtener las respuestas del usuario desde la solicitud
        data = request.json
        print("Datos recibidos:", data)

        # Convertir las respuestas en un formato adecuado para el modelo
        input_data = prepara_datos_para_modelo(data)
        print("Datos preparados para el modelo:", input_data)

        # Verificar la forma de los datos de entrenamiento
        X_train = model.steps[0][1].transformers_[0][1].feature_names_in_
        print("Forma de los datos de entrenamiento:", X_train.shape[1])

        # Verificar la forma de los datos preparados
        print("Forma de los datos preparados:", input_data.shape[1])

        # Realizar la predicción solo si las formas coinciden
        if X_train.shape[1] == input_data.shape[1]:
            prediction = model.predict(input_data)[0]
            print("Predicción:", prediction)
            return jsonify({'prediction': prediction})
        else:
            error_message = "Las formas de los datos no coinciden"
            print("Error:", error_message)
            return jsonify({'error': error_message}), 400

    except ValueError as e:
        # Manejar errores de validación de datos
        print("Error de validación de datos:", str(e))
        return jsonify({'error': str(e)}), 400

    except Exception as e:
        # Manejar cualquier otro error que ocurra durante la predicción
        print("Error durante la predicción:", e)
        return jsonify({'error': str(e)}), 400

def prepara_datos_para_modelo(data):
    # Verificar que no haya valores vacíos
    if any(value == '' for value in data.values()):
        raise ValueError("No se permiten valores vacíos en los datos")

    # Convertir la columna 'Sex' a valores numéricos
    sex_gender = data['Sex_gender'].upper()  # Convertir a mayusculas
    sex_mapping = {'F': 0, 'M': 1}
    if sex_gender not in sex_mapping:
        raise ValueError("Valor de género no válido. Debe ser 'f' o 'm'.")
    sex_numeric = sex_mapping[sex_gender]

    # Codificar las columnas categóricas utilizando el mismo encoder
    new_data_encoded = encoder.transform([[data['Age'], data['Weather'], data['Event']]])

    # Concatenar las variables codificadas con las características originales
    X_new = np.hstack((new_data_encoded.toarray(), [[sex_numeric]]))

    # Normalizar el nuevo vector de datos utilizando el mismo escalador
    X_new_scaled = scaler.transform(X_new)

    return X_new_scaled

@app.route('/')
def index():
    # Renderizar la página de inicio
    return render_template('index.html')

@app.route('/carrito')
def carrito():
    # Renderizar la página del carrito
    return render_template('carrito.html')

if __name__ == "__main__":
    app.run(debug=True)