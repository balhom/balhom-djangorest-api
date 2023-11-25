# Balhom DRF API

Welcome to the Balhom DRF API repository! 🚀

This repository is the beating heart of the Balhom application, providing a powerful backend built with Django and Django Rest Framework. Our API seamlessly connects the frontend with a range of services.

## 🎯 Purpose

The Balhom API is designed to handle data storage, retrieval, and processing, serving as the backbone for our application. It's the engine that powers Balhom's functionality and brings its features to life.

## 🛠 Technologies Used

- **Django**: A high-performance web framework for building robust applications.
- **Django Rest Framework (DRF)**: Turbocharge your Django API with DRF for flexibility and efficiency.
- **Keycloak**: Secure your API with Keycloak for robust authentication services.
- **PostgreSQL**: Our trusty database for storing and managing application data.
- **Redis**: The multitasker—acting as a message broker and cache for optimized performance.
- **Celery**: Elevate your app's responsiveness with Celery for asynchronous task execution.

## 📚 Documentation

Dig into the nitty-gritty details of setting up the API, configuring environment variables, and more in our [API Documentation](./api/README.md). It's your go-to resource for mastering the Balhom API.

## 🐳 Example Docker Compose

Simplify deployment and ensure consistency across environments with our sample Docker Compose configuration.

```yaml
version: '3'

services:

  balhom-api-djangorest:
    image: fabbo/balhom-api-djangorest:latest
    container_name: balhom-api-djangorest
    env_file:
      - ./api.env
    volumes:
      - ./logs/api:/var/log/api
    ports:
      - "8000:80"
    depends_on:
      - balhom-celery-worker
      - balhom-celery-beat
    restart: unless-stopped
    networks:
      - balhom-api-net

  balhom-celery-worker:
    image: fabbo/balhom-api-djangorest:latest
    container_name: balhom-celery-worker
    env_file:
      - ./api.env
    volumes:
      - ./logs/celery_worker:/var/log/api
    restart: unless-stopped
    entrypoint: /app/celery_worker_entrypoint.sh
    networks:
      - balhom-api-net

  balhom-celery-beat:
    image: fabbo/balhom-api-djangorest:latest
    container_name: balhom-celery-beat
    env_file:
      - ./api.env
    volumes:
      - ./logs/celery_beat:/var/log/api
    restart: unless-stopped
    entrypoint: /app/celery_beat_entrypoint.sh
    networks:
      - balhom-api-net

networks:
  balhom-api-net:

```

🚨 Don't forget to fill ```api.env``` file with [ENV Variables](./api/README.md).

## Support

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/FabboMaster)

If you have any questions, concerns, or need assistance, please don't hesitate to reach out. We are here to help you make the most of our Currency Conversion API.

Happy coding!
