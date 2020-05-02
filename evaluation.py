from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
import joblib


def evaluate(y_test, y_pred):
    print('\nConfusion_matrix:')
    print(confusion_matrix(y_test, y_pred))
    print('\nClassification_report:')
    print(classification_report(y_test, y_pred))
    print('\nAccuracy:')
    print(accuracy_score(y_test, y_pred))
    print()


def evaluate_from_report(filepath):
    report = joblib.load(filepath)
    evaluate(report[0], report[1])
