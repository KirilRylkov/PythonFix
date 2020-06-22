from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm
# Create your views here.


def weather(request):
    appid = 'c46a06be02e85b5ecf69a021d7cdc30a'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + appid
    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()
    form = CityForm()
    cities = City.objects.all()
    all_cities = []
    for i in cities:
        res = requests.get(url.format(i.name)).json()
        print(res)
        city_info = {
            'city': i.name,
            'temp': res["main"]["temp"],
            'icon': res["weather"][0]["icon"],
        }
        all_cities.append(city_info)
    context = {'all_info': all_cities, 'form': form,}
    return render(request, 'weather/weather.html', context)
