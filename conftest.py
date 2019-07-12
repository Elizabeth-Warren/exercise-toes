import pytest
from flask import Response

# from moto import mock_s3  # This must come before including models
from toes_app import app as toes_app


@pytest.fixture
def app():
    toes_app.debug = True
    toes_app.response_class = Response
    return toes_app
