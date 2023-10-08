# Auth Requests

## Email Request

| name  | type   | validations   | comments |
| ----- | ------ | ------------- | -------- |
| email | String | format: email |          |

## Change Password Request

| name         | type   | validations      | comments |
| ------------ | ------ | ---------------- | -------- |
| old_password | String | not-blank        |          |
| new_password | String | format: password |          |
