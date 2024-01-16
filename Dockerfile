FROM python:3.10-slim

# Create a group and user to run our app
ENV APP_USER=balhom-api-user
RUN groupadd -r ${APP_USER} && useradd --no-log-init -r -g ${APP_USER} ${APP_USER}

# Install poetry
RUN pip install --upgrade pip && pip install poetry

# Copy dependency files
# To generate poetry files:
# cat requirements.txt | xargs -I % sh -c 'poetry add "%"'
COPY pyproject.toml /
COPY poetry.lock /
#COPY requirements.txt /

# Create requirements.txt file
RUN poetry export -f requirements.txt --output /requirements.txt

# Install dependencies
#RUN poetry install
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /requirements.txt

ENV PATH="/py/bin:$PATH"
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copy your application code to the container
# Note: create a .dockerignore file if any large files or directories should be excluded
RUN mkdir -p /app/src/
WORKDIR /app/
COPY manage.py /app/
COPY api_entrypoint.sh /app/
COPY celery_beat_entrypoint.sh /app/
COPY celery_worker_entrypoint.sh /app/
COPY celery_flower_entrypoint.sh /app/
ADD src /app/src/

# gunicorn will listen on this ports
EXPOSE 80
EXPOSE 443

# Add any custom, static environment variables needed by Django or your settings file here:
#ENV DJANGO_SETTINGS_MODULE=myapp.settings
ENV DJANGO_CONFIGURATION=Prod
ENV WSGI_APLICATION="src.core.wsgi:application"

# Change to a non-root user
USER ${APP_USER}:${APP_USER}

ENTRYPOINT ["/app/api_entrypoint.sh"]