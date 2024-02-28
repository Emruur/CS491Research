import os
import json
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Step 1: Preprocess JSON Data
def read_json_features(folder_path):
    data = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.json'):
            with open(os.path.join(folder_path, file_name)) as f:
                features = json.load(f)
                features['id'] = file_name.split('.')[0]  # Extract ID from filename
                data.append(features)
    return pd.DataFrame(data)

features_df = read_json_features('features')

# Step 2: Preprocess Scores File
def read_scores(file_path):
    scores = {}
    with open(file_path) as f:
        for line in f:
            parts = line.split()
            id = parts[0]
            scores_list = [float(score) for score in parts[1:] if score]
            scores[id] = sum(scores_list) / len(scores_list)  # Average if double scored
    return scores

scores = read_scores('scores.txt')
scores_df = pd.DataFrame(list(scores.items()), columns=['id', 'score'])

# Step 3: Merge Data
merged_df = pd.merge(features_df, scores_df, on='id')

# Step 4: Train the Model
X = merged_df.drop(['id', 'score'], axis=1)
y = merged_df['score']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

# Predict and evaluate
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error: {mse}')

# You can now use model.predict() on new data to predict scores
