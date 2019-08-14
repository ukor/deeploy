import falcon
from falcon import testing
import pytest
from deeploy.app import API

@pytest.fixture
def client():
    return testing.TestClient(API)

def test_send_post(client):
    '''
        Make request without service headers
        Expect response to be Bad Request (400)
    '''
    response = client.simulate_post('/')

    assert response.status == falcon.HTTP_400

def test_github(client):
    ''' Make request with github payload '''
    headers = {
        'X-GITHUB-EVENT': 'merge',
        'X-GITHUB-DELIVERY': 'some_string',
        'X-HUB-SIGNATURE': 'another_string',
        'Content-type': 'application/json'
    }
    response = client.simulate_post('/', headers=headers)

    assert response.status == falcon.HTTP_OK
    assert response.text == 'github'

def test_bitbucket(client):
    ''' Make request with bitbucket payload '''
    headers = {
        'X-EVENT-KEY': 'some_string',
        'X-HOOK-UUID': 'some_UUID'
    }
    response = client.simulate_post('/', headers=headers)

    assert response.status == falcon.HTTP_OK
    assert response.text == 'bitbucket'
