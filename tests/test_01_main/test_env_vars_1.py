import time

import docker
import pytest
import requests

from ..utils import CONTAINER_NAME, get_config, stop_previous_container

client = docker.from_env()


@pytest.mark.parametrize(
    "image,response_text",
    [
        (
            "tiangolo/meinheld-gunicorn:python3.6",
            "Hello World from a default Python 3.6 app in a Docker container, with Meinheld and Gunicorn (default)",
        ),
        (
            "tiangolo/meinheld-gunicorn:python3.6-alpine3.8",
            "Hello World from a default Python 3.6 app in a Docker container, with Meinheld and Gunicorn on Alpine (default)",
        ),
        (
            "tiangolo/meinheld-gunicorn:python3.7",
            "Hello World from a default Python 3.7 app in a Docker container, with Meinheld and Gunicorn (default)",
        ),
        (
            "tiangolo/meinheld-gunicorn:python3.7-alpine3.8",
            "Hello World from a default Python 3.7 app in a Docker container, with Meinheld and Gunicorn on Alpine (default)",
        ),
        (
            "tiangolo/meinheld-gunicorn:latest",
            "Hello World from a default Python 3.7 app in a Docker container, with Meinheld and Gunicorn (default)",
        ),
    ],
)
def test_env_vars_1(image, response_text):
    stop_previous_container(client)
    container = client.containers.run(
        image,
        name=CONTAINER_NAME,
        environment={"WORKERS_PER_CORE": 1, "PORT": "8000", "LOG_LEVEL": "warning"},
        ports={"8000": "8000"},
        detach=True,
    )
    config_data = get_config(container)
    assert config_data["workers_per_core"] == 1
    assert config_data["host"] == "0.0.0.0"
    assert config_data["port"] == "8000"
    assert config_data["loglevel"] == "warning"
    assert config_data["bind"] == "0.0.0.0:8000"
    time.sleep(1)
    response = requests.get("http://127.0.0.1:8000")
    assert response.text == response_text
    container.stop()
    container.remove()
