import os
import sys

import pytest
from fastapi.testclient import TestClient

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app  # Import the FastAPI instance from your app

client = TestClient(app)


@pytest.fixture(scope="module")
def setup():
    # Any setup code needed before tests run
    yield
    # Any teardown code needed after tests run

# Add other fixtures if needed, such as database fixtures
