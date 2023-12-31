from django.urls import path
from src.balance.api.views.annual_balance_view import annual_balance_view, annual_balance_list_view
from src.balance.api.views.monthly_balance_view import monthly_balance_view, monthly_balance_list_view
from src.balance.api.views.balance_view import balance_list_create_view, balance_get_update_view
from src.balance.api.views.balance_years_view import BalanceYearsRetrieveView
from src.balance.api.views.balance_type_view import balance_type_list_view, balance_type_view
from src.balance.api.views.balance_summary_month_view import BalanceSummaryMonthView
from src.balance.api.views.balance_summary_year_view import BalanceSummaryYearView


urlpatterns = [
    # Annual Balance urls
    path("annual-balance", annual_balance_list_view, name="annual-balance-list"),
    path("annual-balance/<int:pk>", annual_balance_view,
         name="annual-balance"),
    # Monthly Balance urls
    path("monthly-balance", monthly_balance_list_view,
         name="monthly-balance-list"),
    path("monthly-balance/<int:pk>", monthly_balance_view,
         name="monthly-balance"),
    # Balance years url
    path("balance/years/<str:type>", BalanceYearsRetrieveView.as_view(),
         name="balance-years-get"),
    # Balance type url
    path("balance/type/<str:type>/<str:name>", balance_type_view,
         name="balance-type-get"),
    path("balance/type/<str:type>", balance_type_list_view,
         name="balance-type-list"),
    # Balance urls
    path("balance/summary/<str:type>/<int:year>/<int:month>", BalanceSummaryMonthView.as_view(),
         name="balance-summary-month"),
    path("balance/summary/<str:type>/<int:year>", BalanceSummaryYearView.as_view(),
         name="balance-summary-year"),
    path("balance", balance_list_create_view,
         name="balance-list-create"),
    path("balance/<int:pk>", balance_get_update_view,
         name="balance-get-update"),
]
