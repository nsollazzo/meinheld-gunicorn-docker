#!/usr/bin/env bash
set -e

use_tag="nsollazzo/meinheld-gunicorn:$NAME"

docker build -t "$use_tag" "$BUILD_PATH"
pytest tests
