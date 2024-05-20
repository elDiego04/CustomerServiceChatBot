import pytest
from app import app, prepara_datos_para_modelo

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# Pruebas para la función prepara_datos_para_modelo
def test_prepara_datos_para_modelo_valores_vacios():
    data = {
        'Sex_gender': 'Femenino',
        'Age': '',
        'Weather': 'Soleado',
        'Event': 'Concierto'
    }
    with pytest.raises(ValueError):
        prepara_datos_para_modelo(data)

def test_prepara_datos_para_modelo_genero_invalido():
    data = {
        'Sex_gender': 'Otro',
        'Age': '25',
        'Weather': 'Soleado',
        'Event': 'Concierto'
    }
    with pytest.raises(ValueError):
        prepara_datos_para_modelo(data)

def test_prepara_datos_para_modelo_edad_invalida():
    data = {
        'Sex_gender': 'Femenino',
        'Age': '-5',
        'Weather': 'Soleado',
        'Event': 'Concierto'
    }
    with pytest.raises(ValueError):
        prepara_datos_para_modelo(data)

def test_prepara_datos_para_modelo_clima_invalido():
    data = {
        'Sex_gender': 'Masculino',
        'Age': '25',
        'Weather': 'InvalidWeather',
        'Event': 'Concierto'
    }
    with pytest.raises(ValueError):
        prepara_datos_para_modelo(data)

def test_prepara_datos_para_modelo_evento_invalido():
    data = {
        'Sex_gender': 'Masculino',
        'Age': '25',
        'Weather': 'Soleado',
        'Event': 'InvalidEvent'
    }
    with pytest.raises(ValueError):
        prepara_datos_para_modelo(data)



# Pruebas para la ruta /carrito
def test_carrito(client):
    response = client.get('/carrito')
    assert response.status_code == 200
    assert b'<title>Carrito</title>' in response.data


def test_predict_method_not_allowed(client):
    response = client.get('/predict')
    assert response.status_code == 405

