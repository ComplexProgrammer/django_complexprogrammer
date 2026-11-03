"""Özbekiston avtotesti uçun yagona ma'lumot manbasi: ``tests`` ierarxiyasi (kitob 49 va 50).

Bir xil 1385 ta savol ilgari ikki joyda alohida saqlanardi:

* ``tests_*`` (kitob 49 — 1–108-biletlar, kitob 50 "e-avtomaktab" — 109-bilet va undan keyingilari) —
  /tests/ sahifalari va GetTopics/GetQuestions API'lari;
* ``projects_avtotest`` — /avtotest/, mobil ilova (GetSavol), bot, imtihon, PDF, mavzular.

``tests`` strukturasi kengroq (variantlar soni çeklanmagan, 4 til, audit, yumşoq öçiriş), şuning uçun
endi tahrir faqat u yerda qilinadi. ``AvtoTest`` esa undan avtomatik hosil qilinadigan "tekis" nusxa
(moslik qatlami): eski API, bot va mobil ilova özgarişsiz işlayveradi.

* ``AvtoTestBuilder`` — tests -> AvtoTest (doimiy; signallar va ``manage.py sync_avtotest``).
  AvtoTest qatorlari (bilet, raqam) böyiça topiladi, id'lari saqlanadi — mobil ilovadagi va
  brauzerdagi "xatolarim" röyxatlari buzilmaydi.
* ``TestsBootstrap`` — AvtoTest -> tests, faqat bir martalik tozalaş (migratsiya 0017): tests'dagi
  nusxa buzilgan (boşqa savollarning javoblari aralaşgan), AvtoTest'dagisi esa toza edi.

Modellar parametr sifatida beriladi — migratsiyadagi tarixiy modellar bilan ham işlaydi.
"""
import shutil
from pathlib import Path

from core.translit import convert

# (kitob id, birinçi bilet): kitob 49 — 1–108, kitob 50 — 109 va undan keyingi biletlar
SYNCED_BOOKS = ((49, 1), (50, 109))
SYNCED_BOOK_IDS = tuple(book_id for book_id, _ in SYNCED_BOOKS)
LETTERS = "ABCD"  # AvtoTest'da 4 ta ustun bor — variantlar 4 tadan oşmasligi kerak
IMAGE_DIR = "tests/questions/images"


def book_for(bilet):
    """Bilet raqami -> (kitob id, kitob ičidagi bilet (topic) raqami)."""
    for book_id, first in reversed(SYNCED_BOOKS):
        if bilet >= first:
            return book_id, bilet - first + 1
    return None, None


def bilet_for(book_id, number):
    """(kitob id, topic raqami) -> AvtoTest bilet raqami; sinxronlanmaydigan kitob uçun None."""
    for bid, first in SYNCED_BOOKS:
        if bid == book_id and number:
            bilet = first + number - 1
            return bilet if book_for(bilet)[0] == book_id else None
    return None


def _cyr(text):
    return convert(text, "cyr") if text else ""


def _rasm(image_name):
    """tests'dagi rasm yöli -> AvtoTest.rasm (static/avtotest/ ičidagi fayl nomi)."""
    if not image_name:
        return ""
    prefix = IMAGE_DIR + "/"
    return image_name[len(prefix):] if image_name.startswith(prefix) else Path(image_name).name


def _copy(src, dst):
    if src.is_file() and not dst.exists():
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)


def question_problem(question, answers):
    """AvtoTest'ga siğmaydigan savol bölsa — sababi (matn), aks holda None.

    ``answers`` — savolning öçirilmagan javoblari (``number`` böyiça tartiblangan)."""
    options = [a for a in answers if (a.name_uz_uz or "").strip()]
    rights = sum(1 for a in options if a.right)
    if not (question.name_uz_uz or "").strip():
        return "savol matni böş"
    if len(options) > len(LETTERS):
        return f"{len(options)} ta variant (AvtoTest'da {len(LETTERS)} tadan oşmasligi kerak)"
    if len(options) < 2:
        return "variantlar 2 tadan kam"
    if rights != 1:
        return f"töğri javoblar soni {rights} ta (aniq bitta bölişi kerak)"
    if any(a.image for a in options):
        return "javob variantida rasm bor (AvtoTest'da javob rasmi yöq)"
    return None


class _Base:
    STATS = ()

    def __init__(self, dry_run=False):
        self.dry_run = dry_run
        self.stats = {k: 0 for k in self.STATS}

    def _save(self, obj, fields, stat, extra=()):
        if fields:
            self.stats[stat] += 1
            if not self.dry_run:
                obj.save(update_fields=fields + list(extra))

    def _create(self, model, stat, **values):
        self.stats[stat] += 1
        if self.dry_run:
            return model(**values)
        return model.objects.create(**values)


# ================================================================================================
# tests -> AvtoTest (doimiy)
# ================================================================================================
class AvtoTestBuilder(_Base):
    STATS = ("rows_created", "rows_updated", "rows_deleted", "questions_skipped")

    def __init__(self, AvtoTest, Books, Topics, Questions, Answers, static_root=None, media_root=None, dry_run=False):
        super().__init__(dry_run)
        self.AvtoTest, self.Books, self.Topics = AvtoTest, Books, Topics
        self.Questions, self.Answers = Questions, Answers
        self.static_root, self.media_root = static_root, media_root
        self.problems = []  # (bilet, raqam, sabab) — bu savollarning AvtoTest qatori özgartirilmadi
        self._books = {}

    def _book_exists(self, book_id):
        if book_id not in self._books:
            self._books[book_id] = self.Books.objects.filter(id=book_id).exists()
        return self._books[book_id]

    def sync_all(self):
        bilets = set(self.AvtoTest.objects.values_list("bilet", flat=True))
        for book_id, _ in SYNCED_BOOKS:
            for number in self.Topics.objects.filter(book_id=book_id, is_deleted=False).values_list("number", flat=True):
                bilet = bilet_for(book_id, number)
                if bilet:
                    bilets.add(bilet)
        for bilet in sorted(bilets):
            self.sync_bilet(bilet)
        return self.stats

    def sync_bilet(self, bilet):
        book_id, number = book_for(bilet)
        # Kitob umuman yöq bölsa (masalan, böş baza) AvtoTest'ga tegilmaydi — hammasi öçib ketmasin
        if book_id is None or not self._book_exists(book_id):
            return self.stats
        topic = self.Topics.objects.filter(book_id=book_id, number=number, is_deleted=False).order_by("id").first()
        questions, answers = [], {}
        if topic is not None:
            questions = list(self.Questions.objects.filter(topic_id=topic.pk, is_deleted=False).order_by("number", "id"))
            for a in self.Answers.objects.filter(question__in=questions, is_deleted=False).order_by("number", "id"):
                answers.setdefault(a.question_id, []).append(a)

        rows = {}
        for row in self.AvtoTest.objects.filter(bilet=bilet).order_by("raqam", "id"):
            if row.raqam in rows:
                self._delete(row)  # bir xil raqamli ikkinçi nusxa
            else:
                rows[row.raqam] = row

        seen = set()
        for q in questions:
            if q.number in seen:
                self._skip(bilet, q.number, "bilet ičida bir xil raqamli ikkinçi savol")
                continue
            seen.add(q.number)
            row = rows.pop(q.number, None)
            options = answers.get(q.id, [])
            problem = question_problem(q, options)
            if problem:  # eski AvtoTest qatori (bölsa) özgarişsiz qoladi
                self._skip(bilet, q.number, problem)
                continue
            self._sync_row(bilet, q, options, row)
        for row in rows.values():  # tests'da yöq (öçirilgan) savollar
            self._delete(row)
        return self.stats

    def _skip(self, bilet, raqam, reason):
        self.stats["questions_skipped"] += 1
        self.problems.append((bilet, raqam, reason))

    def _delete(self, row):
        self.stats["rows_deleted"] += 1
        if not self.dry_run:
            row.delete()

    def _sync_row(self, bilet, q, answers, row):
        options = [a for a in answers if (a.name_uz_uz or "").strip()]
        rasm = _rasm(q.image.name if q.image else "")
        if rasm and self.media_root and self.static_root and not self.dry_run:
            # AvtoTest sahifasi va bot rasmni /static/avtotest/ dan oladi
            _copy(Path(self.media_root) / q.image.name, Path(self.static_root) / "avtotest" / rasm)
        values = {
            "bilet": bilet, "raqam": q.number,
            "savol": q.name_uz_uz or "", "savol_ru": q.name_ru_ru or "", "savol_en": q.name_en_us or "",
            "javob": next(LETTERS[i] for i, a in enumerate(options) if a.right),
            "rasm": rasm,
            "izoh": q.explanation_uz_uz or "", "izoh_ru": q.explanation_ru_ru or "",
            "izoh_en": q.explanation_en_us or "",
            "izoh_holati": q.explanation_status or "", "izoh_ishonch": q.explanation_confidence or "",
        }
        for i, letter in enumerate(LETTERS.lower()):
            a = options[i] if i < len(options) else None
            values[f"javob_{letter}"] = (a.name_uz_uz or "").strip() if a else ""
            values[f"javob_{letter}_ru"] = (a.name_ru_ru or "").strip() if a else ""
            values[f"javob_{letter}_en"] = (a.name_en_us or "").strip() if a else ""
        if row is None:
            self._create(self.AvtoTest, "rows_created", **values)
            return
        changed = [f for f, v in values.items() if getattr(row, f) != v]
        for f in changed:
            setattr(row, f, values[f])
        self._save(row, changed, "rows_updated")


def builder(dry_run=False):
    """Haqiqiy modellar bilan ``AvtoTestBuilder`` (signallar, admin va management buyruqlari uçun)."""
    from django.conf import settings

    from projects.models import AvtoTest
    from tests.models import Answers, Books, Questions, Topics

    static_root = Path(settings.BASE_DIR) / "static"
    return AvtoTestBuilder(AvtoTest, Books, Topics, Questions, Answers, static_root, settings.MEDIA_ROOT, dry_run=dry_run)


def tests_question(bilet, raqam):
    """AvtoTest (bilet, raqam) -> tests'dagi asosiy savol (bölmasa None)."""
    from tests.models import Questions

    book_id, number = book_for(bilet)
    if book_id is None:
        return None
    return (
        Questions.objects.filter(topic__book_id=book_id, topic__number=number, topic__is_deleted=False,
                                 number=raqam, is_deleted=False)
        .order_by("topic_id", "id").first()
    )


# ================================================================================================
# AvtoTest -> tests (bir martalik tozalaş, faqat migratsiya 0017)
# ================================================================================================
def _assign(obj, values, uz_pairs=()):
    """Faqat özgargan maydonlarni yozadi. ``uz_pairs`` — (lotin, kirill) maydonlar:
    kirill faqat lotin matn özgarganda yoki böş bölsa qayta hosil qilinadi (qölda tuzatilgani saqlansin)."""
    changed = []
    for lat, cyr in uz_pairs:
        new = values.get(lat, "")
        if getattr(obj, lat) != new or not getattr(obj, cyr):
            values[cyr] = _cyr(new)
        else:
            values.pop(cyr, None)
    for field, value in values.items():
        if getattr(obj, field) != value:
            setattr(obj, field, value)
            changed.append(field)
    return changed


class TestsBootstrap(_Base):
    STATS = (
        "topics_created", "topics_hidden", "questions_created", "questions_updated", "questions_hidden",
        "answers_created", "answers_updated", "answers_hidden",
    )

    def __init__(self, AvtoTest, Books, Topics, Questions, Answers, static_root=None, media_root=None, dry_run=False):
        super().__init__(dry_run)
        self.AvtoTest, self.Books, self.Topics = AvtoTest, Books, Topics
        self.Questions, self.Answers = Questions, Answers
        self.static_root, self.media_root = static_root, media_root
        self._books = {}

    def _save(self, obj, fields, stat, extra=("updated_at",)):
        super()._save(obj, fields, stat, extra)

    def _hide(self, obj, stat):
        self.stats[stat] += 1
        if not self.dry_run:
            obj.is_deleted = True
            obj.save(update_fields=["is_deleted", "updated_at"])

    def _book(self, book_id):
        if book_id not in self._books:
            self._books[book_id] = self.Books.objects.filter(id=book_id).first()
        return self._books[book_id]

    def sync_all(self):
        bilets = sorted(set(self.AvtoTest.objects.values_list("bilet", flat=True)))
        for bilet in bilets:
            self.sync_bilet(bilet)
        # AvtoTest'da yöq biletlar tests'da ham yaşirilsin
        for book_id, first in SYNCED_BOOKS:
            for topic in self.Topics.objects.filter(book_id=book_id, is_deleted=False):
                bilet = bilet_for(book_id, topic.number)
                if bilet and bilet not in bilets:
                    self.sync_bilet(bilet)
        return self.stats

    def sync_bilet(self, bilet):
        book_id, number = book_for(bilet)
        book = self._book(book_id) if book_id else None
        if book is None:
            return self.stats
        rows = list(self.AvtoTest.objects.filter(bilet=bilet).order_by("raqam", "id"))
        topic = self.Topics.objects.filter(book_id=book_id, number=number, is_deleted=False).order_by("id").first()
        if topic is None:
            if not rows:
                return self.stats
            topic = self._create(
                self.Topics, "topics_created",
                number=number, sort_order=number, book_id=book_id, group_id=book.group_id, type_id=book.type_id,
                created_by_id=book.created_by_id, name_uz_uz=f"{number}-bilet", name_uz_crl=f"{number}-билет",
                name_ru_ru=f"{number}-й билет", name_en_us=f"Ticket {number}",
            )
        common = {"book_id": book_id, "group_id": book.group_id, "type_id": book.type_id, "created_by_id": book.created_by_id}

        existing = {}
        if topic.pk:
            for q in self.Questions.objects.filter(topic_id=topic.pk, is_deleted=False).order_by("number", "id"):
                if q.number in existing:
                    self._hide(q, "questions_hidden")  # bir xil raqamli ikkinçi nusxa
                else:
                    existing[q.number] = q

        seen = set()
        for row in rows:
            if row.raqam in seen:
                continue
            seen.add(row.raqam)
            self._sync_question(row, topic, existing.pop(row.raqam, None), common)
        for question in existing.values():  # AvtoTest'da yöq savollar
            self._hide(question, "questions_hidden")
        if not rows and topic.pk:  # bilet butunlay öçirilgan — /tests/ da böş bilet qolmasin
            self._hide(topic, "topics_hidden")
        return self.stats

    def _sync_question(self, row, topic, question, common):
        if row.rasm and self.static_root and self.media_root and not self.dry_run:
            _copy(Path(self.static_root) / "avtotest" / row.rasm, Path(self.media_root) / IMAGE_DIR / row.rasm)
        values = {
            "number": row.raqam,
            "name_uz_uz": row.savol or "",
            "name_ru_ru": row.savol_ru or "",
            "name_en_us": row.savol_en or "",
            "image": f"{IMAGE_DIR}/{row.rasm}" if row.rasm else "",
            "explanation_uz_uz": row.izoh or "",
            "explanation_ru_ru": row.izoh_ru or "",
            "explanation_en_us": row.izoh_en or "",
            "explanation_status": row.izoh_holati or "",
            "explanation_confidence": row.izoh_ishonch or "",
        }
        pairs = (("name_uz_uz", "name_uz_crl"), ("explanation_uz_uz", "explanation_uz_crl"))
        if question is None:
            values["name_uz_crl"] = _cyr(values["name_uz_uz"])
            values["explanation_uz_crl"] = _cyr(values["explanation_uz_uz"])
            question = self._create(
                self.Questions, "questions_created", topic_id=topic.pk, sort_order=row.raqam, **common, **values
            )
        else:
            values.update(topic_id=topic.pk, book_id=common["book_id"], group_id=common["group_id"],
                          type_id=common["type_id"])
            self._save(question, _assign(question, values, pairs), "questions_updated")
        self._sync_answers(row, question, topic, common)

    def _sync_answers(self, row, question, topic, common):
        options = []
        for letter in LETTERS.lower():
            uz = (getattr(row, f"javob_{letter}") or "").strip()
            if uz:
                options.append((
                    letter.upper(), uz,
                    (getattr(row, f"javob_{letter}_ru") or "").strip(),
                    (getattr(row, f"javob_{letter}_en") or "").strip(),
                ))
        answers = []
        if question.pk:
            answers = list(self.Answers.objects.filter(question_id=question.pk, is_deleted=False).order_by("number", "id"))
        for i, (letter, uz, ru, en) in enumerate(options):
            values = {
                "number": i + 1, "name_uz_uz": uz, "name_ru_ru": ru, "name_en_us": en,
                "right": letter == row.javob, "image": "",
            }
            if i < len(answers):
                values.update(topic_id=topic.pk, book_id=common["book_id"], group_id=common["group_id"],
                              type_id=common["type_id"])  # eski qatorlarda böş qolgan bölişi mumkin
                self._save(answers[i], _assign(answers[i], values, (("name_uz_uz", "name_uz_crl"),)), "answers_updated")
            else:
                values["name_uz_crl"] = _cyr(uz)
                self._create(
                    self.Answers, "answers_created",
                    question_id=question.pk, topic_id=topic.pk, sort_order=0, **common, **values,
                )
        for extra in answers[len(options):]:
            self._hide(extra, "answers_hidden")
