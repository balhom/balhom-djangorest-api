# API Contracts

This directory serves as a reference guide for developers working on the frontend and backend of balhom application. It ensures that both teams are aligned in terms of API integration, reducing miscommunication and enhancing productivity.


## API

### Endpoints

* [Verion Endpoints](./endpoints/version-endpoints.md)
* [Auth Endpoints](./endpoints/auth-endpoints.md)
* [Account Endpoints](./endpoints/account-endpoints.md)
* [Balance Endpoints](./endpoints/balance-endpoints.md)
* [Statistics Endpoints](./endpoints/statistics-endpoints.md)

### Requests

* [Account Requests](./requests/account-requests.md)
* [Balance Requests](./requests/balance-requests.md)

### Responses

* [Version Response](./responses/version-response.md)
* [Account Response](./responses/account-response.md)
* [Balance Response](./responses/balance-responses.md)
* [Statistics Response](./responses/statistics-responses.md)


## Error Codes

| CODE | DEFINITION                                                 | ENDPOINT                                                     |
| ---- | ---------------------------------------------------------- | ------------------------------------------------------------ |
| 1    | User not found                                             | /api/v2/auth/send-verify-email , /api/v2/user/password-reset |
| 2    | Unverified email                                           | /api/v2/auth/password-reset, /api/v2/auth/access             |
| 3    | Cannot send verification mail                              | /api/v2/auth/send-verify-email                               |
| 4    | Cannot send reset password mail                            | /api/v2/auth/password-reset                                  |
| 5    | Password can only be reset 3 times a day                   | /api/v2/auth/password-reset                                  |
| 6    | Email already used                                         | /api/v2/account [POST]                                       |
| 7    | Cannot create user                                         | /api/v2/account [POST]                                       |
| 8    | Cannot update user                                         | /api/v2/account [PUT/PATCH]                                  |
| 9    | Cannot delete user                                         | /api/v2/account [DEL]                                        |
| 10   | Currency type has already been changed in the las 24 hours | /api/v2/account [PUT/PATCH]                                  |
| 11   | Wrong credentials                                          | /api/v2/auth/access                                          |
| 12   | Username already used                                      | /api/v2/account [POST], /api/v2/account [PUT/PATCH]          |
