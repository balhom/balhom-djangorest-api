from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from django.utils.translation import gettext_lazy as _
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from src.balance.models.balance_type_model import BalanceType
from src.balance.api.serializers.balance_type_serializer import BalanceTypeSerializer


class BalanceTypeViewSet(ModelViewSet):
    queryset = BalanceType.objects.all()  # pylint: disable=no-member
    serializer_class = BalanceTypeSerializer
    permission_classes = (IsAuthenticated,)

    def validate(self):
        if "type" not in list(self.kwargs):
            raise ValidationError({"type": [_("type not provided")]})
        if not BalanceType.objects.filter(  # pylint: disable=no-member
            type=self.kwargs["type"]
        ).exists():
            raise ValidationError({"type": [_("type not valid")]})

    def get_queryset(self):
        """
        Filter objects by owner
        """
        if getattr(self, "swagger_fake_view", False):
            return BalanceType.objects.none()  # return empty queryset
        self.validate()
        return BalanceType.objects.filter(  # pylint: disable=no-member
            type=self.kwargs["type"]
        )

    def get_object(self):
        return self.get_queryset().get(
            name=self.kwargs["name"])

    @method_decorator(cache_page(12 * 60 * 60))
    @method_decorator(vary_on_headers("Authorization"))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, args, kwargs)

    @method_decorator(cache_page(12 * 60 * 60))
    @method_decorator(vary_on_headers("Authorization"))
    def list(self, request, *args, **kwargs):
        return super().list(request, args, kwargs)

    def paginate_queryset(self, queryset):
        """
        Avoid using pagination in view
        """
        return None


balance_type_list_view = BalanceTypeViewSet.as_view({
    "get": "list",
})
balance_type_view = BalanceTypeViewSet.as_view({
    "get": "retrieve",
})
