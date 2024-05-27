import pytest
from app.app import app as flask_app
from app.models import db


@pytest.fixture(scope="session")
def app():
    flask_app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": 'mysql+pymysql://root@db/fakeredditdb',
    })
    return flask_app


@pytest.fixture(scope="session")
def db(app):
    with app.app_context():
        db.create_all()
    yield db
    db.session.remove()
    db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()
