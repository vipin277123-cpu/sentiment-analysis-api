# Sentiment Analysis API

A REST API for analyzing the sentiment of English text using a pre-trained Hugging Face Transformer model.

The API classifies text into three sentiment categories:

* **Positive**
* **Negative**
* **Neutral**

It also returns a confidence score between `0` and `1`.

## Features

* Sentiment classification using a pre-trained Transformer model
* Supports English text
* Confidence score for predictions
* Single-text sentiment analysis
* Batch sentiment analysis
* Batch requests limited to 10 texts
* Text validation from 1 to 500 words
* Health check endpoint
* API documentation through Swagger UI
* Automated API tests using Pytest
* Model evaluation on the TweetEval sentiment test dataset

## Tech Stack

* **Python 3.11**
* **FastAPI**
* **Uvicorn**
* **Hugging Face Transformers**
* **PyTorch**
* **Pydantic**
* **Pytest**

## Model

The project uses the pre-trained Hugging Face model:

`cardiffnlp/twitter-roberta-base-sentiment-latest`

The model is based on RoBERTa and is fine-tuned for sentiment classification.

The model predicts three classes:

```text
0 → Negative
1 → Neutral
2 → Positive
```

The API converts the model prediction into a human-readable sentiment label and returns the corresponding confidence score.

## Project Structure

```text
sentiment-analysis-api/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── model.py
│   └── schemas.py
│
├── evaluation/
│   └── evaluate_model.py
│
├── tests/
│   └── test_api.py
│
├── .gitignore
├── requirements.txt
└── README.md
```

### File Description

| File                           | Description                                                   |
| ------------------------------ | ------------------------------------------------------------- |
| `app/main.py`                  | FastAPI application and API endpoints                         |
| `app/model.py`                 | Loads the Transformer model and performs sentiment prediction |
| `app/schemas.py`               | Pydantic request/response models and validation               |
| `evaluation/evaluate_model.py` | Evaluates model performance                                   |
| `tests/test_api.py`            | Automated API tests                                           |
| `requirements.txt`             | Python dependencies                                           |
| `.gitignore`                   | Files excluded from Git                                       |

## API Endpoints

### 1. Health Check

**GET `/api/health`**

Checks whether the API is running.

Example:

```http
GET /api/health
```

Example response:

```json
{
  "status": "healthy"
}
```

---

### 2. Analyze Sentiment

**POST `/api/analyze`**

Analyzes the sentiment of a single text.

#### Request

```json
{
  "text": "I really love this product!"
}
```

#### Response

```json
{
  "text": "I really love this product!",
  "sentiment": "positive",
  "confidence": 0.9844
}
```

The confidence value represents the model's confidence in its predicted sentiment.

---

### 3. Batch Sentiment Analysis

**POST `/api/analyze/batch`**

Analyzes multiple texts in a single request.

A maximum of **10 texts** can be submitted in one batch request.

#### Request

```json
{
  "texts": [
    "I absolutely love this product!",
    "This product is terrible and useless.",
    "The product is okay, nothing special."
  ]
}
```

#### Response

```json
{
  "results": [
    {
      "text": "I absolutely love this product!",
      "sentiment": "positive",
      "confidence": 0.9844
    },
    {
      "text": "This product is terrible and useless.",
      "sentiment": "negative",
      "confidence": 0.9478
    },
    {
      "text": "The product is okay, nothing special.",
      "sentiment": "neutral",
      "confidence": 0.5567
    }
  ]
}
```

## Input Validation

The API validates incoming text before performing sentiment analysis.

### Single text

* Minimum: **1 word**
* Maximum: **500 words**

Example of invalid input:

```json
{
  "text": ""
}
```

This returns a validation error.

### Batch input

A batch request can contain a maximum of **10 texts**.

For example, sending 11 texts results in:

```text
422 Unprocessable Entity
```

with a validation message indicating that the list can contain at most 10 items.

## Swagger API Documentation

FastAPI automatically provides interactive API documentation.

After starting the application, open:

```text
http://127.0.0.1:8000/docs
```

The Swagger interface can be used to test all API endpoints directly from the browser.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/vipin277123-cpu/sentiment-analysis-api.git
cd sentiment-analysis-api
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

## Running the API

Start the FastAPI application using Uvicorn:

```powershell
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

## Testing

The project includes automated API tests using Pytest.

Run:

```powershell
pytest
```

Current test result:

```text
7 passed
```

The tests cover:

* Health check
* Positive sentiment
* Negative sentiment
* Neutral sentiment
* Batch sentiment analysis
* Batch size validation
* Empty text validation

## Model Evaluation

The model was evaluated using the **TweetEval sentiment test dataset**.

### Dataset

```text
Test samples: 12,284
```

### Performance

```text
Accuracy: 72.18%
```

### Classification Report

| Class        | Precision | Recall | F1-score |   Support |
| ------------ | --------: | -----: | -------: | --------: |
| Negative     |      0.69 |   0.81 |     0.74 |      3972 |
| Neutral      |      0.76 |   0.66 |     0.70 |      5937 |
| Positive     |      0.71 |   0.74 |     0.73 |      2375 |
| **Accuracy** |           |        | **0.72** | **12284** |
| Macro Avg    |      0.72 |   0.73 |     0.72 |     12284 |
| Weighted Avg |      0.73 |   0.72 |     0.72 |     12284 |

The evaluation script is located at:

```text
evaluation/evaluate_model.py
```

Run it with:

```powershell
python evaluation/evaluate_model.py
```

## Error Handling

The API uses FastAPI and Pydantic validation to handle invalid requests.

Examples include:

* Empty text
* Text exceeding 500 words
* Batch requests containing more than 10 texts
* Invalid request structures

Invalid requests return appropriate HTTP `422 Unprocessable Entity` responses.

## Example Workflow

```text
Client
  │
  │ POST /api/analyze
  │
  ▼
FastAPI
  │
  ▼
Request Validation
  │
  ▼
RoBERTa Sentiment Model
  │
  ▼
Sentiment Prediction
  │
  ├── Positive
  ├── Negative
  └── Neutral
  │
  ▼
Confidence Score
  │
  ▼
JSON Response
```

## Future Improvements

Possible improvements include:

* Add Docker support
* Deploy the API to Render or Railway
* Add CI/CD using GitHub Actions
* Add API authentication
* Add request logging
* Add rate limiting
* Add more comprehensive performance monitoring
* Improve sentiment performance through model fine-tuning

## License

This project currently does not specify a license.

## Author

**Vipin Sharma**

GitHub:
https://github.com/vipin277123-cpu
