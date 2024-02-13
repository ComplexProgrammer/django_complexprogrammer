from django.shortcuts import render
from django.db.models import Count

from blog.models import Categories, Posts
def index(request):
    id = request.GET.get('id', 0)
    post=[]
    posts=Posts.objects.filter(is_deleted=False).values()
    categories=Categories.objects.filter(is_deleted=False).values()
    posts=Posts.objects.filter(is_deleted=False).values('actor').annotate(total=Count('actor'))
    if id != 0:
        post=Posts.objects.filter(id=id).values().first()
    context={
        'id':id,
        'post': post,
        'posts':posts,
        'categories':categories,
    }
    return render(request, 'blog/index.html', context=context)
