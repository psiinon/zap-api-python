"""
Tests related to the main Zap Client class
"""

TEST_PROXIES = {
    'http': 'http://127.0.0.1:8080',
    'https': 'http://127.0.0.1:8080',
}


def assert_api_key(response, apikey='testapikey'):
    """Some requests should contain valid ZAP api key."""
    assert response._request.headers['X-ZAP-API-Key'] == apikey
    assert 'apikey=%s' % apikey in response.query


def test_urlopen(zap, client_mock):
    """Request method should return a python object from parsed output"""
    api_response ='{"testkey": "testvalue"}'
    client_mock.get('http://localhost:8080', text=api_response)

    assert zap.urlopen('http://localhost:8080', {'querykey': 'queryvalue'}) == api_response

    response = client_mock.request_history[0]

    assert 'X-ZAP-API-Key' not in response._request.headers
    assert 'testapikey' not in response.query
    assert response.proxies == TEST_PROXIES


def test_request_response(zap, client_mock):
    """Request method should return a python object from parsed output"""
    client_mock.get('http://zap/test', text='{"testkey": "testvalue"}')

    assert zap._request('http://zap/test', {'querykey': 'queryvalue'}) == {'testkey': 'testvalue'}

    response = client_mock.request_history[0]

    assert_api_key(response)
    assert response.proxies == TEST_PROXIES


def test_request_other(zap, client_mock):
    """_request_other should simply return a retrieved content."""
    api_response = '{"testkey": "testvalue"}'
    client_mock.get('http://zap/test', text=api_response)

    assert zap._request_other('http://zap/test', {'querykey': 'queryvalue'}) == api_response

    response = client_mock.request_history[0]

    assert_api_key(response)
    assert response.proxies == TEST_PROXIES
