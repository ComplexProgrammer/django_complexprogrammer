#!/bin/bash
# Serverdagi barcha o'zgarishlarni (db.sqlite3 bilan) commit va push qilish.
# Ishlatish:  bash git_push.sh            yoki   bash git_push.sh "commit xabari"
#             bash git_push.sh --auto     — cron uchun (pastga qarang)
# .env, logs/, *.pem, *.key, *-wal kabi fayllar .gitignore orqali chiqarib tashlanadi.
#
# --auto (cron) rejimi:
#   * bir vaqtda faqat bitta nusxa ishlaydi (oldingisi tugamagan bo'lsa — chiqib ketadi);
#   * hamma narsa logs/git_push.log ga yoziladi, cron email faqat xatoda keladi;
#   * faqat db.sqlite3 o'zgargan bo'lsa, u DB_MIN_MINUTES (standart 60) daqiqada bir martadan ko'p commit qilinmaydi —
#     aks holda har bir commit 20 MB lik baza nusxasini qo'shib, repo juda tez kattalashadi;
#   * push qiladigan narsa bo'lmasa GitHub'dan hech narsa tortilmaydi (kod o'z-o'zidan yangilanib qolmaydi).
#
# GitHub'dan yangi kod kelsa (ikkala rejimda): yangi migratsiyalar bölsa, baza nusxasi logs/ ga olinadi va
# `manage.py migrate` avtomatik bajariladi, söng tmp/restart.txt yangilanadi, keyin sahifalar tekşiriladi.
# projects/data/explanations/ ga yangi izoh fayli kelsa, `manage.py import_explanations` ham bajariladi.
#   cPanel → Cron Jobs (har 15 daqiqada):
#     */15 * * * * PYTHON=/home/<user>/virtualenv/.../bin/python bash /path/to/django/git_push.sh --auto
set -e
cd "$(dirname "$0")"

# CloudLinux / cPanel thread limitini saqlash (OpenBLAS 64 ta thread ochib NPROC limitiga urilmasligi uchun)
export OPENBLAS_NUM_THREADS=1
export MKL_NUM_THREADS=1
export OMP_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1
export VECLIB_MAXIMUM_THREADS=1

AUTO=0
if [ "$1" = "--auto" ]; then
    AUTO=1
    shift
fi

BRANCH="master"
MSG="${1:-server: $(date '+%Y-%m-%d %H:%M')}"
PYTHON="${PYTHON:-python3}"
DB_MIN_MINUTES="${DB_MIN_MINUTES:-60}"

if [ "$AUTO" = 1 ]; then
    mkdir -p logs
    if command -v flock >/dev/null; then
        exec 9>"logs/.git_push.lock"
        flock -n 9 || exit 0  # oldingi ishga tushirish hali davom etmoqda
    else
        # flock yo'q tizimlar uchun: papka yaratish atomar; 30 daqiqadan eski qulf (uzilib qolgan ishga tushirish) o'chiriladi
        find logs -maxdepth 1 -name .git_push.lockdir -mmin +30 -exec rmdir {} + 2>/dev/null || true
        mkdir logs/.git_push.lockdir 2>/dev/null || exit 0
        trap 'rmdir logs/.git_push.lockdir 2>/dev/null' EXIT
    fi
    exec 3>&2 >>logs/git_push.log 2>&1
    echo "===== $(date '+%Y-%m-%d %H:%M:%S') auto ====="
    # Xato bo'lsa cron email yuborishi uchun stderr'ga ham chiqaramiz
    trap 'echo "git_push.sh --auto xato bilan tugadi (qator $LINENO). Batafsil: logs/git_push.log" >&3' ERR
fi

# Bot bazani WAL rejimida ochadi: oxirgi yozuvlar db.sqlite3-wal da turadi (u git'ga kirmaydi).
# Commitdan oldin ularni asosiy faylga o'tkazamiz, aks holda eskirgan baza push qilinadi.
"$PYTHON" - <<'PY'
import sqlite3
conn = sqlite3.connect("db.sqlite3", timeout=30)
busy, log, done = conn.execute("PRAGMA wal_checkpoint(FULL)").fetchone()
conn.close()
print(f"WAL checkpoint: {done}/{log} sahifa" + (" (baza band — qisman)" if busy else ""))
PY

git add -A
if [ "$AUTO" = 1 ] && [ "$(git diff --cached --name-only)" = "db.sqlite3" ]; then
    LAST_DB=$(git log -1 --format=%ct -- db.sqlite3 2>/dev/null || echo 0)
    if [ $(( $(date +%s) - ${LAST_DB:-0} )) -lt $(( DB_MIN_MINUTES * 60 )) ]; then
        git reset -q -- db.sqlite3  # faylning o'zi tegilmaydi, faqat commitga kirmaydi
        echo "Faqat baza o'zgargan, oxirgi baza commitidan $DB_MIN_MINUTES daqiqa o'tmagan — keyingi safar."
        exit 0
    fi
fi
if git diff --cached --quiet; then
    echo "Commit qilinadigan o'zgarish yo'q."
else
    git commit -m "$MSG"
fi

if [ "$AUTO" = 1 ]; then
    git fetch -q origin "$BRANCH"
    if [ "$(git rev-list --count "origin/$BRANCH..HEAD")" = 0 ]; then
        echo "Push qilinadigan narsa yo'q."
        exit 0
    fi
fi

# GitHub'dagi yangi kodni olamiz. db.sqlite3 to'qnashsa, server nusxasi qoladi (-X ours).
BEFORE=$(git rev-parse HEAD)
git pull --no-rebase --no-edit -X ours origin "$BRANCH"
git push origin "$BRANCH"

PULLED=0
if [ "$BEFORE" != "$(git rev-parse HEAD)" ]; then
    PULLED=1
    echo
    echo "GitHub'dan yangi o'zgarishlar keldi."

    # Yangi migratsiyalar avtomatik qöllanadi: aks holda yangi kod bazada hali yöq ustunni söraydi va sahifalar
    # migrate qilinguncha xato beradi (2026-11-02: "no such column: comments_comment.status", 14 ta sahifa).
    if "$PYTHON" manage.py migrate --check > /dev/null 2>&1; then
        echo "Yangi migratsiya yöq."
    else
        # Migratsiyadan oldin bazaning nusxasi (WAL bilan birga, sqlite backup API orqali) — muammo bölsa qaytariş uçun
        mkdir -p logs
        BACKUP="logs/db_before_migrate_$(date '+%Y%m%d_%H%M%S').sqlite3"
        "$PYTHON" - "$BACKUP" <<'PY'
import sqlite3, sys
src = sqlite3.connect("db.sqlite3", timeout=30)
dst = sqlite3.connect(sys.argv[1])
src.backup(dst)
dst.close(); src.close()
PY
        echo "Baza nusxasi: $BACKUP"
        # Faqat oxirgi 5 ta nusxa saqlanadi (har biri ~20 MB)
        ls -1t logs/db_before_migrate_*.sqlite3 2>/dev/null | tail -n +6 | xargs -r rm -f
        if "$PYTHON" manage.py migrate --noinput; then
            echo "Migratsiyalar qöllandi."
        else
            echo "⚠️  migrate xato bilan tugadi! Bazani qaytariş: cp $BACKUP db.sqlite3"
            [ "$AUTO" = 1 ] && echo "⚠️  git_push.sh --auto: migrate xato berdi. Nusxa: $BACKUP. Batafsil: logs/git_push.log" >&3
        fi
    fi

    # Lokalda yaratilgan AI izoh qoralamalari (scripts/explanations_local.py) kelsa — bazaga yozamiz
    if git diff --name-only "$BEFORE" HEAD -- projects/data/explanations | grep -q .; then
        if "$PYTHON" manage.py import_explanations; then
            echo "Yangi izoh qoralamalari bazaga yozildi (Admin → Tests → Questions → Qoralama)."
        else
            echo "⚠️  import_explanations xato bilan tugadi."
            [ "$AUTO" = 1 ] && echo "⚠️  git_push.sh --auto: import_explanations xato berdi. Batafsil: logs/git_push.log" >&3
        fi
    fi
    # Passenger yangi kodni yuklasin
    mkdir -p tmp && touch tmp/restart.txt
    echo "Sayt qayta işga tuşirildi (tmp/restart.txt)."
    echo "Bot kodi (avtotest_bot/) özgargan bölsa, botni qöl bilan qayta işga tuşiring: bash restart_bot.sh"
fi
# Asosiy sahifalar ishlayaptimi (2026-10-10..12 dagi kabi uzilish sezilmay qolmasin).
# Avtomatik rejimda — faqat yangi kod kelganda (har 15 daqiqada saytga so'rov yubormaslik uchun).
if [ "$AUTO" = 0 ] || [ "$PULLED" = 1 ]; then
    "$PYTHON" manage.py smoke_check > /tmp/smoke_check.log 2>&1 && echo "Saytni tekshirish: hammasi joyida." \
        || { echo "⚠️  Ba'zi sahifalar xato bermoqda:"; grep -v "^OK" /tmp/smoke_check.log; [ "$AUTO" = 1 ] && grep -v "^OK" /tmp/smoke_check.log >&3; true; }
fi
echo "Tayyor."
