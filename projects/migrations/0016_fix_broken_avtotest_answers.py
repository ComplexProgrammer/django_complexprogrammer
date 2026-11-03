"""Töğri javobini tanlab bölmaydigan 3 ta avtotest savolini tuzatiş.

Asl manbada 5 variantli (A–E) bölgan savollar 4 ustunga siğmay qolgan:
* 136-bilet 1-savol (93-7.jpg): variantlar "c, a, d, e", töğri javob "E" — ammo rasmdagi
  "ikkinçi darajali yöl bilan tutaşuv" belgisi "b" (1.13.2), u variantlar orasida yöq edi.
* 126-bilet 8-savol (Şokning belgilari): töğri javob "E" ("barça javoblar töğri") taşlab ketilgan,
  inglizça maydonlarda esa özbekça kirill matni turgan edi.
* 95-bilet 4-savol (z158.jpg): töğri javob "D", lekin D variant böş. YHQ böyiça burilişda
  ikkala tomonda ham piyodalarga yöl beriladi — "C".

Xuddi şu savollar /tests/ dagi kitoblarda ham bor (töğri javob belgilanmagan) — ular ham tuzatiladi.
Savol matni böyiça topiladi: id lar boşqa bazada farq qilsa ham işlaydi; topilmasa — öziga tegmaydi.
"""
from django.db import migrations

SIGNS_Q = "Qaysi belgi ikkinçi darajali yöl bilan tutaşuvni bildiradi?"
SHOCK_Q = "Şokning belgilari:"
SIGNS_EN = "Which sign indicates a junction with a secondary road?"
TURN_Q = "Qaysi tomonga burilayotganda piyodalarga yöl beriş kerak?"

SHOCK = {
    "uz": ["Teri va şilliq qavatlarning oqarişi, kuçli ter ajralişi", "Es-huşning noaniqligi, behuş holat",
           "Oğiz qurişi, çanqoqlik, nafas olişning tezlaşuvi", "Barça javoblar töğri"],
    "ru": ["Побледнение кожи и слизистых, сильное потоотделение", "Спутанность сознания, обморочное состояние",
           "Сухость рта, жажда, учащённое дыхание", "Все ответы верны"],
    "en": ["Pale skin and mucous membranes, heavy sweating", "Confusion, fainting",
           "Dry mouth, thirst, rapid breathing", "All of the above"],
}


def fix_avtotest(apps):
    AvtoTest = apps.get_model("projects", "AvtoTest")
    for q in AvtoTest.objects.filter(savol=SIGNS_Q, javob="E"):
        q.savol_en = SIGNS_EN
        for lang in ("", "_en", "_ru"):
            for col, val in zip("abcd", ("a", "b", "d", "e")):
                setattr(q, f"javob_{col}{lang}", val)
        q.javob = "B"
        q.save()
    for q in AvtoTest.objects.filter(savol=SHOCK_Q, javob="E"):
        q.savol_en = "Signs of shock:"
        for lang, sfx in (("uz", ""), ("ru", "_ru"), ("en", "_en")):
            for col, val in zip("abcd", SHOCK[lang]):
                setattr(q, f"javob_{col}{sfx}", val)
        q.javob = "D"
        q.save()
    AvtoTest.objects.filter(savol=TURN_Q, javob="D", javob_d="").update(javob="C")


def fix_tests(apps):
    try:
        Questions = apps.get_model("tests", "Questions")
        Answers = apps.get_model("tests", "Answers")
    except LookupError:
        return

    def no_right(qs):
        return [q for q in qs if not Answers.objects.filter(question=q, is_deleted=False, right=True).exists()]

    for q in no_right(Questions.objects.filter(name_uz_uz=SIGNS_Q, is_deleted=False)):
        answers = list(Answers.objects.filter(question=q, is_deleted=False).order_by("number"))
        q.name_en_us = SIGNS_EN
        q.save()
        if len(answers) == 4:
            for a, val in zip(answers, ("a", "b", "d", "e")):
                a.name_uz_uz = a.name_uz_crl = a.name_ru_ru = a.name_en_us = val
                a.right = val == "b"
                a.save()
    for q in no_right(Questions.objects.filter(name_uz_uz=SHOCK_Q, is_deleted=False)):
        q.name_en_us = "Signs of shock:"
        q.save()
        answers = list(Answers.objects.filter(question=q, is_deleted=False).order_by("number"))
        if len(answers) == 4:
            for i, a in enumerate(answers):
                a.name_uz_uz = SHOCK["uz"][i]
                a.name_ru_ru = SHOCK["ru"][i]
                a.name_en_us = SHOCK["en"][i]
                a.right = i == 3
                a.save()
    for q in no_right(Questions.objects.filter(name_uz_uz=TURN_Q, is_deleted=False)):
        Answers.objects.filter(question=q, is_deleted=False, number=3).update(right=True)


def forwards(apps, schema_editor):
    fix_avtotest(apps)
    fix_tests(apps)


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0015_avtotest_bilet_raqam_idx"),
        ("tests", "0023_question_explanation_status"),
    ]

    operations = [
        migrations.RunPython(forwards, migrations.RunPython.noop),
    ]
