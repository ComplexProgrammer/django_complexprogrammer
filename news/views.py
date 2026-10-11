from django.shortcuts import render
from comments.pages import page_comments
from news.models import Posts


def index(request):
    news = []
    comments = page_comments(request)

    id = request.GET.get("id", 0)
    if id == 0:
        news = Posts.objects.filter(is_deleted=False).values()
    else:
        news = Posts.objects.filter(id=id).first()

    context = {
        "id": id,
        "news": news,
        "comments": comments,
    }
    return render(request, "news/index.html", context=context)
