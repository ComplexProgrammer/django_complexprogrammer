# 🚗 @AvtoTestUzbBot - Telegram Avtotest Boti

Ushbu bot **`django_complexprogrammer`** loyihasiga to'liq integratsiya qilingan bo'lib, loyihaning ma'lumotlar bazasidagi (`db.sqlite3`) va media papkasidagi (`media/`) barcha avtotest savollaridan foydalanadi.

---

## 🌟 Asosiy Imkoniyatlar

1. **🚗 108 ta bilet (1080 ta savol):**
   - Rasmiy O'zbekiston YHXBB (GAI) imtihon bazasi.
   - Har bir biletda 10 tadan savol.
   - Sahifalangan qulay inline klaviatura (Pagination).

2. **🎲 Tasodifiy Imtihon (Ekzamen):**
   - Rasmiy imtihon formatida 20 ta tasodifiy savol.
   - 90% o'tish bali (kamida 18 ta to'g'ri javob).

3. **🇺🇸 AQSh CDL haydovchilik testi:**
   - AQSh CDL haydovchilik imtihoni savollari (191 ta savol).

4. **❌ Xatolar ustida ishlash:**
   - Foydalanuvchi qaysi savollarda xato qilgan bo'lsa, bot bularni alohida saqlab boradi.
   - Faqat xato qilingan savollar bo'yicha alohida mashq o'tash imkoniyati.

5. **📸 Rasmli savollar qo'llab-quvvatlovi:**
   - Loyihaning `media/tests/questions/images/` papkasidagi rasmlar avtomatik yuklanadi va savol bilan birga Telegram orqali yuboriladi.

6. **🌐 Ikki tilli (Bilingual):**
   - 🇺🇿 O'zbekcha (Lotin)
   - 🇷🇺 Русский

7. **📊 Shaxsiy statistika:**
   - Ishlangan testlar soni, yechilgan savollar, to'g'ri va xato javoblar, o'rtacha aniqlik foizi.

8. **🔐 Admin paneli (`/admin`):**
   - Umumiy foydalanuvchilar soni va faollik statistikasi.
   - Barcha bot foydalanuvchilariga xabar tarqatish (Broadcast).

---

## 🚀 O'rnatish va Sozlash

### 1. Bot tokenini kiritish
Loyihaning ildizidagi `.env` faylini oching va `@BotFather` dan olingan tokeningizni kiriting:

```env
AVTOTEST_BOT_TOKEN=8423456789:AAH...sizning_tokeningiz...
AVTOTEST_ADMIN_IDS=5656372773
```

---

## ▶️ Ishga tushirish usullari

### 1-usul: Bir marta bosish bilan (Windows)
Loyihaning ichidagi `start_bot.bat` faylini ikki marta bosing yoki terminalda:
```powershell
.\start_bot.bat
```

### 2-usul: Python orqali to'g'ridan-to'g'ri
```bash
python run_bot.py
```

### 3-usul: Django Management Command orqali
```bash
python manage.py run_avtotest_bot
```

---

## 📁 Fayllar Strukturasi

```text
django_complexprogrammer/
├── avtotest_bot/
│   ├── __init__.py
│   ├── config.py           # Sozlamalar va yo'llar
│   ├── database.py         # aiosqlite orqali asinxron DB boshqaruvi
│   ├── texts.py            # O'zbek va rus tillaridagi matnlar
│   ├── keyboards.py        # Reply va Inline klaviaturalar
│   ├── main.py             # Botni ishga tushirish kodi
│   └── handlers/
│       ├── __init__.py     # Routerlarni birlashtirish
│       ├── start.py        # /start va til tanlash
│       ├── bilet.py        # 108 bilet tanlash va navigatsiya
│       ├── quiz.py         # Savollarni chiqarish, javob tekshirish, natijalar
│       ├── exam.py         # 20 ta savollik imtihon
│       ├── cdl.py          # AQSh CDL testi
│       ├── mistakes.py     # Xatolar ustida ishlash
│       ├── stats.py        # Shaxsiy statistika
│       ├── help.py         # Yordam va ilovaga havolalar
│       └── admin.py        # Admin panel va xabar tarqatish
├── tests/
│   └── management/
│       └── commands/
│           └── run_avtotest_bot.py  # Django manage.py komandasi
├── run_bot.py              # Asosiy ishga tushiruvchi
├── start_bot.bat           # Windows ishga tushiruvchisi
├── .env                    # AVTOTEST_BOT_TOKEN sozlamasi
└── AVTOTEST_BOT_README.md  # Qo'llanma
```
