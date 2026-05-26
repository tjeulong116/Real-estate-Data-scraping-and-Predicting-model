import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import SimpleImputer, IterativeImputer, KNNImputer
from sklearn.preprocessing import StandardScaler, OrdinalEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score
from lazypredict.Supervised import LazyRegressor


#Read file
data = pd.read_csv(filepath_or_buffer="", header = 0)

#Split data
target = "price_range"
X = data[["area", "number_of_bedrooms", "number_of_bathrooms", "number_of_stories", "front_length", "legal_status", "old_address"]]
y = data[target]

X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, random_state=42)

#Preprocessing
numerical_transform = Pipeline(steps = [
    ("fill nan", IterativeImputer(max_iter=30, random_state=42)),
    ("scaler", StandardScaler())
])

legal_status_categories = [True, False]
ordinal_transform = Pipeline(steps= [
    ("encoder", OrdinalEncoder(categories= [legal_status_categories], handle_unknown="use_encoded_value", unknown_value=np.nan)),
    ("fill_nan", KNNImputer(n_neighbors= 5, weights="uniform"))
])

nominal_transform = Pipeline(steps= [
    ("fill nan", SimpleImputer(strategy="most_frequent")),
    ("encode", OneHotEncoder(sparse_output=False))
])

ct = ColumnTransformer(transformers= [
    ("numerical_columns", numerical_transform, ["area", "number_of_bedrooms", "number_of_bathrooms", "number_of_stories", "front_length"]),
    ("ordinal/boolean columns", ordinal_transform, ["legal_status"]),
    ("nominal columns", nominal_transform, ["old_address"])
])

# #Lazy predict
# X_train = ct.fit_transform(X_train)
# X_test = ct.transform(X_test)
# clf = LazyRegressor(verbose=0, ignore_warnings=True, custom_metric=None)
# models, predictions = clf.fit(X_train, X_test, y_train, y_test)
# print(models)


# Training
reg = Pipeline(steps= [
    ("preprocessing", ct),
    ("training", LinearRegression())
])

#Evaluating
y_prediction = reg.predict(X = X_test)
print("MAE :", mean_absolute_error(y_true = y_test, y_pred = y_prediction))
print("MSE :", root_mean_squared_error(y_true = y_test, y_pred = y_prediction))
print("R2 :", r2_score(y_true = y_test, y_pred = y_prediction))