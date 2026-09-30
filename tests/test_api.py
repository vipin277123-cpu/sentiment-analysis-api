from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_check():
    response = client.get("/api/health")

    assert response.status_code == 200


def test_positive_sentiment():
    response = client.post(
        "/api/analyze",
        json={"text": "I absolutely love this product!"}
    )

    assert response.status_code == 200

    data = response.json()

    assert data["sentiment"] == "positive"
    assert 0 <= data["confidence"] <= 1


def test_negative_sentiment():
    response = client.post(
        "/api/analyze",
        json={"text": "This product is terrible."}
    )

    assert response.status_code == 200

    data = response.json()

    assert data["sentiment"] == "negative"
    assert 0 <= data["confidence"] <= 1


def test_neutral_sentiment():
    response = client.post(
        "/api/analyze",
        json={"text": "The meeting is scheduled for tomorrow."}
    )

    assert response.status_code == 200

    data = response.json()

    assert data["sentiment"] == "neutral"
    assert 0 <= data["confidence"] <= 1


def test_batch_analysis():
    response = client.post(
        "/api/analyze/batch",
        json={
            "texts": [
                "I love this!",
                "This is terrible.",
                "It is okay."
            ]
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data["results"]) == 3


def test_batch_limit():
    response = client.post(
        "/api/analyze/batch",
        json={
            "texts": [f"Test text {i}" for i in range(11)]
        }
    )

    assert response.status_code == 422


def test_empty_text():
    response = client.post(
        "/api/analyze",
        json={"text": ""}
    )

    assert response.status_code == 422