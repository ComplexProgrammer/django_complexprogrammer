"""AI izoh qoralamalarini bazaga yoziş (server tomoni). ``draft_explanations collect`` va ``import_explanations`` işlatadi."""

from core.translit import clean_uz_latin, latin1995_to_2026, latin_to_cyrillic


def save_draft(kind, key, data):
    """Bitta qoralamani saqlaydi. Saqlangan bölsa True.

    ``kind``/``key``: "avtotest" + (bilet, raqam) | "avtotest_id" + AvtoTest.pk | "tests" + Questions.pk.
    /avtotest/ izohi asosiy manbaga (tests, kitob 49/50) yoziladi — AvtoTest undan ``sync_all()`` bilan yangilanadi.
    Admin tasdiqlagan izohga tegilmaydi.
    """
    from projects.avtotest_sync import tests_question
    from projects.models import AvtoTest
    from tests.models import Questions

    if kind == "avtotest_id":
        row = AvtoTest.objects.filter(pk=key).first()
        if row is None:
            return False
        kind, key = "avtotest", (row.bilet, row.raqam)
    if kind == "avtotest":
        question = tests_question(*key)
        if question is None:
            return False
        pk = question.pk
    else:
        pk = key
    # Bazadagi savollar 2026-yilgi imloda (ş, ç, ğ, ö) — izoh ham şunday saqlanadi
    # AI ba'zan turkça/kirill harflarni aralaştiradi (körä, öрнатилган) — tozalab saqlanadi
    uz = clean_uz_latin(latin1995_to_2026((data.get("uz") or "").strip()))
    if not uz:
        return False
    return bool(Questions.objects.filter(pk=pk).exclude(explanation_status="approved").update(
        explanation_uz_uz=uz, explanation_uz_crl=latin_to_cyrillic(uz),
        explanation_ru_ru=(data.get("ru") or "").strip(), explanation_en_us=(data.get("en") or "").strip(),
        explanation_confidence=data.get("confidence") or "", explanation_status="draft",
    ))


def sync_avtotest():
    """``update()`` signal yubormaydi — yangi izohlar /avtotest/ ga ham tuşsin."""
    from projects.avtotest_sync import builder

    builder().sync_all()
