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

## Keylcoak Setup steps

1. Go to admin console and login.

2. Create a Realm named `balhom-realm`.

3. Create a Client with `OpenID Connect` type and `balhom-api` id. Then in `Capability config`, `Client authentication` must be enabled and in `Authentication flow` section `Standard flow`, `Direct access grants` and `Service accounts roles` must be enabled.

4. Assign `manage-users` role (realm-management) in `Service accounts roles` tab to `balhom-api` client inside `Clients` section. 

5. In `Login` tab inside `Realm settings` section enable `Email as username`, `Login with email` and `Verify email`.

6. Enable `Internatiolization` in `Localization` tab inside `Realm settings` section, and add "français" and "español" as `Supported locales`.

7. In `Email` tab inside `Realm settings` section setup email settings.

8.  In `Sessions` tab inside `Realm settings` section change `SSO Session Idle` and `SSO Session Max` values to 5 Days.
