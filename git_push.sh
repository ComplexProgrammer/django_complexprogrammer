#!/bin/bash
# Serverdagi barcha o'zgarishlarni (db.sqlite3 bilan) commit va push qilish.
# Ishlatish:  bash git_push.sh            yoki   bash git_push.sh "commit xabari"
# .env, logs/, *.pem, *.key, *-wal kabi fayllar .gitignore orqali chiqarib tashlanadi.
set -e
cd "$(dirname "$0")"

BRANCH="master"
MSG="${1:-server: $(date '+%Y-%m-%d %H:%M')}"
PYTHON="${PYTHON:-python3}"

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
if git diff --cached --quiet; then
    echo "Commit qilinadigan o'zgarish yo'q."
else
    git commit -m "$MSG"
fi

# GitHub'dagi yangi kodni olamiz. db.sqlite3 to'qnashsa, server nusxasi qoladi (-X ours).
BEFORE=$(git rev-parse HEAD)
git pull --no-rebase --no-edit -X ours origin "$BRANCH"
git push origin "$BRANCH"

if [ "$BEFORE" != "$(git rev-parse HEAD)" ]; then
    echo
    echo "GitHub'dan yangi o'zgarishlar keldi. Kerak bo'lsa:"
    echo "  $PYTHON manage.py migrate        # yangi migratsiyalar"
    echo "  touch tmp/restart.txt            # saytni qayta ishga tushirish (Passenger)"
    echo "  botni qayta ishga tushiring      # bot kodi o'zgargan bo'lsa"
fi
# Asosiy sahifalar ishlayaptimi (2026-10-10..12 dagi kabi uzilish sezilmay qolmasin)
"$PYTHON" manage.py smoke_check > /tmp/smoke_check.log 2>&1 && echo "Saytni tekshirish: hammasi joyida."     || { echo "⚠️  Ba'zi sahifalar xato bermoqda:"; grep -v "^OK" /tmp/smoke_check.log; }
echo "Tayyor."
