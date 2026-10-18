"""Avtotest savollaridan Shorts / Reels / TikTok uchun 15 soniyalik vertikal videolar (1080×1920, MP4).

    python manage.py make_question_videos --limit 10            # tasodifiy 10 ta savol
    python manage.py make_question_videos --bilet 5             # 5-biletning barcha savollari
    python manage.py make_question_videos --mavzu chorrahalar   # mavzu bo'yicha

Natija: media/videos/<bilet>-<raqam>.mp4 va yonida .txt (video tavsifi + savol sahifasiga havola).
Tuzilishi: savol va variantlar + 8 soniyalik taymer -> to'g'ri javob yashil bilan belgilanadi.
Kerak: ``pip install imageio-ffmpeg`` (ichida tayyor ffmpeg bor).
"""

import subprocess
import textwrap
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from PIL import Image, ImageDraw, ImageFont

from driving import topics
from projects.models import AvtoTest

W, H, FPS = 1080, 1920, 15
QUESTION_SECONDS, ANSWER_SECONDS = 9, 6
FONT = Path(settings.BASE_DIR) / "driving" / "fonts" / "NotoSans.ttf"
IMAGES = Path(settings.BASE_DIR) / "static" / "avtotest"
OUT_DIR = Path(settings.MEDIA_ROOT) / "videos"
SITE = "complexprogrammer.uz"
LETTERS = ("A", "B", "C", "D")
BG, CARD, TEXT, MUTED, ACCENT, OK = (15, 23, 42), (30, 41, 59), (241, 245, 249), (148, 163, 184), (99, 102, 241), (34, 197, 94)


def _font(size, weight="Regular"):
    font = ImageFont.truetype(str(FONT), size)
    font.set_variation_by_name(weight)
    return font


def _wrap(draw, text, font, width):
    """Matnni piksel kengligi bo'yicha qatorlarga bo'lish."""
    lines = []
    for paragraph in text.split("\n"):
        words, line = paragraph.split(), ""
        for word in words:
            candidate = f"{line} {word}".strip()
            if draw.textlength(candidate, font=font) <= width:
                line = candidate
            else:
                if line:
                    lines.append(line)
                line = word
        lines.append(line)
    return lines


def _base(q):
    """Savol, rasm va variantlar chizilgan kadr + har bir variantning to'rtburchagi."""
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    draw.text((60, 70), "AVTOTEST", font=_font(44, "Bold"), fill=ACCENT)
    draw.text((60, 130), f"{q.bilet}-bilet · {q.raqam}-savol", font=_font(36), fill=MUTED)

    y = 210
    if q.rasm and (IMAGES / q.rasm).is_file():
        with Image.open(IMAGES / q.rasm) as pic:
            pic = pic.convert("RGB")
            pic.thumbnail((W - 120, 620))
            img.paste(pic, ((W - pic.width) // 2, y))
            y += pic.height + 40

    font_q = _font(46, "SemiBold")
    for line in _wrap(draw, q.savol, font_q, W - 120)[:6]:
        draw.text((60, y), line, font=font_q, fill=TEXT)
        y += 60
    y += 30

    boxes = {}
    font_a = _font(38)
    for letter in LETTERS:
        answer = getattr(q, "javob_" + letter.lower())
        if not answer:
            continue
        lines = _wrap(draw, answer, font_a, W - 220)[:3]
        height = 40 + 50 * len(lines)
        boxes[letter] = (60, y, W - 60, y + height)
        draw.rounded_rectangle(boxes[letter], radius=24, fill=CARD)
        draw.text((90, y + 20), letter, font=_font(38, "Bold"), fill=ACCENT)
        for k, line in enumerate(lines):
            draw.text((150, y + 20 + 50 * k), line, font=font_a, fill=TEXT)
        y += height + 22
    return img, boxes


def _frames(q):
    base, boxes = _base(q)
    total = QUESTION_SECONDS * FPS
    for i in range(total):  # taymer: pastdagi chiziq qisqarib boradi
        frame = base.copy()
        draw = ImageDraw.Draw(frame)
        left = 1 - i / total
        draw.rounded_rectangle((60, H - 230, W - 60, H - 200), radius=15, fill=CARD)
        draw.rounded_rectangle((60, H - 230, 60 + int((W - 120) * left), H - 200), radius=15, fill=ACCENT)
        seconds = QUESTION_SECONDS - i // FPS
        draw.text((W // 2, H - 300), f"{seconds}", font=_font(64, "Bold"), fill=TEXT, anchor="mm")
        draw.text((W // 2, H - 120), SITE, font=_font(40, "SemiBold"), fill=MUTED, anchor="mm")
        yield frame
    answer = base.copy()
    draw = ImageDraw.Draw(answer)
    if q.javob in boxes:
        draw.rounded_rectangle(boxes[q.javob], radius=24, outline=OK, width=8)
    draw.text((W // 2, H - 270), "To'g'ri javob: " + q.javob, font=_font(56, "Bold"), fill=OK, anchor="mm")
    draw.text((W // 2, H - 120), f"Barcha savollar: {SITE}/avtotest", font=_font(38, "SemiBold"), fill=TEXT, anchor="mm")
    for _ in range(ANSWER_SECONDS * FPS):
        yield answer


def _ffmpeg():
    try:
        import imageio_ffmpeg
    except ImportError as e:
        raise CommandError("imageio-ffmpeg o'rnatilmagan: pip install imageio-ffmpeg") from e
    return imageio_ffmpeg.get_ffmpeg_exe()


class Command(BaseCommand):
    help = "Avtotest savollaridan 15 soniyalik vertikal videolar yasaydi (media/videos/)."

    def add_arguments(self, parser):
        parser.add_argument("--limit", type=int, default=10)
        parser.add_argument("--bilet", type=int)
        parser.add_argument("--mavzu", choices=sorted(topics.TOPIC_BY_SLUG))

    def handle(self, *args, **opts):
        ffmpeg = _ffmpeg()
        qs = AvtoTest.objects.filter(javob__in=LETTERS).exclude(savol="")
        if opts["bilet"]:
            qs = qs.filter(bilet=opts["bilet"]).order_by("raqam")
        else:
            if opts["mavzu"]:
                qs = qs.filter(id__in=topics.topic_map()[opts["mavzu"]])
            qs = qs.order_by("?")[: opts["limit"]]
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        for q in qs:
            out = OUT_DIR / f"{q.bilet}-{q.raqam}.mp4"
            proc = subprocess.Popen(
                [ffmpeg, "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                 "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "veryfast",
                 "-crf", "23", "-movflags", "+faststart", str(out)],
                stdin=subprocess.PIPE,
            )
            for frame in _frames(q):
                proc.stdin.write(frame.tobytes())
            proc.stdin.close()
            if proc.wait() != 0:
                raise CommandError(f"ffmpeg xatosi: {out}")
            url = f"https://{SITE}/avtotest/{q.bilet}/{q.raqam}/"
            caption = (
                f"{q.savol}\n\nJavobini 9 soniyada toping! ⏱\n\n"
                f"Izoh va barcha savollar: {url}\n20 savollik imtihon: https://{SITE}/avtotest/imtihon/\n\n"
                "#avtotest #prava #haydovchilik #yhq #avtotest2026"
            )
            out.with_suffix(".txt").write_text(caption, encoding="utf-8")
            self.stdout.write(self.style.SUCCESS(f"{out} ({out.stat().st_size // 1024} KB)"))
            self.stdout.write(textwrap.shorten(caption, 100))
