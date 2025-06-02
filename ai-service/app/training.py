# Create training DataFrame
# df = create_training_data(all_matches)

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

def train_model(df):

    X = df.drop("outcome", axis=1) # Convert to numpy array what we need for the RandomForestClassifier model
    
    y = df["outcome"] # outcome for random forest model

    print("X :", X)
    print("y :", y)

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # from sklearn.ensemble import GradientBoostingClassifier
    # from xgboost import XGBClassifier

    # # Train model Random Forest Classifier
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=5,
        random_state=42,
        class_weight="balanced"  # Important for imbalanced datasets
    )

    # # Train model Gradient Boosting Classifier
    # model = GradientBoostingClassifier(
    #     n_estimators=300,
    #     learning_rate=0.1,
    #     random_state=42 
    # )

    # Train model XGBoost Classifier
    # model = XGBClassifier(
    #     n_estimators=300,
    #     learning_rate=0.1,
    #     random_state=42 
    # )

    # Add cross-validation
    from sklearn.model_selection import cross_val_score
    cv_scores = cross_val_score(model, X_train, y_train, cv=5)
    print(f"Cross-validation scores: {cv_scores}")
    print(f"Mean CV accuracy: {cv_scores.mean():.2f}")

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    print('Predictions:{} | real data {}'.format(y_pred[:4], y_test[:4]))

    # # # Hyperparameter tuning
    # # param_grid = {
    # #     'n_estimators': [100, 200, 300],
    # #     'max_depth': [None, 5, 10],
    # #     'min_samples_split': [2, 5, 10],
    # #     'min_samples_leaf': [1, 5, 10]
    # # }

    # # grid_search = GridSearchCV(RandomForestClassifier(random_state=42), param_grid, cv=5)
    # # grid_search.fit(X_train, y_train)

    # # print("Best parameters:", grid_search.best_params_)
    # # print("Best score:", grid_search.best_score_)

    # # model = grid_search.best_estimator_
    # # model.fit(X_train, y_train)

    # # # Add cross-validation
    # # from sklearn.model_selection import cross_val_score
    # # cv_scores = cross_val_score(model, X_train, y_train, cv=5)
    # # print(f"Cross-validation scores: {cv_scores}")
    # # print(f"Mean CV accuracy: {cv_scores.mean():.2f}")

    # # y_pred = model.predict(X_test)

    # # print('Predictions:{} | real data {}'.format(y_pred[:4], y_test[:4]))

    from sklearn.metrics import mean_squared_error, r2_score
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f"Mean Squared Error: {mse:.2f}")
    print(f"R-squared: {r2:.2f}")

    # grafic evaluation
    from sklearn.metrics import pair_confusion_matrix, classification_report, confusion_matrix
    import matplotlib.pyplot as plt
    # pair_confusion_matrix(y_test, y_pred)
    # plt.show()

    plt.plot(X_test, y_test, 'ro')
    plt.plot(X_test, y_pred)
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.savefig('plot.png')

    import seaborn as sns
    sns.pairplot(df, hue="outcome")
    sns.scatterplot(x="team1_win_rate", y="team2_win_rate", hue="outcome", data=df)
    plt.plot(X_test, y_pred, color="red")
    plt.savefig("seasons_data_plot_trained_classifier.png")

    # Enhanced evaluation
    print(classification_report(y_test, y_pred))
    print(confusion_matrix(y_test, y_pred))

    # Save model
    # joblib.dump(model, "champions_league_model_3seasons.pkl")
    joblib.dump(model, "enhanced_champions_league_model.pkl")

    # # Make predictions on the testing data
    # y_pred = model.predict(X_test)

    # Evaluate the model's performance
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model accuracy: {accuracy:.3f}")



### initial training processing

from training_data_processing import create_training_data
df = create_training_data()
df.to_csv("cl_3seasons_matches.csv", index=False)
train_model(df)