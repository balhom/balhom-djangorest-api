import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _


class InvitationCode(models.Model):
    code = models.UUIDField(
        verbose_name=_("uuid code"),
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    usage_left = models.PositiveIntegerField(
        verbose_name=_("usage left"), default=1)
    is_active = models.BooleanField(verbose_name=_("is active"), default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Invitation code")
        verbose_name_plural = _("Invitation codes")
        ordering = ["-usage_left"]

    def __str__(self) -> str:
        return str(self.code)
