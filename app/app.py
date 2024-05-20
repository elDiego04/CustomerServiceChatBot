from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np
from modeloPredictivo import encoder, scaler

app = Flask(__name__)

# Cargar el modelo entrenado al inicio de la aplicación
model = joblib.load('modeloPredictivo.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Obtener las respuestas del usuario desde la solicitud
        data = request.get_json()
        if data is None:
            return jsonify({'error': 'No se proporcionaron datos'}), 400

        print("Datos recibidos:", data)

        # Convertir las respuestas en un formato adecuado para el modelo
        input_data = prepara_datos_para_modelo(data)
        print("Datos preparados para el modelo:", input_data)
        prediction = model.predict(input_data)[0]
        print("Predicción:", prediction)
        return jsonify({'prediction': prediction})

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
    sex_gender = data['Sex_gender'].lower()
    sex_mapping = {'femenino': 0, 'masculino': 1}
    if sex_gender not in sex_mapping:
        raise ValueError("Valor de género no válido. Debe ser 'Femenino' o 'Masculino'.")
    sex_numeric = sex_mapping[sex_gender]

    # Codificar las columnas categóricas utilizando el mismo encoder
    try:
        new_data_encoded = encoder.transform([[data['Age'], data['Weather'], data['Event']]])
    except ValueError as e:
        raise ValueError(f"Error al codificar características categóricas: {str(e)}")

    # Concatenar las variables codificadas con las características originales
    X_new = np.hstack((new_data_encoded.toarray(), [[sex_numeric]]))

    # Normalizar el nuevo vector de datos utilizando el mismo escalador
    try:
        X_new_scaled = scaler.transform(X_new)
    except ValueError as e:
        raise ValueError(f"Error al escalar características numéricas: {str(e)}")

    return X_new_scaled

@app.route('/')
def index():
    # Renderizar la página de inicio
    return render_template('index.html', title='Inicio')

@app.route('/carrito')
def carrito():
    # Renderizar la página del carrito
    return render_template('carrito.html', title='Carrito')

if __name__ == "__main__":
    app.run(debug=True)