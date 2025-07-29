# This file is part of the Audiovisually project.
# Here we can find some functions to evaluate our model(s) and perform some analysis on the results.
# The current functions are:

# ...

# Feel free to add any functions you find useful.

import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, f1_score, classification_report, confusion_matrix
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

def evaluate_model(model_path, df, text_column="Sentence", label_column="True Emotion", label_list=None, batch_size=8):
    """
    Evaluate a transformer model on a labeled dataset and return metrics and predictions.

    Args:
        model_path (str): Path to the trained model directory or Hugging Face model name.
        df (pd.DataFrame): DataFrame containing text and true labels.
        text_column (str): Name of the column with input text.
        label_column (str): Name of the column with true labels.
        label_list (list, optional): List of label names. Defaults to standard 7 emotions.
        batch_size (int): Batch size for prediction.

    Returns:
        dict: {
            "accuracy": float,
            "f1": float,
            "classification_report": dict or None,
            "classification_report_message": str or None,
            "confusion_matrix": np.ndarray,
            "result_df": pd.DataFrame
        }

    Example:
        >>> from audiovisually.evaluate import evaluate_model
        >>> df = pd.DataFrame({'Sentence': ['I am happy', 'I am sad'], 'True Emotion': ['happiness', 'sadness']})
        >>> results = evaluate_model("distilroberta-base", df)
        >>> print(results["accuracy"])
        >>> print(results["result_df"].head())
    """
    # Load model and tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSequenceClassification.from_pretrained(model_path)
    model.eval()
    if label_list is None:
        label_list = ['anger', 'sadness', 'disgust', 'fear', 'surprise', 'neutral', 'happiness']
    label2id = {label: i for i, label in enumerate(label_list)}
    id2label = {i: label for i, label in enumerate(label_list)}

    # Prepare data
    texts = df[text_column].tolist()
    true_labels = df[label_column].tolist()
    true_ids = [label2id.get(lbl, -1) for lbl in true_labels]

    # Predict in batches
    preds = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        inputs = tokenizer(batch, return_tensors="pt", padding=True, truncation=True, max_length=128)
        with torch.no_grad():
            outputs = model(**inputs)
            batch_preds = outputs.logits.argmax(dim=1).cpu().numpy()
            preds.extend(batch_preds)
    pred_labels = [id2label[p] for p in preds]

    # Metrics
    acc = accuracy_score(true_ids, preds)
    f1 = f1_score(true_ids, preds, average="weighted")
    # Always include all classes in the report, even if some are missing in the data
    try:
        report = classification_report(
            true_ids,
            preds,
            labels=list(range(len(label_list))),
            target_names=label_list,
            output_dict=True,
            zero_division=0
        )
        report_message = None
    except ValueError as e:
        report = None
        report_message = f"Classification report not available: {str(e)}"
    cm = confusion_matrix(true_ids, preds)

    # Add predictions to DataFrame
    result_df = df.copy()
    result_df["Predicted"] = pred_labels

    return {
        "accuracy": acc,
        "f1": f1,
        "classification_report": report,
        "classification_report_message": report_message,
        "confusion_matrix": cm,
        "result_df": result_df
    }

def compare_models(model_path_1, model_path_2, df, text_column="Sentence", label_column="True Emotion", label_list=None):
    """
    Compare two transformer models on the same labeled dataset.

    Args:
        model_path_1 (str): Path to the first model directory or Hugging Face model name.
        model_path_2 (str): Path to the second model directory or Hugging Face model name.
        df (pd.DataFrame): DataFrame containing text and true labels.
        text_column (str): Name of the column with input text.
        label_column (str): Name of the column with true labels.
        label_list (list, optional): List of label names. Defaults to standard 7 emotions.

    Returns:
        dict: {
            "model_1": {
                "accuracy": float,
                "f1": float,
                "classification_report": dict or None,
                "classification_report_message": str or None,
                "confusion_matrix": np.ndarray,
                "result_df": pd.DataFrame
            },
            "model_2": {
                "accuracy": float,
                "f1": float,
                "classification_report": dict or None,
                "classification_report_message": str or None,
                "confusion_matrix": np.ndarray,
                "result_df": pd.DataFrame
            }
        }

    Example:
        >>> from audiovisually.evaluate import compare_models
        >>> df = pd.DataFrame({'Sentence': ['I am happy', 'I am sad'], 'True Emotion': ['happiness', 'sadness']})
        >>> results = compare_models("distilroberta-base", "cardiffnlp/twitter-roberta-base-emotion", df)
        >>> print(results["model_1"]["accuracy"])
        >>> print(results["model_2"]["result_df"].head())
    """
    eval1 = evaluate_model(model_path_1, df, text_column, label_column, label_list)
    eval2 = evaluate_model(model_path_2, df, text_column, label_column, label_list)
    return {
        "model_1": eval1,
        "model_2": eval2
    }
