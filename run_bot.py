"""
@AvtoTestUzbBot ishga tushirish skripti.
Loyihaning asosiy papkasidan to'g'ridan-to'g'ri ishga tushirish uchun:
python run_bot.py
"""

import os
import sys
from pathlib import Path

# Thread limitlarini cheklash (CloudLinux / cPanel nproc limiti uchun)
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"
os.environ["VECLIB_MAXIMUM_THREADS"] = "1"

# Loyiha papkasini sys.path ga qo'shamiz
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from avtotest_bot.main import main

if __name__ == "__main__":
    main()
