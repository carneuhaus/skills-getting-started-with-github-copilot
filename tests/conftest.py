from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src import app as app_module


_INITIAL_ACTIVITIES = deepcopy(app_module.activities)


@pytest.fixture(autouse=True)
def reset_activities_state():
    """Reset global in-memory activity state before each test."""
    app_module.activities = deepcopy(_INITIAL_ACTIVITIES)
    yield


@pytest.fixture
def client():
    return TestClient(app_module.app)
