# Auth Endpints

| Path                           | Method | Res Status | Res Body        | Res Cookie    | Req Cookie    | Req Body            | Comments                         |
| ------------------------------ | ------ | ---------- | --------------- | ------------- | ------------- | ------------------- | -------------------------------- |
| /api/v2/auth/access            | POST   | 200        | tokens-response | refresh_token | -             | credentials-request |                                  |
| /api/v2/auth/refresh           | POST   | 200        | tokens-response | refresh_token | refresh_token | -                   |                                  |
| /api/v2/auth/logout            | POST   | 204        | -               | -             | refresh_token | -                   |                                  |
| /api/v2/auth/send-verify-email | POST   | 204        | -               | -             | -             | email-request       | Send email verification mail     |
| /api/v2/auth/password-reset    | POST   | 204        | -               | -             | -             | email-request       | Send mail to reset user password |
