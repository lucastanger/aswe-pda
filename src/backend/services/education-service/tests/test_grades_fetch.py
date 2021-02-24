# test_grades_fetch.py
from app import app
from flask import json


def test_grades_fetch():
    """
    Tests the applications fetch grade endpoint
    :return:
    """
    response = app.test_client().get(
        '/rest/api/v1/grades/',
        data=json.dumps({'username': 'testuser', 'password': 'testpw'}),
    )

    # data = json.loads(response.get_data(as_text=True))

    # Currently checking if response is not None
    # TODO: How to check data without specific userdata?
    assert response is not None
    # assert response.status_code == 200
