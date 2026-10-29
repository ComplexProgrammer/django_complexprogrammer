"""Bazadagi barça özbekça matnlarni 2026-yilgi yangi lotin alifbosiga (Ş, Ç, Ğ, Ö) ötkaziş.

Uşbu buyruq ma’lumotlar bazasidagi barça tegişli modellar (Blog, Avtotest, Loyihalar,
Testlar, Yangiliklar, Izohlar, Bozorlar va h.k.) maydonlarini tahlil qilib, 1995-yilgi
lotin harf birikmalarini (sh, ch, o', g') 2026-yilgi isloh qilingan harflarga (ş, ç, ö, ğ)
xavfsiz ötkazadi.

Işlatiş:
    python manage.py migrate_db_to_2026           # Tekşiriş (Dry-run: bazaga tegilmaydi)
    python manage.py migrate_db_to_2026 --dry-run # Tekşiriş (Dry-run rejimida natijalarni köriş)
    python manage.py migrate_db_to_2026 --apply   # Haqiqiy saqlaş (Bazaga yozadi)
    python manage.py migrate_db_to_2026 --model posts --apply  # Faqat bitta modelni yangilaş
"""

import os
import sys
import time

try:
    from django.core.management.base import BaseCommand
    from django.db import transaction
    from django.core.cache import cache
except ImportError:
    class BaseCommand:
        pass
    transaction = None
    cache = None


class Command(BaseCommand):
    help = "Bazadagi barça özbekça matnlarni 2026-yilgi yangi lotin alifbosiga ötkaziş."

    def add_arguments(self, parser):
        parser.add_argument(
            "--apply",
            action="store_true",
            help="Özgarişlarni haqiqatda bazaga saqlaş (batafsil saqlaş rejimida)",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Bazaga yozmasdan, qaysi yozuvlar özgarişini körsatuvçi tekşiruv rejimi",
        )
        parser.add_argument(
            "--model",
            type=str,
            default="",
            help="Faqat bitta modelni qayta işlaş (masalan: posts, avtotest, questions, comments)",
        )
        parser.add_argument(
            "--batch-size",
            type=int,
            default=200,
            help="Har bir paketdagi yozuvlar soni (standart: 200)",
        )

    def handle(self, *args, **options):
        from core.translit import latin1995_to_2026

        is_apply = bool(options.get("apply"))
        is_dry_run = not is_apply or bool(options.get("dry_run"))
        batch_size = options.get("batch_size") or 200
        filter_model = (options.get("model") or "").strip().lower()

        mode_str = "HAYOTIY REJIM (--apply)" if is_apply else "TEKŞIRUV REJIMI (DRY-RUN, bazaga tegilmaydi)"
        self.stdout.write(self.style.SUCCESS("=" * 72))
        self.stdout.write(self.style.SUCCESS(f"  ALIFBO REFORMASI 2026: MA’LUMOTLAR BAZASINI YANGILAŞ"))
        self.stdout.write(self.style.SUCCESS(f"  Holat: {mode_str}"))
        self.stdout.write(self.style.SUCCESS("=" * 72))

        # Model konfiguratsiyalari: (nomi, model_yöli, tekşiriladigan_maydonlar)
        TARGETS = [
            # 1. Blog
            ("blog.Categories", "blog.models.Categories", ["name_uz_uz"]),
            ("blog.Posts", "blog.models.Posts", ["name_uz_uz", "title_uz_uz", "body_uz_uz", "seo_title", "seo_description"]),

            # 2. Loyihalar va Avtotest
            ("projects.Project", "projects.models.Project", ["title", "sub_title", "category"]),
            ("projects.AvtoTest", "projects.models.AvtoTest", ["savol", "javob_a", "javob_b", "javob_c", "javob_d", "izoh"]),

            # 3. Testlar va yöl belgilari
            ("tests.BookTypes", "tests.models.BookTypes", ["name_uz_uz", "description"]),
            ("tests.Types", "tests.models.Types", ["name_uz_uz"]),
            ("tests.Groups", "tests.models.Groups", ["name_uz_uz"]),
            ("tests.Topics", "tests.models.Topics", ["name_uz_uz"]),
            ("tests.Books", "tests.models.Books", ["name_uz_uz"]),
            ("tests.Questions", "tests.models.Questions", ["name_uz_uz", "explanation_uz_uz"]),
            ("tests.Answers", "tests.models.Answers", ["name_uz_uz"]),
            ("tests.RoadSignCategories", "tests.models.RoadSignCategories", ["name_uz_uz"]),
            ("tests.RoadSigns", "tests.models.RoadSigns", ["name_uz_uz", "description_uz_uz"]),
            ("tests.QuestionExplanation", "tests.models.QuestionExplanation", ["explanation"]),

            # 4. Yangiliklar
            ("news.Posts", "news.models.Posts", ["name_uz_uz", "title_uz_uz", "body_uz_uz"]),

            # 5. Bozorlar
            ("markets.Category", "markets.models.Category", ["name_uz_uz"]),
            ("markets.Market", "markets.models.Market", ["name_uz_uz"]),
            ("markets.Store", "markets.models.Store", ["name_uz_uz"]),
            ("markets.Product", "markets.models.Product", ["name_uz_uz", "description_uz_uz"]),

            # 6. Izohlar
            ("comments.Comment", "comments.models.Comment", ["text"]),
        ]

        total_checked = 0
        total_modified = 0
        start_time = time.time()

        for label, import_path, fields in TARGETS:
            short_name = label.split(".")[-1].lower()
            if filter_model and filter_model not in short_name and filter_model not in label.lower():
                continue

            try:
                mod_name, cls_name = import_path.rsplit(".", 1)
                mod = __import__(mod_name, fromlist=[cls_name])
                model_cls = getattr(mod, cls_name)
            except Exception as exc:
                self.stdout.write(self.style.WARNING(f"⚠️ {label} modelini yuklab bölmadi: {exc}"))
                continue

            self.stdout.write(f"\n📂 Model tekşirilmoqda: {self.style.SUCCESS(label)} (maydonlar: {', '.join(fields)})")

            qs = model_cls.objects.all()
            model_total = qs.count()
            total_checked += model_total

            model_modified = 0
            sample_changes = []

            # Paketlab qayta işlaş
            records_to_update = []

            for obj in qs.iterator(chunk_size=batch_size):
                obj_changed = False
                for field_name in fields:
                    if not hasattr(obj, field_name):
                        continue
                    old_val = getattr(obj, field_name)
                    if not old_val or not isinstance(old_val, str):
                        continue

                    new_val = latin1995_to_2026(old_val)
                    if new_val != old_val:
                        setattr(obj, field_name, new_val)
                        obj_changed = True
                        if len(sample_changes) < 2:
                            sample_changes.append({
                                "id": getattr(obj, "id", getattr(obj, "pk", "")),
                                "field": field_name,
                                "old": old_val[:80].replace("\n", " "),
                                "new": new_val[:80].replace("\n", " "),
                            })

                if obj_changed:
                    model_modified += 1
                    total_modified += 1
                    if is_apply:
                        records_to_update.append(obj)
                        if len(records_to_update) >= batch_size:
                            self._save_batch(model_cls, records_to_update, fields)
                            records_to_update = []

            if is_apply and records_to_update:
                self._save_batch(model_cls, records_to_update, fields)

            status_style = self.style.SUCCESS if model_modified else getattr(self.style, "NOTICE", self.style.WARNING)
            self.stdout.write(status_style(
                f"   Jami yozuvlar: {model_total} ta | Yangilanişi kerak: {model_modified} ta"
            ))

            for s in sample_changes:
                self.stdout.write(f"   ↳ [ID {s['id']} / {s['field']}]:")
                self.stdout.write(f"      Eski: {s['old']}")
                self.stdout.write(f"      Yangi: {s['new']}")

        elapsed = round(time.time() - start_time, 2)
        self.stdout.write("\n" + "=" * 72)
        if is_apply:
            try:
                if cache:
                    cache.clear()
            except Exception:
                pass
            if os.path.isdir("tmp"):
                try:
                    restart_file = os.path.join("tmp", "restart.txt")
                    with open(restart_file, "a"):
                        os.utime(restart_file, None)
                    self.stdout.write("🔄 tmp/restart.txt yangilandi.")
                except Exception:
                    pass
            self.stdout.write(self.style.SUCCESS(
                f"✅ YAKUNLANDI! {total_modified} ta yozuv muvaffaqiyatli 2026-yilgi alifboga ötkazildi ({elapsed} soniya)."
            ))
        else:
            self.stdout.write(self.style.WARNING(
                f"ℹ️ TEKŞIRUV YAKUNLANDI (DRY-RUN)! {total_checked} ta yozuv tekşirildi, {total_modified} ta yozuvda özgariş aniqlandi."
            ))
            self.stdout.write(self.style.WARNING(
                f"👉 Haqiqatda bazaga saqlaş uçun buyruqqa --apply parametrini bering:"
            ))
            self.stdout.write(self.style.SUCCESS(
                f"   python manage.py migrate_db_to_2026 --apply"
            ))
        self.stdout.write("=" * 72)

    def _save_batch(self, model_cls, records, fields):
        try:
            # bulk_update tezroq
            model_cls.objects.bulk_update(records, fields)
        except Exception:
            # Fallback agar bulk_update qandaydir sabab bilan çeklangan bölsa
            for r in records:
                r.save(update_fields=fields)
