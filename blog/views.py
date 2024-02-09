from django.shortcuts import render

from blog.models import Categories, Posts
def index(request):
    id = request.GET.get('id', 0)
    data=[]
    categories=Categories.objects.filter(is_deleted=False).values()
    if id == 0:
        data=Posts.objects.filter(is_deleted=False).values()
    else:
        data=Posts.objects.filter(id=id).values().first()
    context={
        'id':id,
        'data': data,
        'categories':categories
    }
    return render(request, 'blog/index.html', context=context)
