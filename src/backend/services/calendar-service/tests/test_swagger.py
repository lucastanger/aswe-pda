import pytest

from app import app


@pytest.fixture()
def test_client():
    return app.test_client()


class TestSwagger:
    def test_swagger_yml(self, test_client):
        response = test_client.get('http://localhost:5560/rest/api/v1/swagger/swagger.yml')

        assert response.status_code == 200
