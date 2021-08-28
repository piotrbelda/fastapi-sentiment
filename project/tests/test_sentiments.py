import json
import pytest


def test_create_sentiment(test_app_with_db):
    response = test_app_with_db.post(
        "/sentiments/", data=json.dumps({"content": "foo", "description": "bar"})
    )
    assert response.status_code == 201
    assert response.json()["content"] == "foo"
    assert response.json()["description"] == "bar"


def test_create_sentiment_invalid_json(test_app):
    response = test_app.post("/sentiments/", data=json.dumps({}))
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "content"],
                "msg": "field required",
                "type": "value_error.missing",
            },
            {
                "loc": ["body", "description"],
                "msg": "field required",
                "type": "value_error.missing",
            },
        ]
    }


def test_read_sentiment(test_app_with_db):
    response = test_app_with_db.post(
        "/sentiments/", data=json.dumps({"content": "foo", "description": "bar"})
    )
    sentiment_id = response.json()["id"]

    response = test_app_with_db.get(f"/sentiments/{sentiment_id}/")
    assert response.status_code == 200

    response_dict = response.json()
    assert response_dict["id"] == sentiment_id
    assert response_dict["content"] == "foo"
    assert response_dict["description"] == "bar"
    assert response_dict["sentiment"]
    assert response_dict["created_at"]


def test_read_sentiment_incorrect_id(test_app_with_db):
    response = test_app_with_db.get("/sentiments/999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Sentiment not found"


def test_read_all_sentiments(test_app_with_db):
    response = test_app_with_db.post(
        "/sentiments/", data=json.dumps({"content": "foo", "description": "bar"})
    )
    sentiment_id = response.json()["id"]

    response = test_app_with_db.get("/sentiments/")
    assert response.status_code == 200

    response_list = response.json()
    assert len(list(filter(lambda d: d["id"] == sentiment_id, response_list))) == 1

def test_remove_sentiment(test_app_with_db):
    response = test_app_with_db.post("/sentiments/", data = json.dumps({"content": "foo", "description":"bar"}))
    summary_id = response.json()["id"]
    response = test_app_with_db.delete(f"/sentiments/{summary_id}/")
    
    assert response.status_code == 200
    assert response.json() == {"id": summary_id, "content": "foo", "description": "bar"}
    
def test_remove_sentiment_incorrect_id(test_app_with_db):
    response = test_app_with_db.delete("/sentiments/999/")
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Sentiment not found"
    
def test_update_sentiment(test_app_with_db):
    response = test_app_with_db.post(
        "/sentiments/", data=json.dumps({"content": "foo", "description": "bar"})
    )
    sentiment_id = response.json()["id"]

    response = test_app_with_db.put(
        f"/sentiments/{sentiment_id}/",
        data=json.dumps({"content": "foo", "description": "bar", "sentiment": False})
    )
    assert response.status_code == 200

    response_dict = response.json()
    assert response_dict["id"] == sentiment_id
    assert response_dict["content"] == "foo"
    assert response_dict["description"] == "bar"
    assert response_dict["sentiment"] == False
    assert response_dict["created_at"]
    
def test_update_sentiment_incorrect_id(test_app_with_db):
    response = test_app_with_db.put(
        "/sentiments/999/",
        data=json.dumps({"content": "foo", "description": "bar", "sentiment": False})
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Sentiment not found"
    
def test_update_sentiment_invalid_json(test_app_with_db):
    response = test_app_with_db.post(
        "/sentiments/", data=json.dumps({"content": "foo", "description": "bar"})
    )
    sentiment_id = response.json()["id"]

    response = test_app_with_db.put(
        f"/sentiments/{sentiment_id}/",
        data=json.dumps({})
    )
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "content"],
                "msg": "field required",
                "type": "value_error.missing",
            },
            {
                "loc": ["body", "description"],
                "msg": "field required",
                "type": "value_error.missing",
            },
            {
                "loc": ["body", "sentiment"],
                "msg": "field required",
                "type": "value_error.missing",
            }
        ]
    }

def test_update_sentiment_invalid_keys(test_app_with_db):
    response = test_app_with_db.post(
        "/sentiments/", data=json.dumps({"content": "foo", "description": "bar"})
    )
    sentiment_id = response.json()["id"]

    response = test_app_with_db.put(
        f"/sentiments/{sentiment_id}/",
        data=json.dumps({"content": "foo", "description": "bar"})
    )
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "sentiment"],
                "msg": "field required",
                "type": "value_error.missing",
            }
        ]
    }