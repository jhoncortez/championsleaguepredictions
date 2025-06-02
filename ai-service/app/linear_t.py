# training sample with linear regression . just for fun
from training_data_processing import create_training_data 

import json
import pandas as pd
import joblib

# Load the data
# with open("cl-data-2024.json") as f:
# with open("cl-data-3seasons.json") as f:
#     data = json.load(f)

# Create training data
df = create_training_data()

# df.head()
df.to_csv("cl_seasons_matches_data_for_training.csv", index=False)

# graphic with seaborn to see initial behavior
import seaborn as sns
import matplotlib.pyplot as plt

# print latest 5 records in df 

sns.pairplot(df, hue="outcome")
sns.scatterplot(x="team1_win_rate", y="team2_win_rate", hue="outcome", data=df)
plt.savefig("seasons_data_plot.png")


# prepare independent and dependent variables
# X = df.iloc[:, 2].values.reshape(-1, 1)
# y = df.iloc[:, 3]
X = df.drop("outcome", axis=1)
y = df["outcome"]

# separate train and test data
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# train model with Lienal Regression
from sklearn.linear_model import LinearRegression

model = LinearRegression()
model.fit(X_train, y_train)

# predict outcome
y_pred = model.predict(X_test)

print('y_test {}'.format(y_test))
print('y_pred {}'.format(y_pred))

# evaluate model
from sklearn.metrics import mean_squared_error, r2_score
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f"Mean Squared Error: {mse:.2f}")
print(f"R-squared: {r2:.2f}")

sns.pairplot(df, hue="outcome")
sns.scatterplot(x="team1_win_rate", y="team2_win_rate", hue="outcome", data=df)
plt.plot(X_test, y_pred, color="red")
plt.savefig("seasons_data_plot_trained_lineal.png")

# save model
joblib.dump(model, "cl_linear_model.pkl")
# print(model.predict(df))