#!/bin/bash
# Shishib ketgan .git papkasini kichraytirish: butun tarix tashlanadi, GitHub'dagi faqat oxirgi commit qoladi (--depth 1).
# git_push.sh har soatda 20 MB lik db.sqlite3 nusxasini commit qiladi, shuning uchun .git tez kattalashadi.
# Ishlatish:  bash git_compact.sh
# cPanel → Cron Jobs (har soatda; git_push.sh bilan bir daqiqaga tushmasligi uchun 7-daqiqada):
#   7 * * * * bash /path/to/django/git_compact.sh
#
# Xavfsizlik:
#   * git_push.sh bilan bitta qulfni (logs/.git_push.lock) ishlatadi — ikkalasi bir vaqtda ishlamaydi;
#   * ishchi fayllarga (db.sqlite3, .env, kod) tegilmaydi — `checkout -f` o'rniga faqat index qayta quriladi;
#   * yangi .git avval logs/.git_new da to'liq tayyorlanadi, keyin eskisi bilan almashtiriladi
#     (yuklab olish uzilsa, eski .git joyida qoladi);
#   * serverdagi HEAD GitHub'dagi master bilan bir xil bo'lmasa (push qilinmagan commit yoki tortilmagan kod) —
#     hech narsa qilinmaydi, git_push.sh sinxronlagandan keyin keyingi safar qayta uriniladi;
#   * .git GIT_MAX_MB (standart 400) dan kichik bo'lsa, hech narsa qilinmaydi (har soatda keraksiz yuklab olmaslik uchun).
#     Har safar majburan bajarish:  GIT_MAX_MB=0 bash git_compact.sh
set -e
cd "$(dirname "$0")"

BRANCH="master"
GIT_MAX_MB="${GIT_MAX_MB:-400}"
NEW=logs/.git_new
OLD=logs/.git_old
LOCKDIR=

mkdir -p logs
if command -v flock >/dev/null; then
    exec 9>"logs/.git_push.lock"
    flock -w 300 9 || exit 0  # git_push.sh ishlayapti va 5 daqiqada tugamadi — keyingi safar
else
    # flock yo'q tizimlar uchun git_push.sh dagi bilan bir xil qulf papkasi
    find logs -maxdepth 1 -name .git_push.lockdir -mmin +30 -exec rmdir {} + 2>/dev/null || true
    mkdir logs/.git_push.lockdir 2>/dev/null || exit 0
    LOCKDIR=logs/.git_push.lockdir
fi
cleanup() { rm -rf "$NEW"; [ -z "$LOCKDIR" ] || rmdir "$LOCKDIR" 2>/dev/null; true; }
trap cleanup EXIT

exec 3>&2 >>logs/git_compact.log 2>&1
echo "===== $(date '+%Y-%m-%d %H:%M:%S') ====="
# Xato bo'lsa cron email yuborishi uchun stderr'ga ham chiqaramiz
trap 'echo "git_compact.sh xato bilan tugadi (qator $LINENO). Batafsil: logs/git_compact.log" >&3' ERR

# Oldingi ishga tushirish ikki `mv` orasida uzilib qolgan bo'lsa — eski .git ni qaytaramiz
if [ ! -d .git ] && [ -d "$OLD" ]; then
    mv "$OLD" .git
    echo "Uzilib qolgan almashtirishdan eski .git qaytarildi."
fi
rm -rf "$NEW" "$OLD"

SIZE_MB=$(du -sm .git | cut -f1)
if [ "$SIZE_MB" -lt "$GIT_MAX_MB" ]; then
    echo ".git: ${SIZE_MB} MB (< ${GIT_MAX_MB} MB) — kichraytirish shart emas."
    exit 0
fi

# Yangi repo: eski config (remote URL va tokeni, upstream, user.name/email) ko'chiriladi
g() { git --git-dir="$NEW" --work-tree=. "$@"; }
git init -q --bare "$NEW"
cp .git/config "$NEW/config"
cp .git/info/exclude "$NEW/info/exclude" 2>/dev/null || true
g symbolic-ref HEAD "refs/heads/$BRANCH"
g fetch -q --depth 1 origin "+refs/heads/$BRANCH:refs/remotes/origin/$BRANCH"

TIP=$(g rev-parse "origin/$BRANCH")
HEAD_NOW=$(git rev-parse HEAD)
if [ "$TIP" != "$HEAD_NOW" ]; then
    echo "Serverdagi HEAD ($HEAD_NOW) GitHub'dagi $BRANCH ($TIP) bilan bir xil emas — git_push.sh sinxronlashini kutamiz."
    exit 0
fi

g update-ref "refs/heads/$BRANCH" "$TIP"
g reset -q  # index = oxirgi commit; ishchi fayllar o'zgarmaydi, commit qilinmagan o'zgarishlar saqlanadi

mv .git "$OLD"
if ! mv "$NEW" .git; then
    mv "$OLD" .git
    echo "Yangi .git ni joyiga qo'yib bo'lmadi — eskisi qaytarildi." >&3
    exit 1
fi
rm -rf "$OLD"

echo ".git: ${SIZE_MB} MB → $(du -sm .git | cut -f1) MB"
git status --short | head -20
echo "Tayyor."
