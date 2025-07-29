from sklearn.base import BaseEstimator, ClassifierMixin
import numpy as np
from base.model import Model

class ConformalClassifier(BaseEstimator,ClassifierMixin):
    def __init__(self,model:Model,alpha: float):
        self.model = model
        self.alpha = alpha
        self.calibration_scores_ = None
        self.quantile_ = None

    def fit(self,X_train,y_train):
        return self.model.fit(X_train,y_train)

    def predict_proba(self,X):
        return self.model.predict_proba(X)
    
    def get_nonconformity_scores(self, X_calib,y_calib):
        calib_matrix = self.predict_proba(X=X_calib)
        nonconformity_scores = [1-calib_matrix[i,y_calib[i]] for i in range(len(y_calib))]
        self.calibration_scores_ = np.array(nonconformity_scores)
        return self.calibration_scores_
    
    def get_prediction_sets(self,X):
        if self.quantile_ is None:
            raise Exception("You must run calibrate_quantile() before predicting.")
        
        probas = self.predict_proba(X)
        prediction_sets = []
        for i in range(probas.shape[0]):
            current_probas = probas[i]
            prediction_set = [k for k,p in enumerate(current_probas) if 1-p <=self.quantile_]
            prediction_sets.append(prediction_set)
        
        return prediction_sets
    
    def calibrate_quantile(self):
        if self.calibration_scores_ is None:
            raise Exception("Calculate the Calibration Scores first, using get_nonconformity_scores(X_calib,y_calib).")
        self.quantile_ = np.quantile(self.calibration_scores_, 1 - self.alpha, method="higher")
        return self.quantile_
    
    def predict(self,X):
        prediction_sets = self.get_prediction_sets(X)
        proba = self.predict_proba(X)
        output = []
        for i in range(X.shape[0]):
            pred_set = prediction_sets[i]

            if not pred_set:
                output.append(np.nan)
                continue
            
            class_probs = {k: proba[i][k] for k in pred_set}
            best_class = best_class = min(
                    [k for k in class_probs if class_probs[k] == max(class_probs.values())]
                    )
            output.append(best_class)

        return np.array(output)

    def evaluate_coverage(self, X_test, y_test):
        prediction_sets = self.get_prediction_sets(X_test)
        correct = sum(1 for i in range(len(y_test)) if y_test[i] in prediction_sets[i])
        return correct/len(y_test)
    
    def evaluate_average_set_size(self, X_test):
        prediction_sets = self.get_prediction_sets(X_test)
        sum_len = sum(len(C) for C in prediction_sets)
        return sum_len/X_test.shape[0]

