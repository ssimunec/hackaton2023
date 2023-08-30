import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier


def find_key(input_dict, value):
    for key, val in input_dict.items():
        if val == value: return key
    return "None"

# Load the CSV file into a DataFrame
data = pd.read_csv('data2.csv')

# Encode categorical variables (gender) using LabelEncoder
le = LabelEncoder()
data['Gender'] = le.fit_transform(data['Gender'])

gender_mapping = {i: label for i, label in enumerate(le.classes_)}

data['Sentiment'] = le.fit_transform(data['Sentiment'])

sentiment_mapping = {i: label for i, label in enumerate(le.classes_)}


data.to_csv('./data2_model.csv', sep='\t', encoding='utf-8')

# Split features (X) and target (y)
X = data[['Age', 'Gender', 'Sentiment']]
Y = data['Food']

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

accuracy = model.score(X_test, y_test)
print(f'Model Accuracy: {accuracy:.2f}')

# Create a new instance for recommendation (replace with actual values)

g = find_key(gender_mapping, 'woman')
s = find_key(sentiment_mapping, 'happy')

new_user = pd.DataFrame({'Age': [30], 'Gender': [g], 'Sentiment': [s]}) 
# Make a prediction
predicted_food = model.predict(new_user)
print(f'Recommended Food: {predicted_food[0]}')
