import pytest
import pandas as pd
import numpy as np
import os

# Path to your real model
MODEL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../best_model"))
print(MODEL_PATH)

# (1) - Preparation: Sample DataFrame for testing
@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "Sentence": ["I am happy", "I am sad", "I am angry"],
        "True Emotion": ["happiness", "sadness", "anger"]
    })

## ---------------  (1) evaluate_model main functionality ------------------------------

# (1) - Test 1: Basic evaluation with default label list
def test_evaluate_model_basic(sample_df):
    from audiovisually.evaluate import evaluate_model
    result = evaluate_model(MODEL_PATH, sample_df, text_column="Sentence", label_column="True Emotion")
    print('!!!!!!!!!!!!!!')
    print(result)
    print('!!!!!!!!!!!!!!')
    assert isinstance(result, dict)
    assert "accuracy" in result
    assert "f1" in result
    assert "classification_report" in result
    assert "confusion_matrix" in result
    assert "result_df" in result
    assert len(result["result_df"]) == 3

# (1) - Test 2: Custom label list
def test_evaluate_model_custom_labels(sample_df):
    from audiovisually.evaluate import evaluate_model
    label_list = ["happiness", "sadness", "anger", "disgust", "fear", "surprise", "neutral"]
    result = evaluate_model(MODEL_PATH, sample_df, label_list=label_list)
    assert set(result["classification_report"].keys()) >= set(label_list)

# (1) - Test 3: Custom text and label columns
def test_evaluate_model_custom_columns():
    from audiovisually.evaluate import evaluate_model
    df = pd.DataFrame({
        "text": ["I am happy"],
        "label": ["happiness"]
    })
    result = evaluate_model(MODEL_PATH, df, text_column="text", label_column="label")
    assert "Predicted" in result["result_df"].columns

# (1) - Test 4: Empty DataFrame input
def test_evaluate_model_empty_df():
    from audiovisually.evaluate import evaluate_model
    df = pd.DataFrame({"Sentence": [], "True Emotion": []})
    result = evaluate_model(MODEL_PATH, df)
    assert result["result_df"].empty
    assert result["accuracy"] == 0 or np.isnan(result["accuracy"])

# (1) - Test 5: Batch size logic
def test_evaluate_model_batch_size(sample_df):
    from audiovisually.evaluate import evaluate_model
    # Use batch_size=2 to test batching logic
    result = evaluate_model(MODEL_PATH, sample_df, batch_size=2)
    assert isinstance(result["result_df"], pd.DataFrame)
    assert len(result["result_df"]) == 3

# (1) - Test 6: Unknown label in true labels
def test_evaluate_model_unknown_label():
    from audiovisually.evaluate import evaluate_model
    df = pd.DataFrame({"Sentence": ["I am happy"], "True Emotion": ["not_in_label_list"]})
    result = evaluate_model(MODEL_PATH, df)
    # Should assign -1 for unknown label, which will be a mismatch
    assert "Predicted" in result["result_df"].columns

## ---------------  (3) compare_models ------------------------------

# (3) - Test 1: Compare two models on the same data
def test_compare_models(sample_df):
    from audiovisually.evaluate import compare_models
    result = compare_models(MODEL_PATH, MODEL_PATH, sample_df)
    assert "model_1" in result
    assert "model_2" in result
    assert "accuracy" in result["model_1"]
    assert "accuracy" in result["model_2"]