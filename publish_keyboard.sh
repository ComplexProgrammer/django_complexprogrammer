#!/bin/bash
# ==============================================================================
# "Yangi Özbek alifbosi klaviaturasi" maqolasini serverda naşr qiliş skripti.
# Işlatiş:
#   bash publish_keyboard.sh             # Naşr qiliş yoki yangilaş
#   bash publish_keyboard.sh --draft     # Qoralama holatida saqlaş (2099-yil)
#   bash publish_keyboard.sh --dry-run   # Bazaga yozmasdan tekşiriş
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
echo "  Complex Programmer: Maqolani naşr qiliş skripti"
echo "  Maqola: Yangi Özbek alifbosi klaviaturasi"
echo "============================================================"

# Maqola va rasmini naşr qiliş
"$PYTHON" manage.py publish_keyboard_post --update "$@"

# Passenger ilovasini qayta yuklaş (keşlangan ma'lumotlar yangilanişi uçun)
if [ -d tmp ]; then
    touch tmp/restart.txt
    echo "🔄 Sayt yangilandi (tmp/restart.txt yangilandi)."
fi

echo "✨ Bajarildi!"
