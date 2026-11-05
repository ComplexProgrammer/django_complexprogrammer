#!/usr/bin/env bash
# ==============================================================================
# Salomatlik rukni (1-4 sahifalar, 31 ta maqola) bannerlarini serverda
# xavfsiz va tizimli yangilaş skripti.
# DIQQAT: Bazaga heç qanday özgariş kiritilmaydi (Zero-DB change).
# ==============================================================================

set -euo pipefail

# Server xotira va thread limitlari
export OPENBLAS_NUM_THREADS=1
export MKL_NUM_THREADS=1
export OMP_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1
export VECLIB_MAXIMUM_THREADS=1

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${SCRIPT_DIR}"

PYTHON_BIN="python"
if [ -f "/home/complex1/virtualenv/complexprogrammer.uz/django/3.12/bin/python" ]; then
    PYTHON_BIN="/home/complex1/virtualenv/complexprogrammer.uz/django/3.12/bin/python"
elif command -v python3 &>/dev/null; then
    PYTHON_BIN="python3"
fi

echo "========================================================================"
echo "  SALOMATLIK RUKNI BANNERLARINI ALMASHTIRİŞ (Zero-DB change)"
echo "  Python: ${PYTHON_BIN}"
echo "========================================================================"

"${PYTHON_BIN}" publish_health_banners.py "$@"
