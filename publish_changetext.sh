#!/bin/bash
# ==============================================================================
# "Lotin-kirill ögirgiç" maqolasini serverda rasmlari bilan birga naşr qiliş.
# Işlatiş:
#   bash publish_changetext.sh             # Naşr qiliş yoki yangilaş
#   bash publish_changetext.sh --draft     # Qoralama holatida saqlaş (2099-yil)
# ==============================================================================
set -e
cd "$(dirname "$0")"

# CloudLinux / cPanel thread limitini saqlash
export OPENBLAS_NUM_THREADS=1
export MKL_NUM_THREADS=1
export OMP_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1
export VECLIB_MAXIMUM_THREADS=1

PYTHON="${PYTHON:-python3}"

echo "============================================================"
echo "  Complex Programmer: Maqolani naşr qiliş skripti"
echo "  Maqola: Lotin-kirill ögirgiç (changetext)"
echo "============================================================"

# Maqola va rasmini nashr qilish
"$PYTHON" manage.py publish_changetext_post --update "$@"

# Passenger ilovasini qayta yuklash (keshlangan ma'lumotlar yangilanishi uchun)
if [ -d tmp ]; then
    touch tmp/restart.txt
    echo "🔄 Sayt yangilandi (tmp/restart.txt yaratildi)."
fi

echo "✨ Bajarildi!"
