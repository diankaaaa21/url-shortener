from unittest.mock import patch

import pytest


@pytest.fixture(autouse=True)
def mock_celery_tasks():
    with patch("shortener.tasks.log_url_creation.delay") as mocked:
        yield mocked
