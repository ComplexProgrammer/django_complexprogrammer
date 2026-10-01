"""
@AvtoTestUzbBot ishga tushirish skripti.
Loyihaning asosiy papkasidan to'g'ridan-to'g'ri ishga tushirish uchun:
python run_bot.py
"""
import sys
from pathlib import Path

# Loyiha papkasini sys.path ga qo'shamiz
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from avtotest_bot.main import main

if __name__ == "__main__":
    main()
