# Balance Requests

## Balance Creation Request

| name               | type               | validations             | comments |
| ------------------ | ------------------ | ----------------------- | -------- |
| name               | String             | max-size: 40, not-blank |          |
| description        | String             | max-size: 2000          |          |
| real_quantity      | double             | min: 0                  |          |
| converted_quantity | Double             | min: 0                  |          |
| date               | LocalDateTime      | not-null                |          |
| currency_type      | String             | max-size: 4, not-blank  |          |
| balance_type       | BalanceTypeRequest | not-null                |          |

> Note:
> * If the `converted_quantity` is not specified then it is obtained from the automatic conversion of the `real_quantity` with the `currency_type` of the account using the currency conversion api.

## Balance Update Request

| name               | type               | validations             | comments |
| ------------------ | ------------------ | ----------------------- | -------- |
| name               | String             | max-size: 40, not-blank |          |
| description        | String             | max-size: 2000          |          |
| real_quantity      | Double             | min: 0                  |          |
| converted_quantity | Double             | min: 0                  |          |
| date               | LocalDateTime      |                         |          |
| currency_type      | String             | max-size: 4, not-empty  |          |
| balance_type       | BalanceTypeRequest |                         |          |

> Note:
> * If `converted_quantity` is not specified then it is obtained from the automatic conversion of the `real_quantity` with the `currency_type` of the account using the currency conversion api.
> * If `real_quantity` is not specified and `currency_type` is specified then the stored `real_quantity` is converted with the specified `currency_type` using the currency conversion api.

## Balance Type Request

| name | type            | validations            | comments |
| ---- | --------------- | ---------------------- | -------- |
| name | String          | max-size: 4, not-blank |          |
| type | BalanceTypeEnum | not-null               |          |

## Enums options:

* **BalanceTypeEnum**: expense, revenue
