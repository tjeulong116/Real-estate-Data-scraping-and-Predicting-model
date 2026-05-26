import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import SimpleImputer, IterativeImputer, KNNImputer
from sklearn.preprocessing import StandardScaler, OrdinalEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score

#Read file
data = pd.read_csv(filepath_or_buffer="", header = 0)

#Split data
target = "price_range"
X = data[["area", "number_of_bedrooms", "number_of_bathrooms", "number_of_stories", "front_length", "legal_status", "old_address"]]
y = data[target]

X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, random_state=42)

#Preprocessing
numerical_transform = Pipeline(steps = [
    ("fill_nan", IterativeImputer(max_iter=30, random_state=42)),
    ("scaler", StandardScaler())
])

legal_status_categories = [True, False]
ordinal_transform = Pipeline(steps= [
    ("encoder", OrdinalEncoder(categories= [legal_status_categories], handle_unknown="use_encoded_value", unknown_value=np.nan)),
    ("fill_nan", KNNImputer())
])

nominal_transform = Pipeline(steps= [
    ("fill_nan", SimpleImputer(strategy="most_frequent")),
    ("encode", OneHotEncoder(sparse_output=False, handle_unknown="ignore"))
])

ct = ColumnTransformer(transformers= [
    ("numerical_columns", numerical_transform, ["area", "number_of_bedrooms", "number_of_bathrooms", "number_of_stories", "front_length"]),
    ("ordinal_boolean_columns", ordinal_transform, ["legal_status"]),
    ("nominal_columns", nominal_transform, ["old_address"])
])

#Training
reg = Pipeline(steps= [
    ("preprocessing", ct),
    ("training", RandomForestRegressor(random_state=42))
])

params: dict = {
    "preprocessing__ordinal_boolean_columns__fill_nan__n_neighbors": range(3,10,2),
    "training__n_estimators": range(50,501,50),
    "training__criterion": ["squared_error", "absolute_error", "friedman_mse", "poisson"]
}

grid_search = GridSearchCV(estimator=reg, param_grid=params, scoring="r2", n_jobs=7, cv=5, verbose=2)
grid_search.fit(X=X_train, y=y_train)

print(grid_search.best_estimator_)
print(grid_search.best_score_)
print(grid_search.best_params_)

#Evaluating
y_prediction = grid_search.best_estimator_.predict(X = X_test)
print("MAE :", mean_absolute_error(y_true = y_test, y_pred = y_prediction))
print("MSE :", root_mean_squared_error(y_true = y_test, y_pred = y_prediction))
print("R2 :", r2_score(y_true = y_test, y_pred = y_prediction))