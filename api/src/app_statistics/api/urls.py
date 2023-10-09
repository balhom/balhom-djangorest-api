from django.urls import path
from app_statistics.api.views.statistics_month_view import StatisticsMonthView
from app_statistics.api.views.statistics_year_view import StatisticsYearView

urlpatterns = [
    path("statistics/<int:year>/<int:month>", StatisticsMonthView.as_view(),
         name="statistics-month"),
    path("statistics/<int:year>", StatisticsYearView.as_view(),
         name="statistics-year")
]
