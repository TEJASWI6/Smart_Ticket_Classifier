import joblib
import numpy as np
import pandas as pd
import torch
from datasets import Dataset
from sklearn.metrics import accuracy_score
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    Trainer,
    TrainingArguments,
    pipeline,
)

# Load cleaned CSV
df = pd.read_csv("data/train.csv")

# Encode categories to numbers
labels = df['category'].unique()
label2id = {label: i for i, label in enumerate(labels)}
id2label = {i: label for label, i in label2id.items()}
df['label'] = df['category'].map(label2id)

# Convert to Hugging Face dataset
dataset = Dataset.from_pandas(df[['text', 'label']])
dataset = dataset.train_test_split(test_size=0.2)

# Load tokenizer & model
model_name = "distilbert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)

def tokenize(batch):
    return tokenizer(batch['text'], padding=True, truncation=True)

tokenized_ds = dataset.map(tokenize, batched=True)

# Load model
model = AutoModelForSequenceClassification.from_pretrained(
    model_name,
    num_labels=len(labels),
    id2label=id2label,
    label2id=label2id
)

# Training arguments
training_args = TrainingArguments(
    output_dir="models/bert_ticket_model",
    evaluation_strategy="epoch",
    save_strategy="epoch",
    logging_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    num_train_epochs=5,
    weight_decay=0.01,
    load_best_model_at_end=True
)

# Metric
def compute_metrics(pred):
    labels = pred.label_ids
    preds = np.argmax(pred.predictions, axis=1)
    acc = accuracy_score(labels, preds)
    return {"accuracy": acc}

# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_ds['train'],
    eval_dataset=tokenized_ds['test'],
    compute_metrics=compute_metrics,
    tokenizer=tokenizer
)

# Train the model 🎉
trainer.train()

# Save final model
trainer.save_model("models/bert_ticket_model")
tokenizer.save_pretrained("models/bert_ticket_model")

# Save label encoder
joblib.dump(label2id, "models/label_encoder.pkl")

print("\n✅ Model training complete and saved in /models!")
