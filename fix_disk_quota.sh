#!/usr/bin/env bash
# Serverda "OSError: [Errno 122] Disk quota exceeded" va
# "UserWarning: No directory at: .../staticfiles/" xatoliklarini tezkor bartaraf etiş skripti.
#
# Işlatiş:
#   bash fix_disk_quota.sh          # staticfiles, keş, backup va pip keşlarini tozalaydi
#   bash fix_disk_quota.sh --all    # Yuqoridagilar + staged_banners papkalarini ham tozalaydi

set -e

echo "========================================================================"
echo "🧹 Server disk kvotasi (Errno 122) va keşni tozalaş boşlandi..."
echo "========================================================================"

echo "📊 Tozalaşdan oldingi holat:"
df -h . 2>/dev/null || true
quota -s 2>/dev/null || true
echo "------------------------------------------------------------------------"

# 1. collectstatic yaratgan ulkan staticfiles/ dublikat papkasini öçirib, böş papka yaratamiz
# (WhiteNoise "No directory at: .../staticfiles/" ogohlantirişini çiqarmasligi uçun böş papka qoladi)
if [ -d "staticfiles" ]; then
    echo "🗑  staticfiles/ içidagi ortiqça nusxalar öçirilmoqda..."
    rm -rf staticfiles
fi
mkdir -p staticfiles

# 2. Django fayl keşi (tmp/django_cache) tozalanadi
echo "🗑  tmp/django_cache/ tozalanmoqda..."
rm -rf tmp/django_cache
mkdir -p tmp/django_cache tmp/django_cache_durable

# 3. Banner va logotip skriptlarining eski backup papkalarini öçiramiz
echo "🗑  Eski zaxira (backups) papkalari tozalanmoqda..."
rm -rf media/projects/backups media/post/backups
rm -rf static/img/backups_logos_* media/projects/images/backups_* media/post/images/backups_*

# 4. Pip va Python __pycache__ keşlarini tozalaymiz
echo "🗑  ~/.cache/pip va __pycache__ tozalanmoqda..."
rm -rf ~/.cache/pip 2>/dev/null || true
find . -type d -name "__pycache__" -prune -exec rm -rf {} + 2>/dev/null || true

# 5. Agar --all berilgan bölsa va bannerlar allaqaçon joriy qilingan bölsa, staged papkalarni ham öçiradi
if [ "${1:-}" = "--all" ]; then
    echo "🗑  Staged banner papkalari (media/projects/staged_banners, media/post/staged_health_banners) tozalanmoqda..."
    rm -rf media/projects/staged_banners media/post/staged_health_banners
fi

mkdir -p tmp
touch tmp/restart.txt

echo "------------------------------------------------------------------------"
echo "📊 Tozalaşdan keyingi holat:"
df -h . 2>/dev/null || true
quota -s 2>/dev/null || true
echo "========================================================================"
echo "✅ Muammo bartaraf etildi va Passenger qayta işga tuşirildi (tmp/restart.txt)!"
