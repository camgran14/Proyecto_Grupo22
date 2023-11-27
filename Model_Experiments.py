import numpy as np
import pandas as pd
import mlflow
import mlflow.sklearn
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LassoCV, RidgeCV, ElasticNetCV
from sklearn import linear_model
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn import metrics

# importar conjunto de datos
def cargar_datos(filename, nombre_base):
    data = pd.read_excel(f"data/{filename}", index_col=0)
    return data


data = cargar_datos("BD_G22_P.xlsx", "Base de datos:")

# separar X y y
X = data.iloc[:, 1:11]
y = data["Puntaje_General_Estandarizado"]

# Dividir los datos en conjuntos de entrenamiento y prueba (80% entrenamiento, 20% prueba)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Modelos_Experimentos
# defina el servidor para llevar el registro de modelos y artefactos
# mlflow.set_tracking_uri('http://localhost:8080')
# registre el experimento
experiment = mlflow.set_experiment("Random_Forest_Experiments")

# Definir la grilla de hiperparámetros a probar para el RandomForestRegressor

n_estimators = [100, 200, 300, 400, 500]
max_depths = [None, 5, 10, 15]
min_samples_splits = [2, 5, 10]
min_samples_leafs = [1, 2, 4]

for n_estimator in n_estimators:
    for max_depth in max_depths:
        for min_samples_split in min_samples_splits:
            for min_samples_leaf in min_samples_leafs:
                with mlflow.start_run(
                    experiment_id=experiment.experiment_id,
                    run_name=f"random-forest-model-num_trees{n_estimator}-maxdepth{max_depth}-ssplit{min_samples_split}-sleaf{min_samples_leaf}",
                ):

                    # Crear el modelo de RandomForestRegressor
                    rf = RandomForestRegressor(
                        n_estimators=n_estimator,
                        max_depth=max_depth,
                        min_samples_split=min_samples_split,
                        min_samples_leaf=min_samples_leaf,
                    )
                    rf.fit(X_train, y_train)

                    predictions = rf.predict(X_test)

                    # Registre los parámetros
                    mlflow.log_param("num_trees", n_estimator)
                    mlflow.log_param("maxdepth", max_depth)
                    mlflow.log_param("min_samples_split", min_samples_split)
                    mlflow.log_param("min_samples_leaf", min_samples_leaf)

                    mlflow.sklearn.log_model(
                        rf,
                        f"random-forest-model-num_trees{n_estimator}-maxdepth{max_depth}-ssplit{min_samples_split}-sleaf{min_samples_leaf}",
                    )

                    mse = mean_squared_error(y_test, predictions)
                    mlflow.log_metric("mse", mse)
                    print(mse)
                    mlflow.end_run()


# registre el experimento
experiment_arbol = mlflow.set_experiment("Arbol_Decision_Experiments")

# Definir la grilla de hiperparámetros a probar para el arbol
max_depths = [None, 5, 10, 15]
min_samples_splits = [2, 5, 10]
min_samples_leafs = [1, 2, 4]

for max_depth in max_depths:
    for min_samples_split in min_samples_splits:
        for min_samples_leaf in min_samples_leafs:
            with mlflow.start_run(experiment_id=experiment_arbol.experiment_id):
                model = DecisionTreeRegressor(
                    max_depth=max_depth,
                    min_samples_split=min_samples_split,
                    min_samples_leaf=min_samples_leaf,
                )
                model.fit(X_train, y_train)
                predictions = model.predict(X_test)

                mse = np.mean((predictions - y_test) ** 2)

                mlflow.log_param("max_depth", max_depth)
                mlflow.log_param("min_samples_split", min_samples_split)
                mlflow.log_param("min_samples_leaf", min_samples_leaf)
                mlflow.log_metric("mse", mse)

                mlflow.sklearn.log_model(model, "decision-tree-model")
                mlflow.end_run()


# registre el experimento
experiment_lasso = mlflow.set_experiment("Linear_Regression_Lasso_Experiments")
# Experimento para LASSO
with mlflow.start_run(experiment_id=experiment_lasso.experiment_id):
    n_alphas = 300
    alphasCalibrar = np.logspace(-10, 2, n_alphas)
    modeloLASSO = LassoCV(alphas=alphasCalibrar).fit(X_train, y_train)
    prediccionLASSO = modeloLASSO.predict(X_test)
    mse = np.average(np.square(prediccionLASSO - y_test))
    mlflow.log_param("penalization", "LASSO")
    mlflow.log_param("alpha", modeloLASSO.alpha_)
    mlflow.log_metric("mse", mse)
    mlflow.end_run()


# registre el experimento
experiment_ridge = mlflow.set_experiment("Linear_Regression_Ridge_Experiments")
with mlflow.start_run(experiment_id=experiment_ridge.experiment_id):
    n_alphas = 300
    alphasCalibrar = np.logspace(-10, 2, n_alphas)
    modeloRidge = RidgeCV(alphas=alphasCalibrar, store_cv_values=True).fit(
        X_train, y_train
    )
    prediccionRidge = modeloRidge.predict(X_test)
    mse = np.average(np.square(prediccionRidge - y_test))
    mlflow.log_param("penalization", "Ridge")
    mlflow.log_param("alpha", modeloRidge.alpha_)
    mlflow.log_metric("mse", mse)
    mlflow.end_run()


# registre el experimento
experiment_elasticnet = mlflow.set_experiment(
    "Linear_Regression_ElasticNet_Experiments"
)
with mlflow.start_run(experiment_id=experiment_elasticnet.experiment_id):
    n_alphas = 300
    alphasCalibrar = np.logspace(-10, 2, n_alphas)
    modeloElastic = ElasticNetCV(alphas=alphasCalibrar, cv=5, random_state=0).fit(
        X_train, y_train
    )
    prediccionElastic = modeloElastic.predict(X_test)
    mse = np.average(np.square(prediccionElastic - y_test))
    mlflow.log_param("penalization", "ElasticNet")
    mlflow.log_param("alpha", modeloElastic.alpha_)
    mlflow.log_metric("mse", mse)
    mlflow.end_run()


def run_experiment(model, X_train, X_test, y_train, y_test, experiment_name):
    with mlflow.start_run(
        experiment_id=mlflow.set_experiment(experiment_name).experiment_id
    ):
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)
        mse = np.average(np.square(predictions - y_test))
        mlflow.log_param("penalization", model.__class__.__name__)
        mlflow.log_param("alpha", getattr(model, "alpha_", None))
        mlflow.log_metric("mse", mse)
        mlflow.end_run()


models = {
    "OLS": linear_model.LinearRegression(),
    "Lasso": LassoCV(alphas=np.logspace(-10, 2, 200)),
    "Ridge": RidgeCV(alphas=np.logspace(-10, 2, 200), store_cv_values=True),
    "ElasticNet": ElasticNetCV(alphas=np.logspace(-10, 2, 200), cv=5, random_state=0),
}

# Run experiments
for model_name, model in models.items():
    run_experiment(
        model,
        X_train,
        X_test,
        y_train,
        y_test,
        f"Linear_Regression_{model_name}_Experiments",
    )

# Additional models and hyperparameters
lasso_params = {"fit__alpha": [0.005, 0.02, 0.03, 0.05, 0.06]}
ridge_params = {"fit__alpha": [550, 580, 600, 620, 650]}

# Use X_train, X_test, y_train, y_test
pipe1 = Pipeline(
    [("poly", PolynomialFeatures()), ("fit", linear_model.LinearRegression())]
)

# Utiliza GridSearchCV para Lasso
lasso_search = GridSearchCV(
    Pipeline([("poly", PolynomialFeatures()), ("fit", linear_model.Lasso())]),
    param_grid=lasso_params,
).fit(X_train, y_train)

best_lasso_estimator = lasso_search.best_estimator_

pipe2 = Pipeline([("poly", PolynomialFeatures()), ("fit", best_lasso_estimator)])

# Utiliza GridSearchCV para Ridge
ridge_search = GridSearchCV(
    Pipeline([("poly", PolynomialFeatures()), ("fit", linear_model.Ridge())]),
    param_grid=ridge_params,
).fit(X_train, y_train)

best_ridge_estimator = ridge_search.best_estimator_

pipe3 = Pipeline([("poly", PolynomialFeatures()), ("fit", best_ridge_estimator)])

models3 = {"OLS": pipe1, "Lasso": pipe2, "Ridge": pipe3}

# Run additional experiments
for model_name, model in models3.items():
    run_experiment(
        model,
        X_train,
        X_test,
        y_train,
        y_test,
        f"Polynomial_Regression_{model_name}_Experiments",
    )
