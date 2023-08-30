import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

class Recommender:
    def __init__(self):
        # Load the CSV file into a DataFrame
        self.data = pd.read_csv('./data/data_recommend.csv')

        # Encode categorical variables (gender) using LabelEncoder
        le = LabelEncoder()
        self.data['Gender'] = le.fit_transform(self.data['Gender'])

        self.gender_mapping = {i: label for i, label in enumerate(le.classes_)}

        self.data['Sentiment'] = le.fit_transform(self.data['Sentiment'])

        self.sentiment_mapping = {i: label for i, label in enumerate(le.classes_)}

        self.data.to_csv('./data/data2_model.csv', sep='\t', encoding='utf-8')

        # Split features (X) and target (y)
        X = self.data[['Age', 'Gender', 'Sentiment']]
        Y = self.data['Food']

        X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X_train, y_train)

        accuracy = self.model.score(X_test, y_test)
        print(f'Model Accuracy: {accuracy:.2f}')

    def run(self, age, gender, sentiment):
        g = self.find_key(self.gender_mapping, gender)
        s = self.find_key(self.sentiment_mapping, sentiment)

        new_user = pd.DataFrame({'Age': [age], 'Gender': [g], 'Sentiment': [s]}) 
        # Make a prediction
        predicted_food = self.model.predict(new_user)
        print(f'Recommended Food: {predicted_food[0]}')

        return predicted_food[0]

    def find_key(self, input_dict, value):
        for key, val in input_dict.items():
            if val == value: return key
        return "None"





# Create a new instance for recommendation (replace with actual values)


