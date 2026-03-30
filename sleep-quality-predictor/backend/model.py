import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle

# Load dataset
data = pd.read_csv('../dataset/sleep_data.csv')

# Print columns (check panna)
print(data.columns)

# Select needed columns (adjust if needed)
X = data[['Sleep Duration', 'Stress Level', 'Physical Activity Level']]
y = data['Quality of Sleep']

# Train test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Save model
pickle.dump(model, open('sleep_model.pkl', 'wb'))

print("Model trained and saved successfully!")