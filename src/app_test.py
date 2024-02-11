import pytest
import requests


BASE_URL = 'http://localhost:5000'
tasks = []


def test_create_task():
    data = {
        "title": "Task 1",
        "description": "This is the first task"
    }
    response = requests.post(f'{BASE_URL}/tasks', json=data)
    assert response.status_code == 201
    response_json = response.json()
    assert "id" in response_json
    assert "message" in response_json
    assert "Task created successfully" in response_json['message']
    tasks.append(response_json['id'])


def test_get_tasks():
    response = requests.get(f'{BASE_URL}/tasks')
    assert response.status_code == 200
    response_json = response.json()
    assert "tasks" in response_json
    assert "total_tasks" in response_json


def test_get_task():
    if tasks:
        task_id = tasks[0]
        response = requests.get(f'{BASE_URL}/tasks/{task_id}')
        assert response.status_code == 200
        response_json = response.json()
        assert "id" in response_json
        assert "title" in response_json
        assert "description" in response_json
        assert "completed" in response_json
        assert task_id == response_json['id']


def test_update_task():
    if tasks:
        task_id = tasks[0]
        payload = {
            "title": "Task 1 updated",
            "description": "This is the first task updated",
            "completed": True
        }
        response = requests.put(f'{BASE_URL}/tasks/{task_id}', json=payload)
        assert response.status_code == 201
        response_json = response.json()
        assert "message" in response_json
        assert "Task updated successfully" in response_json['message']

        response = requests.get(f'{BASE_URL}/tasks/{task_id}')
        assert response.status_code == 200
        response_json = response.json()
        assert response_json["title"] == payload["title"]
        assert response_json["description"] == payload["description"]
        assert response_json["completed"] == payload["completed"]


def test_delete_task():
    if tasks:
        task_id = tasks[0]
        response = requests.delete(f'{BASE_URL}/tasks/{task_id}')
        assert response.status_code == 200
        response_json = response.json()
        assert "message" in response_json
        assert "Task deleted successfully" in response_json['message']

        response = requests.get(f'{BASE_URL}/tasks/{task_id}')
        assert response.status_code == 404
        response_json = response.json()
        assert "message" in response_json
        assert "Task not found" in response_json['message']
