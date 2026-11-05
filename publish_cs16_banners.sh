#!/bin/bash
# ==============================================================================
# CS 1.6 turkumi (pricel, FPS, headshot) maqolalariga yangi generatsiya
# qilingan banner rasmlarini serverda joriy qiliş skripti.
#
# Işlatiş:
#   bash publish_cs16_banners.sh             # Server bazasida rasmlarni yangilaş
#   bash publish_cs16_banners.sh --dry-run   # Bazaga yozmasdan tekşiriş
#   bash publish_cs16_banners.sh --status    # Hozirgi holatni tekşiriş
# ==============================================================================
set -e
cd "$(dirname "$0")"

# CloudLinux / cPanel thread limitini saqlaş
export OPENBLAS_NUM_THREADS=1
export MKL_NUM_THREADS=1
export OMP_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1
export VECLIB_MAXIMUM_THREADS=1

PYTHON="${PYTHON:-python3}"

echo "============================================================"
echo "  Complex Programmer: CS 1.6 Maqolalari Bannerlarini Yangilaş"
echo "  1. /blog/cs-16-pricel-sozlamalari/"
echo "  2. /blog/cs-16-fps-oshirish/"
echo "  3. /blog/cs-16-headshot-sozlamalari/"
echo "============================================================"

# Python skripti orqali bazadagi rasmlarni yangilaş
"$PYTHON" publish_cs16_banners.py "$@"

# Passenger ilovasini qayta yuklaş (keşlangan ma'lumotlar yangilanişi uçun)
if [ -d tmp ]; then
    touch tmp/restart.txt
    echo "🔄 Sayt yangilandi (tmp/restart.txt yangilandi)."
fi

echo "✨ Muvaffaqiyatli bajarildi!"

