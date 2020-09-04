from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from cities.models import City
from cities.serializers import CitySerializer

# Create your views here.


@csrf_exempt
def city_list(request):
    if request.method == "GET":
        cities = City.objects.all()
        serializer = CitySerializer(cities, many=True)
        return JsonResponse(serializer.data, safe=False)


@csrf_exempt
def city_detail(request, pk):
    try:
        city = City.objects.get(pk=pk)
    except City.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == "GET":
        serializer = CitySerializer(city)
        return JsonResponse(serializer.data)

