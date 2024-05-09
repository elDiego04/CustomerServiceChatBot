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
        data = request.json['data']
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
            print("Error: Las formas de los datos no coinciden")
            return jsonify({'error': 'Las formas de los datos no coinciden'}), 400

    except Exception as e:
        # Manejar cualquier error que ocurra durante la predicción
        print("Error durante la predicción:", e)
        return jsonify({'error': str(e)}), 400

def prepara_datos_para_modelo(data):
    # Crear un DataFrame con las respuestas del usuario
    new_data = pd.DataFrame([data])

    # Asegurarse de que las columnas necesarias estén presentes
    required_columns = ['Age', 'Weather', 'Sex_gender', 'Event']
    missing_columns = [col for col in required_columns if col not in new_data.columns]
    if missing_columns:
        raise ValueError(f"Faltan las siguientes columnas en los datos recibidos: {', '.join(missing_columns)}")

    # Convertir la columna 'Sex' a valores numéricos
    new_data['Sex_gender'] = new_data['Sex_gender'].map({'f': 0, 'm': 1})

    # Codificar las columnas categóricas utilizando el mismo encoder
    new_data_encoded = encoder.transform(new_data[['Age', 'Weather', 'Event']])

    # Concatenar las variables codificadas con las características originales
    X_new = np.hstack((new_data_encoded.toarray(), new_data[['Sex_gender']].values))

    # Normalizar el nuevo vector de datos utilizando el mismo escalador
    new_data_scaled = scaler.transform(X_new)

    return new_data_scaled
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