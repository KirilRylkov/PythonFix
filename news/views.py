from django.shortcuts import render
import requests
from .models import News
from .forms import NewsForm


def news(request):
    appid = '3f8e7eb4584d429baa3ffc20b5a302db'
    url = 'https://newsapi.org/v2/top-headlines?country=us&apiKey=' + appid
    if request.method == 'POST':
        form = NewsForm(request.POST)
        form.save()
    form = NewsForm()
    searches = News.objects.all()
    all_news = []
    j = 0
    for i in searches:
        print(i)
        res = requests.get(url.format(i.search)).json()
        print(res)
        new_info = {
            'title': res["articles"][j]["title"],
            'author': res['articles'][j]["author"],
            'description': res['articles'][j]["description"],
            'content': res['articles'][j]["content"],
            'data': res['articles'][j]['publishedAt'],
            'image': res['articles'][j]['urlToImage'],
        }
        j += 1
        all_news.append(new_info)
    context = {'all_info': all_news, 'form': form}
    return render(request, 'news/news.html', context)
