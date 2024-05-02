from flask import Flask, render_template, request, jsonify
import joblib

app = Flask(__name__)
model = joblib.load('modeloPredictivo.pkl')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # Obtener los datos de entrada de la solicitud
            data = request.json['data']

            # Realizar la predicción utilizando el modelo cargado
            prediction = model.predict([data])[0]

            # Mapear el número de clase a la etiqueta correspondiente
            target_names = ['Age', 'Size', 'Weather', 'Sex_Gender', 'Event', 'Satisfaction']
            predicted_class = target_names[prediction]

            return jsonify({'prediction': predicted_class})
        except Exception as e:
            # Manejar cualquier error que ocurra durante la predicción
            return jsonify({'error': str(e)}), 400
    else:
        # Renderizar la página de inicio
        return render_template('index.html')

@app.route('/carrito')
def carrito():
    # Renderizar la página del carrito
    return render_template('carrito.html')

if __name__ == "__main__":
    app.run(debug=True)
