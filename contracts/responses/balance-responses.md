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
| type  | BalanceTypeEnum |          |
| image | String          |          |

## Annual Balance Response

| name              | type   | comments |
| ----------------- | ------ | -------- |
| gross_quantity    | double |          |
| expected_quantity | double |          |
| currency_type     | String |          |
| year              | int    |          |

## Monthly Balance Response

| name              | type   | comments |
| ----------------- | ------ | -------- |
| gross_quantity    | double |          |
| expected_quantity | double |          |
| currency_type     | String |          |
| year              | int    |          |
| month             | int    |          |

## Balance Years Response

| name  | type       | comments |
| ----- | ---------- | -------- |
| years | List [int] |          |

## Enums options:

* **BalanceTypeEnum**: expense, revenue
