from typing import Protocol
import numpy as np

class SklearnModel(Protocol):
    def fit(self, X, y): ...
    def predict(self, X) -> np.ndarray: ...
    def predict_proba(self, X) -> np.ndarray: ...


class Model:
    def __init__(self, model: SklearnModel):
        self._model = model

    def fit(self, X, y):
        return self._model.fit(X, y)

    def predict(self, X):
        return self._model.predict(X)

    def predict_proba(self, X):
        return self._model.predict_proba(X)
