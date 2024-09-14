# Python 3.11 image'ni yuklaymiz
FROM python:3.10-slim


# Konteyner ichida ish katalogini o'rnatamiz
WORKDIR /app

# Mahalliy fayllarni konteynerga nusxalash
COPY . /app

# Python kutubxonalarni o'rnatish (requirements.txt orqali)
RUN pip install --no-cache-dir -r requirements.txt

# Django loyihasini ishga tushirish
CMD ["python", "manage.py", "runserver", "0.0.0.0:4444"]
