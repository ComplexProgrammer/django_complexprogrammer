from django.shortcuts import render
from comments.models import Comment
from news.models import Posts

def index(request):
    news = []
    current_url = request.build_absolute_uri()
    comments = Comment.objects.filter(
        page_url=current_url,
        parent=None  # Only get top-level comments
    ).prefetch_related(
        'replies',  # First level replies
        'replies__replies',  # Second level replies
        'replies__replies__replies',  # Third level replies
        'replies__replies__replies__replies'  # Fourth level replies
    ).order_by('-created_at')
    
    id = request.GET.get('id', 0)
    if id == 0:
        news = Posts.objects.filter(is_deleted=False).values()
    else:
        news = Posts.objects.filter(id=id).first()
    
    context = {
        'id': id,
        'news': news,
        'comments': comments,
    }
    return render(request, "news/index.html", context=context)
