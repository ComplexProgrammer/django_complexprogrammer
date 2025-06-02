from comments.models import Comment

class CommentsMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) if hasattr(super(), 'get_context_data') else {}
        current_url = self.request.build_absolute_uri()
        comments = Comment.objects.filter(
            page_url=current_url,
            parent=None
        ).prefetch_related(
            'replies',
            'replies__replies',
            'replies__replies__replies'
        ).order_by('-created_at')
        context['comments'] = comments
        return context
