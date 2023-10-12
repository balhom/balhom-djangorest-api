# User Endpints

| Path                    | Method | Res Status | Res Body         | Res Cookie | Req Param | Req Body                     | Comments                          |
| ----------------------- | ------ | ---------- | ---------------- | ---------- | --------- | ---------------------------- | --------------------------------- |
| /api/v2/account         | POST   | 201        | account-response | -          | -         | account-creation-request     |                                   |
| /api/v2/account/profile | GET    | 200        | account-response | -          | -         | -                            | Get current authenticated user    |
| /api/v2/account/profile | PATCH  | 204        | -                | -          | -         | account-update-request       |                                   |
| /api/v2/account/image   | PUT    | 204        | -                | -          | -         | account-image-update-request |                                   |
| /api/v2/account/profile | DEL    | 204        | -                | -          | -         | -                            | Delete current authenticated user |
