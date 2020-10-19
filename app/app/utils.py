from cities.models import City
from sports.models import Sport


def city_query_param(model, queryset, city_name=None):
    if city_name is not None:
        city = City.objects.filter(name=city_name)
        if not city.count():
            queryset = model.objects.none()
        elif city.count() == 1:
            queryset = queryset.filter(city=city[0].id)
        else:
            result = {}
            for num in city:
                result += queryset.filter(city=num)
            queryset = result
    return queryset


def sport_query_param(model, queryset, sport_name=None):
    if sport_name is not None:
        sport = Sport.objects.filter(name=sport_name)
        if not sport.count():
            queryset = model.objects.none()
        elif sport.count() == 1:
            queryset = queryset.filter(city=sport[0].id)
        else:
            result = {}
            for num in sport:
                result += queryset.filter(city=num)
            queryset = result
    return queryset
