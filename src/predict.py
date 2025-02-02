# author : Valli Akella
# date: 2021-11-25

"""This code predicts the contraceptive method used based on the model derived from a pickle file and generates PR curve, Roc
curve, classification report and confusion matrix.
Usage: predict.py --test_path=<test_path>, --model=<model>, --output_path=<output_path>

Options:
--test_path=<test_path>        path to the test set
--model=<model>                pickle file containing to predict the targets of the testdata
--output_path=<output_path>    path to save the files from the script locally
 """


import sys
import time
import os
import string

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import (
    
    classification_report,
    confusion_matrix,
    roc_curve
)
from sklearn.metrics import PrecisionRecallDisplay 
from sklearn.metrics import RocCurveDisplay 
from sklearn.metrics import ConfusionMatrixDisplay
from docopt import docopt
from sklearn.inspection import permutation_importance


#%matplotlib inline
import pickle

opt = docopt(__doc__)
def main(test_path,model, output_path):
    # train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)
    
    #splitting into X_train and y_train
    #X_train, y_train = train_df.drop(columns=["Contraceptive_method_used"]), train_df["Contraceptive_method_used"]

    #splitting into X_test and y_test
    X_test, y_test = test_df.drop(columns=["Contraceptive_method_used"]), test_df["Contraceptive_method_used"]
    
    
    #Converting it to a binary model(train set)
    # y_train = y_train.replace(1,0)
    # y_train = y_train.replace([2,3],1)
    
    #Converting it to a binary model(test set)
    y_test = y_test.replace(1,0)
    y_test = y_test.replace([2,3],1)

    final_svc_model = pickle.load(open(model, "rb"))

    #Predictions on the test data
    y_pred = final_svc_model.predict(X_test)
    pred_df = pd.DataFrame(y_pred, y_test)


    #Confusion Matrix
    # final_svc_model.fit(X_train, y_train)
    cm = ConfusionMatrixDisplay.from_estimator(
    final_svc_model, X_test, y_test, values_format="d", display_labels=["contra_no", "contra_yes"]
)
    plt.savefig(output_path +"cm.png")

    #Classification Report
    cl_report = pd.DataFrame(classification_report(
        y_test, y_pred, target_names=["contra_no", "contra_yes"], output_dict=True)).T
    cl_report['precision']['accuracy'] = None
    cl_report['recall']['accuracy'] = None
    cl_report['support']['accuracy'] = None
    cl_report.to_csv(output_path + "cl_report.csv")
    
    # Generate PR Curve
    pr_curve = PrecisionRecallDisplay.from_estimator(final_svc_model, X_test, y_test)
    plt.savefig(output_path + "pr_curve.png")

    # Generate ROC Curve
    
    roc_plot = RocCurveDisplay.from_estimator(final_svc_model, X_test, y_test)
    plt.savefig(output_path + "roc_curve.png")
    
    perm_importance = permutation_importance(final_svc_model, X_test, y_test)
    feature_names = X_test.columns
    features = np.array(feature_names)
    plt.figure(figsize= (15,10))
    sorted_idx = perm_importance.importances_mean.argsort()
    plt.barh(features[sorted_idx], perm_importance.importances_mean[sorted_idx])
    plt.yticks(fontsize=8)
    plt.xlabel("Permutation Importance")
    plt.savefig(output_path + "feature_imp.png")
    
    
if __name__ == "__main__":
    main(opt["--test_path"], opt["--model"],opt["--output_path"])


     
