import pytest

@pytest.mark.django_db
def test_get_context_data(client):
    response = client.get('/')
    assert 'posts' in response.context
