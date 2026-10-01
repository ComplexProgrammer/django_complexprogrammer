import os
from pathlib import Path

# Loyihaning asosiy papkasi (django_complexprogrammer)
BASE_DIR = Path(__file__).resolve().parent.parent

# .env faylini xavfsiz o'qish funksiyasi
def load_env_file(env_path: Path):
    if not env_path.exists():
        return
    try:
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, val = line.split("=", 1)
                key = key.strip()
                val = val.strip().strip("'\"")
                if key not in os.environ:
                    os.environ[key] = val
    except Exception as e:
        print(f"[Config] .env yuklashda ogohlantirish: {e}")

# .env ni yuklash
load_env_file(BASE_DIR / ".env")

# Asosiy sozlamalar
BOT_TOKEN = os.getenv("AVTOTEST_BOT_TOKEN", "").strip()

# Admin Telegram ID lari
raw_admin_ids = os.getenv("AVTOTEST_ADMIN_IDS", "5656372773")
ADMIN_IDS = [int(i.strip()) for i in raw_admin_ids.split(",") if i.strip().isdigit()]

# Ma'lumotlar bazasi va media fayllar
DB_PATH = BASE_DIR / "db.sqlite3"
MEDIA_DIR = BASE_DIR / "media"

# Test kitoblari ID lari
UZB_AVTOTEST_BOOK_ID = 49   # Avto Test 2025 (108 bilet, 1080 savol)
E_AVTOMAKTAB_BOOK_ID = 50   # e-avtomaktab (305 savol)
CDL_USA_BOOK_ID = 1         # AQSh CDL testi (191 savol)

# Test rejimlari
BILET_QUESTIONS_COUNT = 10  # Har bir biletda 10 ta savol
EXAM_QUESTIONS_COUNT = 20   # Imtihonda 20 ta savol
PASSING_PERCENTAGE = 90     # O'tish bali (90%)
DEFAULT_LANG = "uz"         # Asosiy til
