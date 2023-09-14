from django.urls import path

from converter.views import CurrencyConverterView, CurrencyRatesView, CurrencyFromRedis

urlpatterns = [
    path('rates/', CurrencyConverterView.as_view()),
    path('all_rates/', CurrencyRatesView.as_view()),
    path('cashe_rates/', CurrencyFromRedis.as_view()),
]