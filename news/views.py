from django.shortcuts import render

from news.models import Posts

def index(request):
    news=[]
    id = request.GET.get('id', 0)
    if id == 0:
        news=Posts.objects.values()
    else:
        news=Posts.objects.filter(id=id).first()
    context={
        'id':id,
        'news': news
    }
    return render(request, "news/index.html", context=context)
