from datasets import load_dataset
from transformers import pipeline
from sklearn.metrics import accuracy_score, classification_report


MODEL_NAME = "cardiffnlp/twitter-roberta-base-sentiment-latest"

LABEL_MAP = {
    "negative": 0,
    "neutral": 1,
    "positive": 2
}


print("Loading model...")

classifier = pipeline(
    "sentiment-analysis",
    model=MODEL_NAME,
    tokenizer=MODEL_NAME
)


print("Loading TweetEval sentiment test dataset...")

dataset = load_dataset(
    "cardiffnlp/tweet_eval",
    "sentiment",
    split="test"
)


texts = dataset["text"]
true_labels = dataset["label"]

print(f"Test samples: {len(texts)}")
print("Running predictions...")


predictions = []

for text in texts:
    result = classifier(text, truncation=True)[0]

    predicted_label = result["label"].lower()

    predictions.append(LABEL_MAP[predicted_label])


accuracy = accuracy_score(true_labels, predictions)

print("\nModel Performance")
print("-----------------")
print(f"Accuracy: {accuracy:.4f}")
print(f"Accuracy: {accuracy * 100:.2f}%")

print("\nClassification Report")
print("---------------------")

print(
    classification_report(
        true_labels,
        predictions,
        target_names=[
            "negative",
            "neutral",
            "positive"
        ]
    )
)