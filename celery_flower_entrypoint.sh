#!/bin/sh

# Exit immediately if any of the following command exits 
# with a non-zero status
set -e

exec celery -A src.core flower -l ERROR "$@"
