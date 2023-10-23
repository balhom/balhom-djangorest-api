## Setup steps

1. Go to admin console and login.

2. Create a Realm named `balhom-realm`.

3. Create a Client with `OpenID Connect` type and `balhom-api` id. Then in `Capability config`, `Client authentication` must be enabled and in `Authentication flow` section `Standard flow`, `Direct access grants` and `Service accounts roles` must be enabled.

4. Assign `manage-users` role (realm-management) in `Service accounts roles` tab to `balhom-api` client inside `Clients` section. 

5. In `Login` tab inside `Realm settings` section enable `Email as username`, `Login with email` and `Verify email`.

6. Enable `Internatiolization` in `Localization` tab inside `Realm settings` section, and add "français" and "español" as `Supported locales`.

7. In `Email` tab inside `Realm settings` section setup email settings.

8.  In `Sessions` tab inside `Realm settings` section change `SSO Session Idle` and `SSO Session Max` values to 5 Days.
