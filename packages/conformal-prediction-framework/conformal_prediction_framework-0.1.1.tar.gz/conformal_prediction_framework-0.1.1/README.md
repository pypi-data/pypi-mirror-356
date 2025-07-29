# Conformal Prediction Framework

Conformal Prediction Framework is a modular and extensible implementation of Conformal Predictors for classification problems. It is compatible with any model that follows the scikit-learn interface (`fit`, `predict`, `predict_proba`) and provides prediction sets with finite-sample statistical guarantees.

This framework allows practitioners to control the error rate of predictions under minimal assumptions and provides functionality for evaluating both coverage and prediction set size.

## Installation

Install via pip:

```bash
pip install conformal-prediction-framework
````

## Usage Example

```python
import numpy as np
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

from conformal_prediction_framework import ConformalClassifier, Model

# Step 1: Generate synthetic data
X, y = make_classification(
    n_samples=1000,
    n_features=20,
    n_classes=3,
    n_informative=10,
    random_state=42
)

# Step 2: Split into training, calibration, and test sets
X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.4, random_state=42)
X_calib, X_test, y_calib, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

# Step 3: Wrap your classifier and create the conformal predictor
base_model = LogisticRegression(multi_class='multinomial', max_iter=1000)
model = Model(base_model)
conformal = ConformalClassifier(model=model, alpha=0.1)

# Step 4: Train and calibrate
conformal.fit(X_train, y_train)
conformal.get_nonconformity_scores(X_calib, y_calib)
conformal.calibrate_quantile()

# Step 5: Predict and evaluate
prediction_sets = conformal.get_prediction_sets(X_test)
coverage = conformal.evaluate_coverage(X_test, y_test)
avg_set_size = conformal.evaluate_average_set_size(X_test)
point_predictions = conformal.predict(X_test)

# Output results
print(f"Coverage: {coverage:.3f}")
print(f"Average prediction set size: {avg_set_size:.2f}")
print(f"Sample prediction sets: {prediction_sets[:5]}")
print(f"Point predictions: {point_predictions[:5]}")
```

## Features

* Wraps any scikit-learn-like classifier.
* Provides conformal prediction sets with guaranteed coverage.
* Computes empirical coverage and average prediction set size.
* Modular design for extensibility.

## License

This project is licensed under the MIT License.