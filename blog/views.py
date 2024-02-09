from django.shortcuts import render

from blog.models import Posts
def index(request):
    data=[]
    id = request.GET.get('id', 0)
    if id == 0:
        data=Posts.objects.filter(is_deleted=False).values()
    else:
        data=Posts.objects.filter(id=id).values().first()
    context={
        'id':id,
        'data': data
    }
    return render(request, 'blog/index.html', context=context)
