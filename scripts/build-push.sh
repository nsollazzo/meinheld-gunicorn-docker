#!/usr/bin/env bash

set -e

use_tag="nsollazzo/meinheld-gunicorn:$NAME"
use_dated_tag="${use_tag}-$(date -I)"

docker build -t "$use_tag" "$BUILD_PATH"

docker tag "$use_tag" "$use_dated_tag"

docker push "$use_tag"
docker push "$use_dated_tag"
