from app import app

def test_home():
    response = app.test_client().get('/')
    assert response.status_code == 200, "Home test Failure"

def test_org():
    response = app.test_client().get('/')
    assert response.status_code == 200, "Org test Failure"

def test_repo():
    response = app.test_client().get('/')
    assert response.status_code == 200, "Repo test Failure"