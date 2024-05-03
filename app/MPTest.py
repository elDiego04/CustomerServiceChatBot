from modeloPredictivo import *



new_data = pd.DataFrame({'Age': ['Elderly'], 'Weather': ['Warm'], 'Sex_gender': ['M'], 'Event': ['Funeral'] })
new_data['Sex_gender'] = new_data['Sex_gender'].map({'F': 0, 'M': 1})
new_data_encoded = encoder.transform(new_data[['Age', 'Weather', 'Event']])
new_data_encoded = np.hstack((new_data_encoded.toarray(), new_data.drop(['Age', 'Weather', 'Event'], axis=1)))
new_data_scaled = scaler.transform(new_data_encoded)
prediction = sakuraModel.predict(new_data_scaled)
print("Predicción:", prediction)

new_data = pd.DataFrame({'Age': ['Teenager'], 'Weather': ['Temperate'], 'Sex_gender': ['M'], 'Event': ['Graduation']})
new_data['Sex_gender'] = new_data['Sex_gender'].map({'F': 0, 'M': 1})
new_data_encoded = encoder.transform(new_data[['Age', 'Weather', 'Event']])
new_data_encoded = np.hstack((new_data_encoded.toarray(), new_data.drop(['Age', 'Weather', 'Event'], axis=1)))
new_data_scaled = scaler.transform(new_data_encoded)
prediction = sakuraModel.predict(new_data_scaled)
print("Predicción:", prediction)

new_data = pd.DataFrame({'Age': ['Teenager'], 'Weather': ['Temperate'], 'Sex_gender': ['F'], 'Event': ["Quinceanera_party"]})
new_data['Sex_gender'] = new_data['Sex_gender'].map({'F': 0, 'M': 1})
new_data_encoded = encoder.transform(new_data[['Age', 'Weather', 'Event']])
new_data_encoded = np.hstack((new_data_encoded.toarray(), new_data.drop(['Age', 'Weather', 'Event'], axis=1)))
new_data_scaled = scaler.transform(new_data_encoded)
prediction = sakuraModel.predict(new_data_scaled)
print("Predicción:", prediction)

new_data = pd.DataFrame({'Age': ['Adult'],  'Weather': ['Warm'], 'Sex_gender': ['F'], 'Event': ['Baptism']})
new_data['Sex_gender'] = new_data['Sex_gender'].map({'F': 0, 'M': 1})
new_data_encoded = encoder.transform(new_data[['Age', 'Weather', 'Event']])
new_data_encoded = np.hstack((new_data_encoded.toarray(), new_data.drop(['Age', 'Weather', 'Event'], axis=1)))
new_data_scaled = scaler.transform(new_data_encoded)
prediction = sakuraModel.predict(new_data_scaled)
print("Predicción:", prediction)

new_data = pd.DataFrame({'Age': ['Elderly'],  'Weather': ['Temperate'], 'Sex_gender': ['M'], 'Event': ['Stag-party'] })
new_data['Sex_gender'] = new_data['Sex_gender'].map({'F': 0, 'M': 1})
new_data_encoded = encoder.transform(new_data[['Age', 'Weather', 'Event']])
new_data_encoded = np.hstack((new_data_encoded.toarray(), new_data.drop(['Age', 'Weather', 'Event'], axis=1)))
new_data_scaled = scaler.transform(new_data_encoded)
prediction = sakuraModel.predict(new_data_scaled)
print("Predicción:", prediction)