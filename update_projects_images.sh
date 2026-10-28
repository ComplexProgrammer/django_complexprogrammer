#!/bin/bash
# ==============================================================================
# Generatsiya qilingan öyin rasmlarini https://complexprogrammer.uz/projects/
# bölimidagi loyihalar uçun joriy qiliş skripti.
#
# Işlatiş:
#   bash update_projects_images.sh                  # Barça 8 ta öyin rasmini yangilaş
#   bash update_projects_images.sh --update-titles  # Rasmlar va sarlavhalarni yangilaş
#   bash update_projects_images.sh --dry-run        # Bazaga yozmasdan tekşiriş
#   bash update_projects_images.sh --game snake     # Faqat bitta öyin rasmini yangilaş
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
echo "  Complex Programmer: /projects/ öyin rasmlarini yangilaş"
echo "  Öyinlar: Snake, Car Racing, Duck Hunt, Motorcycle,"
echo "           Bubble Shooter, Ping Pong, Tic Tac Toe, Tetris"
echo "============================================================"

# Rasmlarni media/projects/images/ ga nusxalaş va Project modelida yangilaş
"$PYTHON" manage.py update_projects_game_images "$@"

# Passenger ilovasini qayta yuklaş (keşlangan ma'lumotlar yangilanişi uçun)
if [ -d tmp ]; then
    touch tmp/restart.txt
    echo "🔄 Sayt yangilandi (tmp/restart.txt yaratildi)."
fi

echo "✨ Bajarildi!"

