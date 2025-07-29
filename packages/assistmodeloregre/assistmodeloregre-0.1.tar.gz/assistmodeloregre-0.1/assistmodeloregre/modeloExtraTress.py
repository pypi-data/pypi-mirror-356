from sklearn.ensemble import ExtraTreesRegressor
import numpy as np

class modeloExtraTress:
    def __init__(self, modelo_base):
        self.modelo_base = modelo_base

    def fit(self, X, y):
        self.modelo_base.fit(X, y)

    def predict(self, X):
        all_preds = np.array([tree.predict(X) for tree in self.modelo_base.estimators_])
        mean_preds = np.mean(all_preds, axis=0)
        std_preds = np.std(all_preds, axis=0)
        confianza = 1 / (1 + std_preds)
        return np.column_stack((mean_preds, confianza))

