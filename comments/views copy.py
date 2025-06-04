from django.shortcuts import render, redirect, get_object_or_404
from .forms import CommentForm
from .models import Comment
from django.http import HttpResponseRedirect

def add_comment(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            parent_id = request.POST.get('parent_id')
            if parent_id:
                parent = Comment.objects.get(id=parent_id)
                comment.parent = parent
            comment.save()
            return HttpResponseRedirect(request.POST.get('page_url'))
    else:
        form = CommentForm()      # Get comments for the current page
    current_url = request.build_absolute_uri()
    comments = Comment.objects.filter(
        page_url=request.POST.get('page_url', current_url),
        parent=None  # Only get top-level comments
    ).prefetch_related(
        'replies',
        'replies__replies',  # Get replies of replies
        'replies__replies__replies'  # Get even deeper replies
    ).order_by('-created_at')
    
    return render(request, 'comment_form.html', {'form': form, 'comments': comments})