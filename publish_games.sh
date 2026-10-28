#!/bin/bash
# ==============================================================================
# Complex Programmer (/projects/) bölimidagi barça onlayn öyinlar maqolalarini
# serverda rasmlari bilan birga naşr qiliş skripti.
#
# Işlatiş:
#   bash publish_games.sh                  # Barça 8 ta maqolani naşr qiliş yoki yangilaş
#   bash publish_games.sh --draft          # Qoralama holatida saqlaş (2099-yil)
#   bash publish_games.sh --dry-run        # Bazaga yozmasdan tekşiriş
#   bash publish_games.sh --game tetris    # Faqat bitta öyin maqolasini naşr qiliş
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
echo "  Complex Programmer: Öyin maqolalarini naşr qiliş skripti"
echo "  Maqolalar: Snake, Car Racing, Duck Hunt, Motorcycle,"
echo "             Bubble Shooter, Ping Pong, Tic Tac Toe, Tetris"
echo "============================================================"

# Maqolalar va rasmlarini naşr qiliş
"$PYTHON" manage.py publish_games_posts --update "$@"

# Passenger ilovasini qayta yuklaş (keşlangan ma'lumotlar yangilanişi uçun)
if [ -d tmp ]; then
    touch tmp/restart.txt
    echo "🔄 Sayt yangilandi (tmp/restart.txt yaratildi)."
fi

echo "✨ Bajarildi!"

