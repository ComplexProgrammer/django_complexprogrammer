from datetime import timedelta

from django.contrib import messages
from django.utils import timezone
from django.core.cache import cache
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from comments.pages import normalize_page_url, page_comments
from comments.utils import in_background, send_comment_notification, send_reply_notification
from .forms import CommentForm
from .models import Comment

# Bitta IP'dan RATE_LIMIT daqiqada RATE_LIMIT_COUNT tadan ko'p izoh yozib bo'lmaydi
RATE_LIMIT_COUNT = 5
RATE_LIMIT_SECONDS = 10 * 60
# Sahifada birdaniga shuncha izoh chiqadi, qolganlari "Ko'proq izohlar" tugmasi bilan (comment_form.html)
COMMENTS_PER_PAGE = 20


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
        reason = form.errors.get("text")
        messages.error(request, f"Izoh yuborilmadi: {reason[0] if reason else 'maydonlarni to‘g‘ri to‘ldiring.'}")
        return _safe_redirect(request, back_url)

    comment = form.save(commit=False)
    # Rasmiy javob belgisi soxtalashtirilmasin: bu email faqat xodimlarga
    if comment.is_official and not request.user.is_staff:
        messages.error(request, "Bu email manzilidan foydalanib bo'lmaydi.")
        return _safe_redirect(request, back_url)
    comment.page_url = normalize_page_url(back_url)
    parent = None
    parent_id = request.POST.get("parent_id")
    if parent_id:
        parent = Comment.objects.filter(id=parent_id).first() if parent_id.isdigit() else None
        if parent is None:
            return _safe_redirect(request, back_url)
        comment.parent = parent
        comment.page_url = parent.page_url

    # Takror yuborish (ikki marta bosish, sahifani yangilash): bazadagi izohlarning ~44% shunday edi
    duplicate = Comment.objects.filter(
        page_url=comment.page_url,
        email__iexact=comment.email,
        text=comment.text,
        parent=parent,
        created_at__gte=timezone.now() - timedelta(hours=24),
    ).exists()
    if duplicate:
        messages.info(request, "Bu izoh allaqachon qoldirilgan.")
        return _safe_redirect(request, back_url)
    comment.save()
    cache.set(rate_key, sent + 1, RATE_LIMIT_SECONDS)

    if parent is None:
        in_background(send_comment_notification, comment)
    else:
        in_background(send_reply_notification, comment, parent)
    messages.success(request, "Izohingiz qabul qilindi. Rahmat!")
    return _safe_redirect(request, back_url)


def more_comments(request):
    """Sahifaning keyingi COMMENTS_PER_PAGE ta izohi (HTML bo'lagi) — "Ko'proq izohlar" tugmasi uchun."""
    try:
        offset = max(int(request.GET.get("offset", 0)), 0)
    except ValueError:
        offset = 0
    page_url = normalize_page_url(request.GET.get("page_url", ""))
    comments = page_comments(request, page_url)[offset:offset + COMMENTS_PER_PAGE]
    return render(request, "comment_more.html", {"comments": comments})
