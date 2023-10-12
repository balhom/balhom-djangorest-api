# Account Requests

## Account Creation Request

| name                     | type   | validations                                      | comments             |
| ------------------------ | ------ | ------------------------------------------------ | -------------------- |
| username                 | String | max-size: 15, regex: "^[A-Za-z0-9]+$", not-blank |                      |
| email                    | String | format: email, not-blank                         |                      |
| locale                   | String | max-size: 5, not-blank                           |                      |
| inv_code                 | UUID   | not-null                                         |                      |
| password                 | String | format: password, not-blank                      |                      |
| expected_annual_balance  | double | min: 0                                           | Optional, default: 0 |
| expected_monthly_balance | double | min: 0                                           | Optional, default: 0 |
| pref_currency_type       | String | max-size: 4, not-blank                           |                      |

## Account Update Request

| name                     | type    | validations                                      | comments |
| ------------------------ | ------- | ------------------------------------------------ | -------- |
| username                 | String  | max-size: 15, regex: "^[A-Za-z0-9]+$", not-empty |          |
| locale                   | String  | max-size: 5, not-empty                           |          |
| receive_email_balance    | Boolean |                                                  |          |
| balance                  | Double  |                                                  |          |
| expected_annual_balance  | Double  | min: 0                                           |          |
| expected_monthly_balance | Double  | min: 0                                           |          |
| pref_currency_type       | String  | max-size: 4, not-empty                           |          |

> Note:
> * If `balance` is not specified and `pref_currency_type` is specified then the stored `balance` is converted with the specified `pref_currency_type` using the currency conversion api.

## Account Image Update Request

| name  | type          | validations | comments |
| ----- | ------------- | ----------- | -------- |
| image | MultiPartFile |             |          |

## Email Request

| name  | type   | validations   | comments |
| ----- | ------ | ------------- | -------- |
| email | String | format: email |          |

## Change Password Request

| name         | type   | validations      | comments |
| ------------ | ------ | ---------------- | -------- |
| old_password | String | not-blank        |          |
| new_password | String | format: password |          |
