from comments.pages import page_comments


class CommentsMixin:
    def get_context_data(self, **kwargs):
        context = (
            super().get_context_data(**kwargs)
            if hasattr(super(), "get_context_data")
            else {}
        )
        context["comments"] = page_comments(self.request)
        return context
