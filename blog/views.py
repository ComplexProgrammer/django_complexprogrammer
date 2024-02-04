from django.shortcuts import render
def index(request):
    context={
        'data':''
    }
    return render(request, 'blog/index.html', context=context)
