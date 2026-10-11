from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from django.db import migrations

MEANINGFUL_PARAMS = ("id", "categorie_id", "type_id", "group_id", "book_id")
LANG_PREFIXES = {"uz", "en", "tr", "ru"}


def normalize(url):
    # comments/pages.py dagi normalize_page_url nusxasi (migratsiya o'zgarmasligi uchun)
    parts = urlsplit(url or "")
    path = parts.path or "/"
    segments = path.split("/")
    if len(segments) > 2 and segments[1] in LANG_PREFIXES:
        path = "/" + "/".join(segments[2:])
    query = urlencode(
        sorted((k, v) for k, v in parse_qsl(parts.query) if k in MEANINGFUL_PARAMS)
    )
    netloc = parts.netloc.lower()
    if netloc.startswith("www."):
        netloc = netloc[4:]
    return urlunsplit(("https", netloc, path, query, ""))


def forwards(apps, schema_editor):
    Comment = apps.get_model("comments", "Comment")
    changed = []
    for comment in Comment.objects.only("id", "page_url").iterator():
        new_url = normalize(comment.page_url)
        if new_url != comment.page_url:
            comment.page_url = new_url
            changed.append(comment)
    Comment.objects.bulk_update(changed, ["page_url"], batch_size=500)


class Migration(migrations.Migration):
    dependencies = [("comments", "0005_comment_email")]

    operations = [migrations.RunPython(forwards, migrations.RunPython.noop)]
