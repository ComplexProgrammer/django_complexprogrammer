#!/bin/bash
# YouTube yuklovchi (yt-dlp) ni yangilash. YouTube saytini tez-tez o'zgartiradi — eski yt-dlp ishlamay qoladi.
# Ishlatish:  bash update_ytdlp.sh
#
# Nima qiladi:
#   * yt-dlp ni oxirgi versiyaga yangilaydi; imageio-ffmpeg (video+audio birlashtirish, MP3) yo'q bo'lsa — o'rnatadi;
#   * versiya o'zgargan bo'lsagina saytni qayta ishga tushiradi (tmp/restart.txt) — aks holda saytga tegmaydi;
#   * serverdan YouTube ochilishini qisqa sinov bilan tekshirib, natijani logga yozadi
#     (Hetzner kabi data-markaz IP'larini YouTube "Sign in to confirm you're not a bot" deb bloklashi mumkin);
#   * hamma narsa logs/update_ytdlp.log ga yoziladi, cron email faqat xatoda keladi.
#
# cPanel → Cron Jobs (har kuni 04:30):
#   30 4 * * * PYTHON=/home/<user>/virtualenv/.../bin/python bash /path/to/django/update_ytdlp.sh
set -e
cd "$(dirname "$0")"

# CloudLinux / cPanel thread limitini saqlash
export OPENBLAS_NUM_THREADS=1
export MKL_NUM_THREADS=1
export OMP_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1
export VECLIB_MAXIMUM_THREADS=1

PYTHON="${PYTHON:-python3}"
LOG="logs/update_ytdlp.log"
TEST_URL="https://youtu.be/jNQXAC9IVRw"  # 19 soniyalik "Me at the zoo" — YouTube'dagi birinchi video, o'chirilmaydi

mkdir -p logs tmp
# Bir vaqtda faqat bitta nusxa (oldingisi tugamagan bo'lsa — chiqib ketadi)
if command -v flock >/dev/null; then
    exec 9>"logs/.update_ytdlp.lock"
    flock -n 9 || exit 0
fi
exec 3>&2 >>"$LOG" 2>&1
echo "===== $(date '+%Y-%m-%d %H:%M:%S') ====="
# Xato bo'lsa cron email yuborishi uchun stderr'ga ham chiqaramiz
trap 'echo "update_ytdlp.sh xato bilan tugadi (qator $LINENO). Batafsil: $LOG" >&3' ERR

version() {
    "$PYTHON" -c "import yt_dlp; print(yt_dlp.version.__version__)" 2>/dev/null || echo "yo'q"
}

fail() {
    echo "XATO: $1"
    echo "update_ytdlp.sh: $1. Batafsil: $LOG" >&3
    exit 1
}

# PyPI'dagi oxirgi versiya. pip ulana olmasa ham (paket allaqachon o'rnatilgan bo'lsa) 0 bilan tugaydi —
# shuning uchun natijani alohida tekshiramiz, aks holda eskirgan yt-dlp haqida hech kim bilmay qoladi
LATEST=$("$PYTHON" -m pip index versions yt-dlp --disable-pip-version-check 2>/dev/null | sed -n 's/^yt-dlp (\(.*\))$/\1/p')
[ -n "$LATEST" ] || fail "PyPI'ga ulanib bo'lmadi — yt-dlp yangilanmadi"

OLD=$(version)
# [default]: yt-dlp-ejs — YouTube'ning kirilgan (cookie) klientlari uchun JavaScript
"$PYTHON" -m pip install -q --disable-pip-version-check -U "yt-dlp[default]"
# deno — o'sha JavaScript'ni bajaradigan runtime. glibc 2.27 dan eski tizimda o'rnatilmaydi:
# xato yt-dlp yangilanishini to'xtatmasin, faqat logga yozilsin (o'rniga node ishlatish mumkin — YTDLP_NODE)
"$PYTHON" -m pip install -q --disable-pip-version-check -U deno     || echo "OGOHLANTIRISH: deno o'rnatilmadi (glibc: $(ldd --version 2>/dev/null | head -1)). Node yo'lini .env dagi YTDLP_NODE ga yozing"
if ! "$PYTHON" -c "import imageio_ffmpeg" 2>/dev/null; then
    echo "imageio-ffmpeg o'rnatilmoqda (birinchi marta, ~30 MB)..."
    "$PYTHON" -m pip install -q --disable-pip-version-check imageio-ffmpeg
fi
NEW=$(version)
[ "$NEW" = "$LATEST" ] || fail "yt-dlp $NEW, PyPI'da esa $LATEST — yangilab bo'lmadi"

if [ "$OLD" != "$NEW" ]; then
    # Passenger yangi yt-dlp ni faqat qayta ishga tushgach yuklaydi
    touch tmp/restart.txt
    echo "yt-dlp yangilandi: $OLD -> $NEW (sayt qayta ishga tushirildi)"
else
    echo "yt-dlp oxirgi versiyada: $NEW"
fi

# YouTube serverdan ochiladimi? Sayt ishlatadigan kod orqali (.env dagi YTDLP_COOKIES / YTDLP_PROXY bilan).
# Natija faqat logga yoziladi — cron xatosi hisoblanmaydi
"$PYTHON" manage.py shell -v 0 -c "
import os
from django.conf import settings
from projects import youtube_downloader as yd
used = []
if settings.YTDLP_COOKIES and os.path.isfile(settings.YTDLP_COOKIES):
    used.append('cookie fayli')
if settings.YTDLP_PROXY:
    used.append('proksi')
via = ' (' + ', '.join(used) + ' bilan)' if used else ' (cookie/proksisiz)'
try:
    info = yd.video_info('$TEST_URL')
    print('YouTube sinovi' + via + ': OK — ' + info['title'] + ', sifatlar: ' + str(info['heights']))
except Exception as exc:
    print('YouTube sinovi' + via + ': XATO — ' + str(exc)[:200])
    if getattr(exc, 'detail', ''):
        print('   sabab: ' + exc.detail[:400])
print('   JS runtime: ' + ', '.join(k + '=' + str(v.get('path', 'PATH')) for k, v in yd.js_runtimes().items()))
" 2>/dev/null || true
