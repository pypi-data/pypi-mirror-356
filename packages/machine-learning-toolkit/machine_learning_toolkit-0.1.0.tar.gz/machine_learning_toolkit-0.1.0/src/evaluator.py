import time
from sklearn.pipeline import make_pipeline
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, ConfusionMatrixDisplay
)
import matplotlib.pyplot as plt

def evaluate_model(
    name,
    estimator,
    X_train,
    X_test,
    y_train,
    y_test,
    preprocess=None,
    zero_division=0,
    show_plot=True,
):
    """
    Evaluate a model and print key metrics along with the confusion matrix.
    
    Parameters:
        name (str): Model name.
        estimator: scikit-learn compatible model.
        X_train, X_test: Feature datasets.
        y_train, y_test: Label datasets.
        preprocess: Optional preprocessing pipeline or transformer.
        zero_division (int): Handling of zero-division in precision/recall.
        show_plot (bool): Whether to display the confusion matrix plot.
    
    Returns:
        dict: Dictionary of evaluation metrics.
    """
    if preprocess:
        pipe = make_pipeline(preprocess, estimator)
    else:
        pipe = make_pipeline(estimator)

    start_time = time.perf_counter()
    pipe.fit(X_train, y_train)
    y_pred = pipe.predict(X_test)
    end_time = time.perf_counter()

    metrics = {
        'Modelo': name,
        'Accuracy': round(accuracy_score(y_test, y_pred), 8),
        'Precision': round(precision_score(y_test, y_pred, zero_division=zero_division), 8),
        'Recall': round(recall_score(y_test, y_pred, zero_division=zero_division), 8),
        'F1': round(f1_score(y_test, y_pred, zero_division=zero_division), 8),
        'Tiempo Ejecución (segs)': round(end_time - start_time, 4)
    }

    if show_plot:
        labels = [False, True]
        cm = confusion_matrix(y_test, y_pred, labels=labels)
        disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['False', 'True'])
        fig, ax = plt.subplots(figsize=(5, 4))
        disp.plot(cmap='Blues', ax=ax, colorbar=True)
        ax.set_title(f"Matriz de confusión – {name}")
        plt.tight_layout()
        plt.show()

    return metrics
