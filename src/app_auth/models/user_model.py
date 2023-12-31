import uuid
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _


class BalanceUserManager(UserManager):
    def create_user(
        self, keycloak_id, **extra_fields
    ):  # pylint: disable=arguments-differ
        if not keycloak_id:
            raise ValueError(
                _(
                    "A keycloak id must be provided"
                )  # pylint: disable=used-before-assignment
            )

        from src.currency_conversion_client.django_client import get_currency_conversion_client
        currency_conversion_client = get_currency_conversion_client()
        currency_type = currency_conversion_client.get_currency_codes()[0]

        return User.objects.create(
            keycloak_id=keycloak_id,
            is_staff=False,
            is_superuser=False,
            pref_currency_type=currency_type,
        )

    def create_superuser(
        self, keycloak_id, **extra_fields
    ):  # pylint: disable=arguments-differ
        if not keycloak_id:
            raise ValueError(
                _(
                    "A keycloak id must be provided"
                )  # pylint: disable=used-before-assignment
            )

        from src.currency_conversion_client.django_client import get_currency_conversion_client
        currency_conversion_client = get_currency_conversion_client()
        currency_type = currency_conversion_client.get_currency_codes()[0]

        return User.objects.create(
            keycloak_id=keycloak_id,
            is_staff=True,
            is_superuser=True,
            pref_currency_type=currency_type,
        )


def _image_user_dir(instance, filename):
    # File will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return "user_{0}/{1}".format(instance.id, filename)


class User(AbstractUser):
    # Fields to ignore in db form default User model:
    first_name = None
    last_name = None
    password = None
    username = None
    email = None

    # Change default id to uuid will make
    # an enumeration attack more difficult
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    keycloak_id = models.TextField(
        verbose_name=_("keycloak id"), unique=True, editable=False
    )
    image = models.ImageField(
        verbose_name=_("profile image"),
        upload_to=_image_user_dir,
        default="users/default_user.jpg",
    )
    current_balance = models.FloatField(
        verbose_name=_("current balance"),
        default=0.0
    )
    receive_email_balance = models.BooleanField(
        verbose_name=_("receive email about balance"),
        default=True
    )
    # Expected annual balance at the end of a year,
    # it is used to be subtracted with the gross balance of each year
    # and get the net balance
    expected_annual_balance = models.FloatField(
        verbose_name=_("expected annual balance"),
        validators=[MinValueValidator(0.0)],
        default=0.0,
    )
    # Expected monthly balance at the end of a month,
    # it is used to be subtracted with the gross balance of each month
    # and get the net balance
    expected_monthly_balance = models.FloatField(
        verbose_name=_("expected monthly balance"),
        validators=[MinValueValidator(0.0)],
        default=0.0,
    )
    # Date of the last password reset code sent
    date_pass_reset = models.DateTimeField(
        verbose_name=_("date of last password reset code sent"), blank=True, null=True
    )
    # Number of requests for password reset
    count_pass_reset = models.IntegerField(
        verbose_name=_("number of requests for password reset"), default=0
    )
    pref_currency_type = models.CharField(
        verbose_name=_("preferred currency type"),
        max_length=4,
    )
    # Date of the last preferred currency type change.
    # It is stored because this action requires time and compute power
    date_currency_change = models.DateTimeField(
        verbose_name=_("date of last preferred currency type change"),
        blank=True,
        null=True,
    )

    objects = BalanceUserManager()
    USERNAME_FIELD = "keycloak_id"
    REQUIRED_FIELDS = []

    def __str__(self):
        return str(self.keycloak_id)
