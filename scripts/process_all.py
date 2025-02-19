import os
import subprocess
import sys

environments = [
    {
        "NAME": "latest",
        "BUILD_PATH": "python8-slim-buster",
        "TEST_STR1": "Hello World from a default Python 3.8 app in a Docker container, with Meinheld and Gunicorn (default)",
        "TEST_STR2": "Test app. From Meinheld with Gunicorn. Using Python 3.8",
    },
    {
        "NAME": "python3.8-slim-buster",
        "BUILD_PATH": "python3.8-slim-buster",
        "TEST_STR1": "Hello World from a default Python 3.8 app in a Docker container, with Meinheld and Gunicorn (default)",
        "TEST_STR2": "Test app. From Meinheld with Gunicorn. Using Python 3.8",
    },
    {
        "NAME": "python3.7-slim-buster",
        "BUILD_PATH": "python3.7-slim-buster",
        "TEST_STR1": "Hello World from a default Python 3.7 app in a Docker container, with Meinheld and Gunicorn (default)",
        "TEST_STR2": "Test app. From Meinheld with Gunicorn. Using Python 3.7",
    },
    {
        "NAME": "python3.6-slim-buster",
        "BUILD_PATH": "python3.6-slim-buster",
        "TEST_STR1": "Hello World from a default Python 3.6 app in a Docker container, with Meinheld and Gunicorn (default)",
        "TEST_STR2": "Test app. From Meinheld with Gunicorn. Using Python 3.6",
    },
]

start_with = os.environ.get("START_WITH")
build_push = os.environ.get("BUILD_PUSH")


def process_tag(*, env: dict):
    use_env = {**os.environ, **env}
    script = "scripts/test.sh"
    if build_push:
        script = "scripts/build-push.sh"
    return_code = subprocess.call(["bash", script], env=use_env)
    if return_code != 0:
        sys.exit(return_code)


def print_version_envs():
    env_lines = []
    for env in environments:
        env_vars = []
        for key, value in env.items():
            env_vars.append(f"{key}='{value}'")
        env_lines.append(" ".join(env_vars))
    for line in env_lines:
        print(line)


def main():
    start_at = 0
    if start_with:
        start_at = [
            i for i, env in enumerate((environments)) if env["NAME"] == start_with
        ][0]
    for i, env in enumerate(environments[start_at:]):
        print(f"Processing tag: {env['NAME']}")
        process_tag(env=env)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        print_version_envs()
    else:
        main()
