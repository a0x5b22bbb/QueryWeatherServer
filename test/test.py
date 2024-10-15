import pytest
from app import create_app
import time

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_get_weather_by_location_id(client):
    response = client.get('/api/weather?location_id=101010100')
    assert response.status_code == 200
    data = response.get_json()
    assert 'now' in data

def test_get_weather_no_params(client):
    response = client.get('/api/weather')
    assert response.status_code == 400
    data = response.get_json()
    assert data['error'] == "LocationID is required"

def test_get_weather_invalid_city(client):
    response = client.get('/api/weather?location_id=InvalidCity')
    assert response.status_code == 400
    data = response.get_json()
    assert "LocationID is invalid" in data['error']

def test_rate_limit(client):
    url = '/api/weather?location_id=101010100'

    # 发送 25 个请求(每分钟最大请求20次)
    responses = []
    start_time = time.time()
    for _ in range(10):
        response = client.get(url)
        responses.append(response)
        time.sleep(0.05)  # 每个请求间隔 0.05 秒，总共 1 秒内发完

    end_time = time.time()
    duration = end_time - start_time

    print(f"Total time taken: {duration} seconds")

    # 检查前几个请求是否成功
    for i in range(5):
        assert responses[i].status_code == 200

    # 检查后几个请求是否被限流
    for i in range(5, 10):
        assert responses[i].status_code == 429
