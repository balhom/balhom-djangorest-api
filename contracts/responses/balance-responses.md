# Balance Responses

| name               | type                | comments |
| ------------------ | ------------------- | -------- |
| id                 | UUID                |          |
| name               | String              |          |
| description        | String              |          |
| real_quantity      | double              |          |
| converted_quantity | double              |          |
| date               | LocalDateTime       |          |
| currency_type      | String              |          |
| balance_type       | BalanceTypeResponse |          |

## Balance Type Response

| name  | type            | comments |
| ----- | --------------- | -------- |
| name  | String          |          |
| type  | BalanceTypeEnum | not-null |
| image | String          |          |

## Enums options:

* **BalanceTypeEnum**: expense, revenue
