# User Endpints

| Path                           | Method | Res Status | Res Body         | Res Cookie | Req Param | Req Body                 | Comments                          |
| ------------------------------ | ------ | ---------- | ---------------- | ---------- | --------- | ------------------------ | --------------------------------- |
| /api/v2/account                | POST   | 201        | account-response | -          | -         | account-creation-request |                                   |
| /api/v2/account                | GET    | 200        | account-response | -          | -         | -                        | Get current authenticated user    |
| /api/v2/account                | PATCH  | 204        | -                | -          | -         | account-update-request   |                                   |
| /api/v2/account                | DEL    | 204        | -                | -          | -         | -                        | Delete current authenticated user |
