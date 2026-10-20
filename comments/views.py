from django.contrib import messages
from django.core.cache import cache
from django.http import HttpResponseRedirect
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from comments.pages import normalize_page_url
from comments.utils import in_background, send_comment_notification, send_reply_notification
from .forms import CommentForm
from .models import Comment

# Bitta IP'dan RATE_LIMIT daqiqada RATE_LIMIT_COUNT tadan ko'p izoh yozib bo'lmaydi
RATE_LIMIT_COUNT = 5
RATE_LIMIT_SECONDS = 10 * 60


def _client_ip(request):
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "")


def _safe_redirect(request, url):
    if url and url_has_allowed_host_and_scheme(
        url, allowed_hosts={request.get_host()}, require_https=request.is_secure()
    ):
        return HttpResponseRedirect(url + "#comments")
    return HttpResponseRedirect("/")


@require_POST
def add_comment(request):
    back_url = request.POST.get("page_url", "")

    # Honeypot: odamlar bu maydonni ko'rmaydi, botlar esa to'ldiradi
    if request.POST.get("website"):
        return _safe_redirect(request, back_url)

    rate_key = f"comment-rate:{_client_ip(request)}"
    sent = cache.get(rate_key, 0)
    if sent >= RATE_LIMIT_COUNT:
        messages.error(request, "Juda ko'p izoh yubordingiz. Birozdan so'ng urinib ko'ring.")
        return _safe_redirect(request, back_url)

    form = CommentForm(request.POST)
    if not form.is_valid():
        messages.error(request, "Izoh yuborilmadi: maydonlarni to'g'ri to'ldiring.")
        return _safe_redirect(request, back_url)

    comment = form.save(commit=False)
    comment.page_url = normalize_page_url(back_url)
    parent = None
    parent_id = request.POST.get("parent_id")
    if parent_id:
        parent = Comment.objects.filter(id=parent_id).first() if parent_id.isdigit() else None
        if parent is None:
            return _safe_redirect(request, back_url)
        comment.parent = parent
        comment.page_url = parent.page_url
    comment.save()
    cache.set(rate_key, sent + 1, RATE_LIMIT_SECONDS)

    if parent is None:
        in_background(send_comment_notification, comment)
    else:
        in_background(send_reply_notification, comment, parent)
    messages.success(request, "Izohingiz qabul qilindi. Rahmat!")
    return _safe_redirect(request, back_url)
