from fastapi.testclient import TestClient
import json
from unittest.mock import patch, AsyncMock

from main import app


def test_index_route_returns_html():
    with TestClient(app) as client:
        response = client.get('/')
        assert response.status_code == 200
        assert response.headers['content-type'] == 'text/html; charset=utf-8'
        assert '<!DOCTYPE html>' in response.text or '<html' in response.text


def test_chat_app_ts_route():
    with TestClient(app) as client:
        response = client.get('/chat_app.ts')
        assert response.status_code == 200
        assert response.headers['content-type'] == 'text/plain; charset=utf-8'
        assert response.text is not None


def test_get_chat_history_empty():
    with TestClient(app) as client:
        response = client.get('/chat/')
        assert response.status_code == 200
        assert response.headers['content-type'] == 'text/plain; charset=utf-8'
        assert response.text == ''


def test_post_chat_missing_prompt():
    with TestClient(app) as client:
        response = client.post('/chat/')
        assert response.status_code == 422


def test_invalid_route():
    with TestClient(app) as client:
        response = client.get('/nonexistent')
        assert response.status_code == 404
