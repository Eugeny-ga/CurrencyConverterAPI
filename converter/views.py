from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from django.core.cache import cache


class CurrencyConverterView(APIView):
    def get(self, request) -> Response:
        """
        Конвертация валюта по курсам ЦБ РФ.
        Возвращает результат конвертации валюты в json.
        Пример ответа: {'result': 123.45}.
        """
        # Получить параметры запроса
        from_currency = request.GET.get('from')
        to_currency = request.GET.get('to')
        value = request.GET.get('value')

        # Получить курсы валют относительно рубля и сохранить в кэш,
        # так как API ЦБ РФ имеет ограничения по количеству запросов.

        data = cache.get('data')
        if not data:
            data = requests.get().json()
            cache.set('data', data)

        # В API ЦБ РФ курсы валют сформированы относительно рубля РФ.
        # Сам рубль РФ в json отсутствует.
        # Поэтому это отсутствующее значение заменяем на 1 во избежание ошибки.

        value = value or 1
        exchange_rate_from = data['Valute'].get(from_currency, {'Value': 1})['Value']
        exchange_rate_to = data['Valute'].get(to_currency, {'Value': 1})['Value']

        # Конвертировать значение валюты
        converted_value = (exchange_rate_from / exchange_rate_to) * float(value)

        # Создать ответ
        response = Response({
            'result': round(converted_value, 4)
        })

        return response

class CurrencyRatesView(APIView):
    def get(self, request) -> Response:
        """Получаем все курсы валют с сайта ЦБ РФ"""
        data = cache.get('data')
        if not data:
            data = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
            cache.set('data', data)
        return Response(data)


class CurrencyFromRedis(APIView):
    """Получаем курсы валют из кэша"""
    def get(self, request) -> Response:
        data = cache.get('data')
        return Response(data)

