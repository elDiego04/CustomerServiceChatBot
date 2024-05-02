from modeloPredictivo import *



new_data = pd.DataFrame({'Age': ['Elderly'], 'Size': ['M'], 'Weather': ['Warm'], 'Sex_Gender': ['M'], 'Event': ['Funeral'], 'Satisfaction': [1] })
new_data['Sex_Gender'] = new_data['Sex_Gender'].map({'F': 0, 'M': 1})
new_data_encoded = encoder.transform(new_data[['Age', 'Size', 'Weather', 'Event']])
new_data_encoded = np.hstack((new_data_encoded.toarray(), new_data.drop(['Age', 'Size', 'Weather', 'Event'], axis=1)))
new_data_scaled = scaler.transform(new_data_encoded)
prediction = sakuraModel.predict(new_data_scaled)
print("Predicción:", prediction)

new_data = pd.DataFrame({'Age': ['Teenager'], 'Size': ['S'], 'Weather': ['Temperate'], 'Sex_Gender': ['M'], 'Event': ['Graduation'], 'Satisfaction': [0] })
new_data['Sex_Gender'] = new_data['Sex_Gender'].map({'F': 0, 'M': 1})
new_data_encoded = encoder.transform(new_data[['Age', 'Size', 'Weather', 'Event']])
new_data_encoded = np.hstack((new_data_encoded.toarray(), new_data.drop(['Age', 'Size', 'Weather', 'Event'], axis=1)))
new_data_scaled = scaler.transform(new_data_encoded)
prediction = sakuraModel.predict(new_data_scaled)
print("Predicción:", prediction)

new_data = pd.DataFrame({'Age': ['Teenager'], 'Size': ['M'], 'Weather': ['Temperate'], 'Sex_Gender': ['F'], 'Event': ["Quinceanera_party"], 'Satisfaction': [1] })
new_data['Sex_Gender'] = new_data['Sex_Gender'].map({'F': 0, 'M': 1})
new_data_encoded = encoder.transform(new_data[['Age', 'Size', 'Weather', 'Event']])
new_data_encoded = np.hstack((new_data_encoded.toarray(), new_data.drop(['Age', 'Size', 'Weather', 'Event'], axis=1)))
new_data_scaled = scaler.transform(new_data_encoded)
prediction = sakuraModel.predict(new_data_scaled)
print("Predicción:", prediction)

new_data = pd.DataFrame({'Age': ['Adult'], 'Size': ['XL'], 'Weather': ['Warm'], 'Sex_Gender': ['F'], 'Event': ['Baptism'], 'Satisfaction': [0] })
new_data['Sex_Gender'] = new_data['Sex_Gender'].map({'F': 0, 'M': 1})
new_data_encoded = encoder.transform(new_data[['Age', 'Size', 'Weather', 'Event']])
new_data_encoded = np.hstack((new_data_encoded.toarray(), new_data.drop(['Age', 'Size', 'Weather', 'Event'], axis=1)))
new_data_scaled = scaler.transform(new_data_encoded)
prediction = sakuraModel.predict(new_data_scaled)
print("Predicción:", prediction)

new_data = pd.DataFrame({'Age': ['Elderly'], 'Size': ['L'], 'Weather': ['Temperate'], 'Sex_Gender': ['M'], 'Event': ['Stag-party'], 'Satisfaction': [0] })
new_data['Sex_Gender'] = new_data['Sex_Gender'].map({'F': 0, 'M': 1})
new_data_encoded = encoder.transform(new_data[['Age', 'Size', 'Weather', 'Event']])
new_data_encoded = np.hstack((new_data_encoded.toarray(), new_data.drop(['Age', 'Size', 'Weather', 'Event'], axis=1)))
new_data_scaled = scaler.transform(new_data_encoded)
prediction = sakuraModel.predict(new_data_scaled)
print("Predicción:", prediction)
