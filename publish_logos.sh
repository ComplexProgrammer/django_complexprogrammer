#!/usr/bin/env bash
# Complex Programmer (complexprogrammer.uz) yangi logotiplarini serverda joriy qiliş
# va Disk Quota (Errno 122) muammosining oldini oliş skripti.
# Işlatiş:
#   bash publish_logos.sh            # Standart: Cyber-Knight C0mplex uslubi
#   bash publish_logos.sh monogram   # Minimalist <CP> Monogram uslubi

set -e

STYLE="${1:-knight}"

echo "========================================================================"
echo "🚀 Complex Programmer (complexprogrammer.uz) logotiplarini yangilaş..."
echo "📌 Tanlangan uslub: $STYLE"
echo "========================================================================"

# 1. Avval disk kvotasini töldirib qöyadigan ortiqça dublikat/keş papkalarini tozalaymiz
# Eslatma: Loyihada WHITENOISE_USE_FINDERS=True yoqilgan, şuning uçun collectstatic
# qiliş şart emas (collectstatic butun static/ va media/ papkalaridan nusxa olib diskni töldirib qöyadi!).
rm -rf staticfiles
mkdir -p staticfiles
rm -rf tmp/django_cache/*
rm -rf media/projects/backups media/post/backups static/img/backups_logos_*
rm -rf ~/.cache/pip 2>/dev/null || true

if command -v python3 >/dev/null 2>&1; then
    PYTHON_CMD="python3"
else
    PYTHON_CMD="python"
fi

$PYTHON_CMD publish_logos.py --style "$STYLE"

mkdir -p tmp
touch tmp/restart.txt
echo "✅ Disk tozalandi, logotiplar joriy qilindi va server qayta işga tuşirildi (tmp/restart.txt)!"
