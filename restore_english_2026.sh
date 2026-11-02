#!/bin/bash
# ==============================================================================
# 2026-yilgi alifboga xato ögirilgan inglizça sözlarni (Sçool, Şooter, Şe is...) tiklaş.
#
# Işlatiş (serverda):
#   bash restore_english_2026.sh            # Tekşiriş: nima özgarişini körsatadi, bazaga yozmaydi
#   bash restore_english_2026.sh --apply    # Bazaga saqlaş
# ==============================================================================
set -e
cd "$(dirname "$0")"

export OPENBLAS_NUM_THREADS=1
export MKL_NUM_THREADS=1
export OMP_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1
export VECLIB_MAXIMUM_THREADS=1

PYTHON="${PYTHON:-python3}"
"$PYTHON" manage.py restore_english_2026 "$@"

if [ "$1" = "--apply" ] && [ -d tmp ]; then
    touch tmp/restart.txt
    echo "🔄 Sayt yangilandi (tmp/restart.txt)."
fi
