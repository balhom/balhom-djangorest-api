# Balhom DRF API

Welcome to the Balhom DRF API repository! 🚀

This repository is the beating heart of the Balhom application, providing a powerful backend built with Django and
Django Rest Framework. Our API seamlessly connects the frontend with a range of services.

## 🎯 Purpose

The Balhom API is designed to handle data storage, retrieval, and processing, serving as the backbone for our
application. It's the engine that powers Balhom's functionality and brings its features to life.

## 🛠 Technologies Used

- **Django**: A high-performance web framework for building robust applications.
- **Django Rest Framework (DRF)**: Turbocharge your Django API with DRF for flexibility and efficiency.
- **Keycloak**: Secure your API with Keycloak for robust authentication services.
- **PostgreSQL**: Our trusty database for storing and managing application data.
- **Redis**: The multitasker—acting as a message broker and cache for optimized performance.
- **Celery**: Elevate your app's responsiveness with Celery for asynchronous task execution.

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
    restart: unless-stopped
    entrypoint: /app/celery_worker_entrypoint.sh
    networks:
      - balhom-api-net

  balhom-celery-beat:
    image: fabbo/balhom-api-djangorest:latest
    container_name: balhom-celery-beat
    env_file:
      - ./api.env
    restart: unless-stopped
    entrypoint: /app/celery_beat_entrypoint.sh
    networks:
      - balhom-api-net

volumes:
  balhom-api-djangorest-logs:
  balhom-celery-beat-logs:
  balhom-celery-worker-logs:

networks:
  balhom-api-net:
```

🚨 Don't forget to fill ```api.env``` file with [ENV Variables](./api/README.md).

## Environment Variables

| NAME                        | DESCRIPTION                                                                 |
|-----------------------------|-----------------------------------------------------------------------------|
| ALLOWED_HOSTS               | List of strings representing the allowed host/domain names                  |
| CORS_HOSTS                  | CORS allowed hosts (url format)                                             |
| CSRF_HOSTS                  | CSRF allowed hosts (url format)                                             |
| USE_HTTPS                   | Enable HTTPS (true or false). Default: ***false***                          |
| LOG_FILE_PATH               | Use a file for logging, like "/var/log/app.log". If not set console is used |
| EMAIL_HOST                  | Email service host name                                                     |
| EMAIL_PORT                  | Email service port                                                          |
| EMAIL_HOST_USER             | Email service authentication user                                           |
| EMAIL_HOST_PASSWORD         | Email service authentication password                                       |
| CELERY_BROKER_URL           | Celery url                                                                  |
| EMAIL_CODE_THRESHOLD        | Time to wait for a new email verification code generation                   |
| EMAIL_CODE_VALID            | Email verification code validity duration                                   |
| UNVERIFIED_USER_DAYS        | Days for a periodic deletion of unverified users. Default: 2                |
| DATABASE_URL                | Databse endpoint                                                            |
| APP_VERSION                 | Minimum supported app version. Optional                                     |
| WEB_VERSION                 | Minimum supported web version. Optional                                     |
| DISABLE_ADMIN_PANEL         | Disable admin panel url `/general/admin`. Default: ***false***              |
| S3_URL                      | S3 api url                                                                  |
| S3_ACCESS_KEY               | S3 access key                                                               |
| S3_SECRET_KEY               | S3 secret key                                                               |
| S3_STATIC_BUCKET_NAME       | S3 static bucket name. Default: ***balhom-static-bucket***                  |
| S3_MEDIA_BUCKET_NAME        | S3 media bucket name. Default: ***balhom-media-bucket***                    |
| KEYCLOAK_URL                | Keycloak url                                                                |
| KEYCLOAK_CLIENT_ID          | Keycloak client id. Default: ***balhom-api***                               |
| KEYCLOAK_CLIENT_SECRET      | Keycloak client secret                                                      |
| KEYCLOAK_REALM              | Keycloak realm. Default: ***balhom-realm***                                 |
| CURRENCY_CONVERSION_API_URL | Currency conversion api url                                                 |
| CURRENCY_CONVERSION_API_KEY | Currency conversion api key                                                 |

## API Error Codes

| CODE | DEFINITION                                                 | ENDPOINT                                                                   |
|------|------------------------------------------------------------|----------------------------------------------------------------------------|
| 1    | User not found                                             | /api/v2/auth/send-verify-email , /api/v2/auth/password-reset               |
| 2    | Unverified email                                           | /api/v2/auth/password-reset , /api/v2/account [POST] , /api/v2/auth/access |
| 3    | Cannot send verification mail                              | /api/v2/auth/send-verify-email                                             |
| 4    | Cannot send reset password mail                            | /api/v2/auth/password-reset                                                |
| 5    | Password can only be reset 3 times a day                   | /api/v2/auth/password-reset                                                |
| 6    | Email already used                                         | /api/v2/account [POST]                                                     |
| 7    | Cannot create user                                         | /api/v2/account [POST]                                                     |
| 8    | Cannot update user                                         | /api/v2/account [PUT]                                                      |
| 9    | Cannot delete user                                         | /api/v2/account [DEL]                                                      |
| 10   | Currency type has already been changed in the las 24 hours | /api/v2/account [PUT]                                                      |
| 11   | Wrong credentials                                          | /api/v2/auth/access                                                        |
| 12   | Username already used                                      | /api/v2/account [POST]                                                     |
| 20   | Cannot make conversion                                     | /api/v2/account [PUT] , /api/v2/balance [POST] , /api/v2/balance [PUT]     |

## Keylcoak Setup steps

1. Go to admin console and login.

2. Create a Realm named `balhom-realm`.

3. Create a Client with `OpenID Connect` type and `balhom-api` id. Then in `Capability config`, `Client authentication`
   must be enabled and in `Authentication flow` section `Standard flow`, `Direct access grants`
   and `Service accounts roles` must be enabled.

4. Assign `manage-users` role (realm-management) in `Service accounts roles` tab to `balhom-api` client inside `Clients`
   section.

5. In `Login` tab inside `Realm settings` section enable `Email as username`, `Login with email` and `Verify email`.

6. Enable `Internatiolization` in `Localization` tab inside `Realm settings` section, and add "français" and "español"
   as `Supported locales`.

7. In `Email` tab inside `Realm settings` section setup email settings.

8. In `Sessions` tab inside `Realm settings` section change `SSO Session Idle` and `SSO Session Max` values to 5 Days.

## Support

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/FabboMaster)

If you have any questions, concerns, or need assistance, please don't hesitate to reach out. We are here to help you
make the most of our Currency Conversion API.

Happy coding!
