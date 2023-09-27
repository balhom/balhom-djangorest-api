# Balance Endpints

| Path                               | Method | Res Status | Res Body                        | Res Cookie | Req Param                                                          | Req Body                 | Comments |
| ---------------------------------- | ------ | ---------- | ------------------------------- | ---------- | ------------------------------------------------------------------ | ------------------------ | -------- |
| /api/v2/annual-balance             | GET    | 200        | page [annual-balance-response]  | -          | -                                                                  | -                        |          |
| /api/v2/annual-balance/{id}        | GET    | 200        | annual-balance-response         | -          | -                                                                  | -                        |          |
| /api/v2/monthly-balance            | GET    | 200        | page [monthly-balance-response] | -          | -                                                                  | -                        |          |
| /api/v2/monthly-balance/{id}       | GET    | 200        | monthly-balance-response        | -          | -                                                                  | -                        |          |
| /api/v2/balance                    | GET    | 200        | page [balance-response]         | -          | converted_quantity_min, converted_quantity_max, date_from, date_to | -                        |          |
| /api/v2/balance/{id}               | GET    | 200        | balance-response                | -          | -                                                                  | -                        |          |
| /api/v2/balance                    | POST   | 201        | balance-response                | -          | -                                                                  | balance-creation-request |          |
| /api/v2/balance                    | PATCH  | 204        | -                               | -          | -                                                                  | balance-update-request   |          |
| /api/v2/balance/{id}               | DEL    | 204        | balance-response                | -          | -                                                                  | -                        |          |
| /api/v2/balance/years/{type}       | GET    | 200        | balance-years-response          | -          | -                                                                  | -                        |          |
| /api/v2/balance/type/{type}        | GET    | 200        | page [balance-type-response]    | -          | -                                                                  | -                        |          |
| /api/v2/balance/type/{type}/{name} | GET    | 200        | balance-type-response           | -          | -                                                                  | -                        |          |
