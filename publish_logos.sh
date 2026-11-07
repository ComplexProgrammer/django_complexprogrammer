#!/usr/bin/env bash
# Complex Programmer (complexprogrammer.uz) yangi logotiplarini serverda joriy qiliş skripti
# Işlatiş:
#   bash publish_logos.sh            # Standart: Cyber-Knight C0mplex uslubi
#   bash publish_logos.sh monogram   # Minimalist <CP> Monogram uslubi

set -e

STYLE="${1:-knight}"

echo "========================================================================"
echo "🚀 Complex Programmer (complexprogrammer.uz) logotiplarini yangilaş..."
echo "📌 Tanlangan uslub: $STYLE"
echo "========================================================================"

if command -v python3 >/dev/null 2>&1; then
    PYTHON_CMD="python3"
else
    PYTHON_CMD="python"
fi

$PYTHON_CMD publish_logos.py --style "$STYLE"

if [ -f "manage.py" ]; then
    echo "📦 Static fayllarni yiğilmoqda (collectstatic)..."
    $PYTHON_CMD manage.py collectstatic --noinput || true
fi

mkdir -p tmp
touch tmp/restart.txt
echo "✅ Server qayta işga tuşirildi (tmp/restart.txt) va logotiplar joriy qilindi!"

