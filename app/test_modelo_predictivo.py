import unittest
import pandas as pd
from unittest.mock import patch, mock_open
from io import StringIO
from modeloPredictivo import *

class TestSakuraModel(unittest.TestCase):
    def setUp(self):
        self.data = """Age;Weather;Sex_gender;Event;Type_Clothing_Event
Adulto;Frio;Femenino;Matrimonio;Vestido
Niño;Caliente;Masculino;Graduación;Traje
Adolescente;Lluvioso;Femenino;Cumpleaños;Falda
Adulto;Soleado;Masculino;Fiesta;Camisa
"""
        self.df = pd.read_csv(StringIO(self.data), sep=";")

    @patch('pandas.read_csv')
    def test_read_csv(self, mock_read_csv):
        mock_read_csv.return_value = self.df
        df = pd.read_csv(r"C:\Users\57305\OneDrive\Documentos\ExpertSystems\CustomerServiceChatBot\SakuraStylishDB.csv", delimiter=";")
        self.assertTrue(df.equals(self.df))

    def test_map_sex_gender(self):
        self.df['Sex_gender'] = self.df['Sex_gender'].map({'Femenino': 0, 'Masculino': 1})
        expected_values = [0, 1, 0, 1]
        self.assertEqual(list(self.df['Sex_gender']), expected_values)

    def test_train_test_split(self):
        X = self.df.drop('Type_Clothing_Event', axis=1)
        y = self.df['Type_Clothing_Event']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=99)
        self.assertEqual(len(X_train), 2)
        self.assertEqual(len(X_test), 2)
        self.assertEqual(len(y_train), 2)
        self.assertEqual(len(y_test), 2)

    @patch('joblib.dump')
    def test_dump_model(self, mock_dump):
        sakuraModel = RandomForestClassifier()
        joblib.dump(sakuraModel, 'modeloPredictivo.pkl')
        mock_dump.assert_called_once_with(sakuraModel, 'modeloPredictivo.pkl')

if __name__ == '__main__':
    unittest.main()