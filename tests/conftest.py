from pytest import fixture

from mailer.mailer import create_app


@fixture
def client():
    app = create_app()
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client
