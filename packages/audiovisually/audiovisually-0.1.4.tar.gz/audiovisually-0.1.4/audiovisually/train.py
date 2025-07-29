# This file is part of the Audiovisually project.
# Here we can find some functions re-train our model(s).
# The goal here is to continiously train our model(s) with the option to try new parameters on new data.
# The current functions are:

# ...

# Feel free to add any functions you find useful.

import pandas as pd
import torch
from transformers import (
    AutoTokenizer, 
    AutoModelForSequenceClassification, 
    Trainer, 
    TrainingArguments,
    EarlyStoppingCallback
)
from sklearn.model_selection import train_test_split

LABEL_MAP = ['anger', 'sadness', 'disgust', 'fear', 'surprise', 'neutral', 'happiness']

def train_new_transformer_model(
    train_df,
    model_name="distilroberta-base",
    text_column="Sentence",
    label_column="Label",
    num_labels=7,
    output_dir="./new_model",
    epochs=10,
    batch_size=8,
    learning_rate=2e-5,
    eval_split=0.1,
    label_list=None,
    patience=3,
    validation_df=None,
    validation_text_column=None,
    validation_label_column=None,
    **kwargs
):
    """
    Train a transformer model from pretrained weights with a new classification head, using early stopping and saving the best model.

    Args:
        train_df (pd.DataFrame): DataFrame with text and labels.
        model_name (str): Hugging Face model name (default "distilroberta-base").
        text_column (str): Column with input text.
        label_column (str): Column with target labels.
        num_labels (int): Number of classes.
        output_dir (str): Directory to save the model.
        epochs (int): Number of epochs.
        batch_size (int): Batch size.
        learning_rate (float): Learning rate.
        eval_split (float): Fraction for validation split.
        label_list (list): Optional list of label names.
        patience (int): Early stopping patience.
        validation_df (pd.DataFrame): Optional DataFrame for validation data.
        validation_text_column (str): Optional column name for validation text.
        validation_label_column (str): Optional column name for validation labels.
        **kwargs: Additional TrainingArguments.

    Returns:
        Trainer: Hugging Face Trainer object (already trained).

    Example:
        >>> from audiovisually.train import train_new_transformer_model
        >>> df = pd.DataFrame({'Sentence': ['I am happy', 'I am sad'], 'Label': ['happiness', 'sadness']})
        >>> trainer = train_new_transformer_model(df, model_name="distilroberta-base", output_dir="./my_model")
    """
    # --- Load tokenizer and set up label mappings ---
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    label_list = LABEL_MAP if label_list is None else label_list
    label2id = {label: i for i, label in enumerate(label_list)}
    id2label = {i: label for i, label in enumerate(label_list)}

    # --- Load model with correct label mappings ---
    model = AutoModelForSequenceClassification.from_pretrained(
        model_name,
        num_labels=len(label_list),
        id2label=id2label,
        label2id=label2id
    )

    # --- Encode labels in train DataFrame ---
    train_df["label_id"] = train_df[label_column].map(label2id)

    # --- Split data or use provided validation set ---
    if validation_df is not None:
        train_data = train_df
        vtext_col = validation_text_column if validation_text_column else text_column
        vlabel_col = validation_label_column if validation_label_column else label_column
        eval_data = validation_df.copy()
        eval_data["label_id"] = eval_data[vlabel_col].map(label2id)
    else:
        if train_df[label_column].value_counts().min() < 2:
            train_data, eval_data = train_test_split(
                train_df, test_size=eval_split, random_state=42
            )
        else:
            train_data, eval_data = train_test_split(
                train_df, test_size=eval_split, stratify=train_df[label_column], random_state=42
            )
        vtext_col = text_column
        vlabel_col = label_column

    # --- Define custom Dataset class ---
    class EmotionDataset(torch.utils.data.Dataset):
        def __init__(self, df, text_col, label_col):
            self.encodings = tokenizer(
                df[text_col].tolist(), truncation=True, padding=True, max_length=128
            )
            self.labels = df["label_id"].tolist()

        def __getitem__(self, idx):
            item = {k: torch.tensor(v[idx]) for k, v in self.encodings.items()}
            item["labels"] = torch.tensor(self.labels[idx])
            return item

        def __len__(self):
            return len(self.labels)

    # --- Prepare datasets ---
    train_ds = EmotionDataset(train_data, text_column, label_column)
    eval_ds = EmotionDataset(eval_data, vtext_col, vlabel_col)

    # --- Set up training arguments ---
    training_args = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=epochs,
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=batch_size,
        eval_strategy="epoch",
        save_strategy="epoch",
        learning_rate=learning_rate,
        logging_dir=f"{output_dir}/logs",
        load_best_model_at_end=True,
        metric_for_best_model="eval_loss",
        greater_is_better=False,
        **kwargs
    )

    # --- Initialize Trainer and train ---
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_ds,
        eval_dataset=eval_ds,
        callbacks=[EarlyStoppingCallback(early_stopping_patience=patience)],
    )

    trainer.train()
    trainer.save_model(output_dir)
    tokenizer.save_pretrained(output_dir)
    return trainer

def retrain_existing_model(
    model_path,
    train_df,
    text_column="Sentence",
    label_column="Label",
    output_dir="./retrained_model",
    epochs=10,
    batch_size=8,
    learning_rate=2e-5,
    eval_split=0.1,
    label_list=None,
    patience=3,
    validation_df=None,
    validation_text_column=None,
    validation_label_column=None,
    **kwargs
):
    """
    Fine-tune an existing transformer model on new data, with early stopping and best model saving.

    Args:
        model_path (str): Path to the pre-trained model directory.
        train_df (pd.DataFrame): DataFrame with text and labels.
        text_column (str): Column with input text.
        label_column (str): Column with target labels.
        output_dir (str): Directory to save the retrained model.
        epochs (int): Number of epochs.
        batch_size (int): Batch size.
        learning_rate (float): Learning rate.
        eval_split (float): Fraction for validation split.
        label_list (list): Optional list of label names.
        patience (int): Early stopping patience.
        validation_df (pd.DataFrame): Optional DataFrame for validation data.
        validation_text_column (str): Optional column name for validation text.
        validation_label_column (str): Optional column name for validation labels.
        **kwargs: Additional TrainingArguments.

    Returns:
        Trainer: Hugging Face Trainer object (already trained).

    Example:
        >>> from audiovisually.train import retrain_existing_model
        >>> df = pd.DataFrame({'Sentence': ['I am happy', 'I am sad'], 'Label': ['happiness', 'sadness']})
        >>> trainer = retrain_existing_model("./my_model", df, output_dir="./my_model_retrained")
    """
    # --- Load tokenizer and set up label mappings ---
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    label_list = LABEL_MAP if label_list is None else label_list
    label2id = {label: i for i, label in enumerate(label_list)}
    id2label = {i: label for i, label in enumerate(label_list)}

    # --- Load model with correct label mappings ---
    model = AutoModelForSequenceClassification.from_pretrained(
        model_path,
        num_labels=len(label_list),
        id2label=id2label,
        label2id=label2id
    )

    # --- Encode labels in train DataFrame ---
    train_df["label_id"] = train_df[label_column].map(label2id)

    # --- Split data or use provided validation set ---
    if validation_df is not None:
        train_data = train_df
        vtext_col = validation_text_column if validation_text_column else text_column
        vlabel_col = validation_label_column if validation_label_column else label_column
        eval_data = validation_df.copy()
        eval_data["label_id"] = eval_data[vlabel_col].map(label2id)
    else:
        if train_df[label_column].value_counts().min() < 2:
            train_data, eval_data = train_test_split(
                train_df, test_size=eval_split, random_state=42
            )
        else:
            train_data, eval_data = train_test_split(
                train_df, test_size=eval_split, stratify=train_df[label_column], random_state=42
            )
        vtext_col = text_column
        vlabel_col = label_column

    # --- Define custom Dataset class ---
    class EmotionDataset(torch.utils.data.Dataset):
        def __init__(self, df, text_col, label_col):
            self.encodings = tokenizer(
                df[text_col].tolist(), truncation=True, padding=True, max_length=128
            )
            self.labels = df["label_id"].tolist()

        def __getitem__(self, idx):
            item = {k: torch.tensor(v[idx]) for k, v in self.encodings.items()}
            item["labels"] = torch.tensor(self.labels[idx])
            return item

        def __len__(self):
            return len(self.labels)

    # --- Prepare datasets ---
    train_ds = EmotionDataset(train_data, text_column, label_column)
    eval_ds = EmotionDataset(eval_data, vtext_col, vlabel_col)

    # --- Set up training arguments ---
    training_args = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=epochs,
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=batch_size,
        eval_strategy="epoch",
        save_strategy="epoch",
        learning_rate=learning_rate,
        logging_dir=f"{output_dir}/logs",
        load_best_model_at_end=True,
        metric_for_best_model="eval_loss",
        greater_is_better=False,
        **kwargs
    )

    # --- Initialize Trainer and train ---
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_ds,
        eval_dataset=eval_ds,
        callbacks=[EarlyStoppingCallback(early_stopping_patience=patience)],
    )

    trainer.train()
    trainer.save_model(output_dir)
    tokenizer.save_pretrained(output_dir)
    return trainer

def get_model_info(model_path_or_name):
    """
    Print and return key information about a transformer model and its tokenizer.

    Args:
        model_path_or_name (str): Hugging Face model name or local path.

    Returns:
        dict: Model and tokenizer information.

    Example:
        >>> from audiovisually.train import get_model_info
        >>> info = get_model_info("distilroberta-base")
    """
    from transformers import AutoConfig

    config = AutoConfig.from_pretrained(model_path_or_name)
    tokenizer = AutoTokenizer.from_pretrained(model_path_or_name)

    info = {
        "model_name": config.name_or_path,
        "architecture": config.architectures,
        "num_labels": getattr(config, "num_labels", None),
        "id2label": getattr(config, "id2label", None),
        "label2id": getattr(config, "label2id", None),
        "vocab_size": getattr(tokenizer, "vocab_size", None),
        "max_length": getattr(tokenizer, "model_max_length", None),
    }

    print("Model Information:")
    for k, v in info.items():
        print(f"  {k}: {v}")

    return info