# Balhom DRF API

## Environment Variables

| NAME                        | DESCRIPTION                                                                 |
| --------------------------- | --------------------------------------------------------------------------- |
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
