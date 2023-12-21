#!/bin/sh

# Exit immediately if any of the following command exits 
# with a non-zero status
set -e

export DJANGO_CONFIGURATION=Prod

exec celery -A core beat -l ERROR \
    --scheduler django_celery_beat.schedulers:DatabaseScheduler "$@"
