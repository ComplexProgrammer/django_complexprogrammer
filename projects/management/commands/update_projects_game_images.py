"""Complex Programmer (/projects/) sahifasidagi barça onlayn öyinlar uçun generatsiya qilingan rasmlarni joriy qiliş buyruği.

Işlatiş:
    python manage.py update_projects_game_images                 # 8 ta öyin rasmini /projects/ uçun yangilaydi
    python manage.py update_projects_game_images --dry-run       # bazaga va fayllarga özgartiriş kiritmasdan tekşiradi
    python manage.py update_projects_game_images --update-titles # rasmlar bilan birga sarlavha/tavsiflarni ham yangilaydi
    python manage.py update_projects_game_images --game snake    # faqat bitta öyin rasmini yangilaydi
"""

import os
import shutil

PROJECT_GAMES = [
    {
        "key": "snake",
        "url": "snake",
        "src_image": "post/images/snake_online_game.jpg",
        "dest_image": "projects/images/snake_online_game.jpg",
        "category": "Web project",
        "title": "Snake — Ilon öyini",
        "sub_title": "20×20 maydon, 3 xil tezlik va 2 xil devor rejimiga ega klassik arkada",
        "application_id": "",
        "order": 10,
    },
    {
        "key": "car",
        "url": "car",
        "src_image": "post/images/car_racing_online_game.jpg",
        "dest_image": "projects/images/car_racing_online_game.jpg",
        "category": "Web and Mobile project",
        "title": "Car Racing — Avtopoyga",
        "sub_title": "3 polosali magistralda sport avtomobili poygasi va reaksiya sinovi",
        "application_id": "car.complexprogrammeruz",
        "order": 11,
    },
    {
        "key": "duckhunt",
        "url": "duckhunt",
        "src_image": "post/images/duck_hunt_online_game.jpg",
        "dest_image": "projects/images/duck_hunt_online_game.jpg",
        "category": "Web project",
        "title": "Duck Hunt — Ördak ovi",
        "sub_title": "10 ta ördakni eng qisqa soniyalarda urib tuşiriş böyiça merganlik öyini",
        "application_id": "",
        "order": 12,
    },
    {
        "key": "motorcycle",
        "url": "motorcycle",
        "src_image": "post/images/motorcycle_online_game.jpg",
        "dest_image": "projects/images/motorcycle_online_game.jpg",
        "category": "Web project",
        "title": "Motorcycle — Motokross",
        "sub_title": "Haqiqiy 2D fizika asosidagi tepaliklar va tramplinlar oşa mototsikl poygasi",
        "application_id": "",
        "order": 13,
    },
    {
        "key": "bubbleshooter",
        "url": "bubbleshooter",
        "src_image": "post/images/bubble_shooter_online_game.jpg",
        "dest_image": "projects/images/bubble_shooter_online_game.jpg",
        "category": "Web project",
        "title": "Bubble Shooter — Şarçalar",
        "sub_title": "6 xil rangdagi şarçalarni lazer möljal yordamida birlaştirib portlating",
        "application_id": "",
        "order": 14,
    },
    {
        "key": "pingpong",
        "url": "pingpong",
        "src_image": "post/images/ping_pong_online_game.jpg",
        "dest_image": "projects/images/ping_pong_online_game.jpg",
        "category": "Web project",
        "title": "Ping Pong — Stol tennisi",
        "sub_title": "Sun’iy intellektga qarşi 3 xil qiyinlik darajasida klassik stol tennisi",
        "application_id": "",
        "order": 15,
    },
    {
        "key": "tictactoe",
        "url": "tictactoe",
        "src_image": "post/images/tic_tac_toe_online_game.jpg",
        "dest_image": "projects/images/tic_tac_toe_online_game.jpg",
        "category": "Web project",
        "title": "Tic Tac Toe — X va O",
        "sub_title": "Yengilmas Minimax sun’iy intellekt yoki 2 kişilik rejimdagi mantiqiy öyin",
        "application_id": "",
        "order": 16,
    },
    {
        "key": "tetris",
        "url": "tetris",
        "src_image": "post/images/tetris_online_game.jpg",
        "dest_image": "projects/images/tetris_online_game.jpg",
        "category": "Web project",
        "title": "Tetris — Boşqotirma",
        "sub_title": "7-bag tizimi, SRS aylanma, Ghost va Hold imkoniyatli zamonaviy Tetris",
        "application_id": "",
        "order": 17,
    },
]


try:
    from django.core.management.base import BaseCommand, CommandError
except ImportError:
    class BaseCommand:
        pass

    class CommandError(Exception):
        pass


class Command(BaseCommand):
    help = "Generatsiya qilingan öyin rasmlarini https://complexprogrammer.uz/projects/ bölimidagi loyihalar uçun joriy qiliş."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Bazaga va fayl tizimiga özgartiriş kiritmasdan tekşiriş",
        )
        parser.add_argument(
            "--update-titles",
            action="store_true",
            help="Rasm bilan birga loyiha sarlavhasi (title) va qisqa tavsifini (sub_title) ham yangilaş",
        )
        parser.add_argument(
            "--game",
            type=str,
            default="",
            help="Faqat bitta öyin kaliti böyiça yangilaş (masalan: snake, tetris)",
        )

    def handle(self, *args, **opts):
        from django.conf import settings
        from django.core.cache import cache
        from projects.models import Project

        target = (opts.get("game") or "").strip().lower().strip("/")
        items = PROJECT_GAMES
        if target:
            items = [g for g in PROJECT_GAMES if g["key"] == target or g["url"] == target]
            if not items:
                valid = ", ".join(g["key"] for g in PROJECT_GAMES)
                raise CommandError(f"Öyin topilmadi: '{target}'. Mavjud öyinlar: {valid}")

        projects_img_dir = os.path.join(settings.MEDIA_ROOT, "projects", "images")
        if not opts["dry_run"]:
            os.makedirs(projects_img_dir, exist_ok=True)

        self.stdout.write(self.style.SUCCESS("=" * 68))
        self.stdout.write(
            self.style.SUCCESS(
                f"🖼 /projects/ bölimi uçun öyin rasmlarini yangilaş ({len(items)} ta öyin)"
            )
        )
        self.stdout.write(self.style.SUCCESS("=" * 68))

        updated_count = 0

        for idx, item in enumerate(items, start=1):
            key = item["key"]
            url_val = item["url"]
            src_rel = item["src_image"]
            dest_rel = item["dest_image"]

            src_full = os.path.join(settings.MEDIA_ROOT, src_rel)
            dest_full = os.path.join(settings.MEDIA_ROOT, dest_rel)

            if not os.path.exists(src_full) and not os.path.exists(dest_full):
                self.stdout.write(
                    self.style.WARNING(
                        f"⚠️ [{key}] Manba rasm topilmadi: {src_full}"
                    )
                )
                continue

            # Manba rasmni media/projects/images/ içiga nusxalaymiz
            if not opts["dry_run"] and os.path.exists(src_full):
                if os.path.abspath(src_full) != os.path.abspath(dest_full):
                    shutil.copy2(src_full, dest_full)

            url_variants = [url_val, f"{url_val}/", f"/{url_val}", f"/{url_val}/"]
            qs = Project.objects.filter(url__in=url_variants)

            if opts["dry_run"]:
                count = qs.count()
                old_imgs = [str(p.image) for p in qs] if count else ["(yangi yaratiladi)"]
                self.stdout.write(
                    self.style.SUCCESS(
                        f"[DRY-RUN] {idx}. {key.upper()} (url='{url_val}', topildi={count} ta)\n"
                        f"          Eski rasm: {', '.join(old_imgs)}\n"
                        f"          Yangi rasm: {dest_rel}"
                    )
                )
                updated_count += 1
                continue

            if qs.exists():
                for proj in qs:
                    old_img = str(proj.image)
                    proj.image = dest_rel
                    if opts["update_titles"]:
                        proj.title = item["title"]
                        proj.sub_title = item["sub_title"]
                    proj.save()
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"✅ [{idx}/{len(items)}] {proj.title} (id={proj.id}, url='/{proj.url}')\n"
                            f"   🔄 Eski rasm: {old_img}  ➔  Yangi rasm: {dest_rel}"
                        )
                    )
                updated_count += 1
            else:
                proj = Project.objects.create(
                    category=item["category"],
                    title=item["title"],
                    sub_title=item["sub_title"],
                    url=url_val,
                    application_id=item["application_id"],
                    image=dest_rel,
                    status=True,
                    is_service=False,
                    order=item["order"],
                )
                updated_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f"✅ [{idx}/{len(items)}] Yangi loyiha yaratildi: {proj.title} (id={proj.id}, url='/{proj.url}')\n"
                        f"   🖼 Rasm: {dest_rel}"
                    )
                )

        if not opts["dry_run"] and updated_count:
            try:
                cache.clear()
            except Exception:
                pass

        mode_label = "TEKŞIRUV (DRY-RUN)" if opts["dry_run"] else "JORIY QILINDI"
        self.stdout.write(self.style.SUCCESS("=" * 68))
        self.stdout.write(
            self.style.SUCCESS(
                f"✨ Yakunlandi! {updated_count} ta öyin rasmi /projects/ uçun tayyor ({mode_label})."
            )
        )
        self.stdout.write(self.style.SUCCESS("=" * 68))
