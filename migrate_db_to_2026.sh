#!/bin/bash
# ==============================================================================
# Bazadagi barça özbekça matnlarni 2026-yilgi yangi lotin alifbosiga ötkaziş.
# Işlatiş:
#   bash migrate_db_to_2026.sh            # Tekşiriş (Dry-run: bazaga tegilmaydi)
#   bash migrate_db_to_2026.sh --dry-run  # Tekşiriş
#   bash migrate_db_to_2026.sh --apply    # Haqiqatda bazaga saqlaş
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
echo "  Complex Programmer: 2026 Alifbo Reformasi Baza Skripti"
echo "============================================================"

"$PYTHON" manage.py migrate_db_to_2026 "$@"

if [[ "$*" == *"--apply"* ]] && [ -d tmp ]; then
    touch tmp/restart.txt
    echo "🔄 Sayt yangilandi (tmp/restart.txt yaratildi)."
fi

echo "✨ Bajarildi!"

