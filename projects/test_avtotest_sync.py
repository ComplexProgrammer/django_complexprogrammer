"""tests (kitob 49/50) -> AvtoTest sinxronlaşi va bir martalik AvtoTest -> tests tozalaşi.

projects/avtotest_sync.py va projects/signals.py.
"""
from django.contrib.auth.models import User
from django.test import TestCase

from projects.avtotest_sync import TestsBootstrap, bilet_for, book_for, builder
from projects.models import AvtoTest
from tests.models import Answers, Books, Groups, Questions, Topics, Types

NAMES = {"name_uz_uz": "x", "name_uz_crl": "x", "name_ru_ru": "x", "name_en_us": "x"}


def names(uz, ru="", en=""):
    return {"name_uz_uz": uz, "name_uz_crl": uz, "name_ru_ru": ru or uz, "name_en_us": en or uz}


class SyncTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="admin")
        t = Types.objects.create(created_by=self.user, **NAMES)
        g = Groups.objects.create(created_by=self.user, number=24, type=t, **NAMES)
        self.book49 = Books.objects.create(id=49, created_by=self.user, type=t, group=g)
        self.book50 = Books.objects.create(id=50, created_by=self.user, type=t, group=g)

    def topic(self, number, book=None):
        book = book or self.book49
        return Topics.objects.create(book=book, group=book.group, number=number, created_by=self.user, **NAMES)

    def question(self, topic, number, options=("Bir", "Ikki", "Uç"), right=2, **kw):
        q = Questions.objects.create(
            topic=topic, book=topic.book, number=number, created_by=self.user,
            **{**names(f"{topic.number}-{number} savol", "вопрос", "question"), **kw},
        )
        for i, text in enumerate(options, 1):
            self.answer(q, i, text, right=i == right)
        return q

    def answer(self, q, number, text, right=False, **kw):
        return Answers.objects.create(
            question=q, topic=q.topic, book=q.topic.book, number=number, right=right, created_by=self.user,
            **{**names(text), **kw},
        )


class BuilderTests(SyncTestCase):
    def test_book_mapping(self):
        self.assertEqual(book_for(1), (49, 1))
        self.assertEqual(book_for(108), (49, 108))
        self.assertEqual(book_for(109), (50, 1))
        self.assertEqual(bilet_for(50, 31), 139)
        self.assertEqual(bilet_for(49, 109), None)  # 49-kitobga tegişli emas
        self.assertEqual(bilet_for(7, 1), None)

    def test_builds_rows(self):
        with self.captureOnCommitCallbacks(execute=False):
            self.question(self.topic(1), 1, right=3, image="tests/questions/images/1_1.jpg")
            self.question(self.topic(2, self.book50), 4)
        builder().sync_all()
        row = AvtoTest.objects.get(bilet=1, raqam=1)
        self.assertEqual((row.savol, row.savol_ru, row.savol_en), ("1-1 savol", "вопрос", "question"))
        self.assertEqual((row.javob_a, row.javob_b, row.javob_c, row.javob_d), ("Bir", "Ikki", "Uç", ""))
        self.assertEqual((row.javob, row.rasm), ("C", "1_1.jpg"))
        self.assertEqual(AvtoTest.objects.get(bilet=110, raqam=4).javob, "B")

    def test_keeps_ids_and_deletes_removed(self):
        with self.captureOnCommitCallbacks(execute=False):
            q = self.question(self.topic(3), 1)
            gone = self.question(q.topic, 2)
            kept = AvtoTest.objects.create(bilet=3, raqam=1, savol="eski", javob="A")
            stale = AvtoTest.objects.create(bilet=3, raqam=9, savol="tests'da yöq", javob="A")
            gone.is_deleted = True
            gone.save()
        builder().sync_all()
        self.assertEqual(AvtoTest.objects.get(bilet=3, raqam=1).id, kept.id)
        self.assertEqual(AvtoTest.objects.get(id=kept.id).savol, "3-1 savol")
        self.assertFalse(AvtoTest.objects.filter(id=stale.id).exists())
        self.assertFalse(AvtoTest.objects.filter(bilet=3, raqam=2).exists())

    def test_invalid_question_keeps_old_row(self):
        with self.captureOnCommitCallbacks(execute=False):
            q = self.question(self.topic(4), 1, options=("a", "b", "c", "d", "e"))
            old = AvtoTest.objects.create(bilet=4, raqam=1, savol="eski", javob="B")
            two_right = self.question(q.topic, 2)
            self.answer(two_right, 4, "Yana", right=True)
        b = builder()
        b.sync_all()
        self.assertEqual(AvtoTest.objects.get(id=old.id).savol, "eski")
        self.assertFalse(AvtoTest.objects.filter(bilet=4, raqam=2).exists())
        self.assertEqual({(bilet, raqam) for bilet, raqam, _ in b.problems}, {(4, 1), (4, 2)})

    def test_missing_book_does_not_wipe_avtotest(self):
        with self.captureOnCommitCallbacks(execute=False):
            AvtoTest.objects.create(bilet=200, raqam=1, savol="s", javob="A")
            Books.objects.filter(id=50).delete()
        builder().sync_all()
        self.assertTrue(AvtoTest.objects.filter(bilet=200).exists())

    def test_idempotent(self):
        with self.captureOnCommitCallbacks(execute=False):
            self.question(self.topic(5), 1)
        builder().sync_all()
        stats = builder().sync_all()
        self.assertEqual(sum(stats.values()), 0, stats)

    def test_signals(self):
        topic = self.topic(6)
        with self.captureOnCommitCallbacks(execute=True):
            q = self.question(topic, 1)
        row = AvtoTest.objects.get(bilet=6, raqam=1)
        self.assertEqual(row.javob, "B")

        a, b = Answers.objects.filter(question=q).order_by("number")[:2]
        with self.captureOnCommitCallbacks(execute=True):
            b.right = False
            b.save()
            a.right = True
            a.name_uz_uz = "Yangi"
            a.save()
        row.refresh_from_db()
        self.assertEqual((row.javob, row.javob_a), ("A", "Yangi"))

        with self.captureOnCommitCallbacks(execute=True):  # biletni boşqa raqamga köçiriş
            topic.number = 7
            topic.save()
        self.assertFalse(AvtoTest.objects.filter(bilet=6).exists())
        self.assertTrue(AvtoTest.objects.filter(bilet=7, raqam=1).exists())

        with self.captureOnCommitCallbacks(execute=True):
            q.is_deleted = True
            q.save()
        self.assertFalse(AvtoTest.objects.filter(bilet=7).exists())


class BootstrapTests(SyncTestCase):
    """Migratsiya 0017: buzilgan tests nusxasi toza AvtoTest böyiça tiklanadi."""

    def bootstrap(self):
        return TestsBootstrap(AvtoTest, Books, Topics, Questions, Answers).sync_all()

    def test_repairs_mixed_answers_and_round_trips(self):
        with self.captureOnCommitCallbacks(execute=False):
            AvtoTest.objects.create(
                bilet=2, raqam=6, savol="2-6 savol", savol_ru="вопрос", savol_en="question",
                javob_a="Bir", javob_b="Ikki", javob_c="Uç", javob="B",
            )
            q = Questions.objects.create(topic=self.topic(2), book=self.book49, number=6, created_by=self.user, **NAMES)
            old = [self.answer(q, n, text, right=r) for n, text, r in
                   ((1, "Bir", False), (1, "Boşqa", True), (2, "Ikki", True), (2, "Yana", False), (3, "Uç", False))]
            self.bootstrap()
        live = list(Answers.objects.filter(question=q, is_deleted=False).order_by("number"))
        self.assertEqual([a.id for a in live], [a.id for a in old[:3]])
        self.assertEqual([(a.name_uz_uz, a.right) for a in live], [("Bir", False), ("Ikki", True), ("Uç", False)])
        self.assertEqual(Questions.objects.get(pk=q.pk).name_uz_crl, "2-6 савол")
        # Tozalangandan keyin teskari yönaliş heç narsani özgartirmasligi kerak
        self.assertEqual(sum(builder().sync_all().values()), 0)
