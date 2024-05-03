from flask import Flask, render_template, request, jsonify
import joblib

app = Flask(__name__)

# Cargar el modelo entrenado al inicio de la aplicación
model = joblib.load('modeloPredictivo.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Obtener las respuestas del usuario desde la solicitud
        data = request.json['data']

        # Convertir las respuestas en un arreglo NumPy
        input_data = [list(data.values())]

        # Realizar la predicción utilizando el modelo cargado
        prediction = model.predict(input_data)[0]

        return jsonify({'prediction': prediction})
    except Exception as e:
        # Manejar cualquier error que ocurra durante la predicción
        return jsonify({'error': str(e)}), 400

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