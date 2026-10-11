from django.core.exceptions import ValidationError
from django.http import Http404
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
        try:
            news = Posts.objects.filter(id=id, is_deleted=False).first()
        except (ValueError, ValidationError):
            news = None
        if news is None:
            raise Http404("Yangilik topilmadi")

    context = {
        "id": id,
        "news": news,
        "comments": comments,
    }
    if id != 0 and news:
        context["seo_description"] = getattr(news, "title_uz_uz", "") or ""
    return render(request, "news/index.html", context=context)
