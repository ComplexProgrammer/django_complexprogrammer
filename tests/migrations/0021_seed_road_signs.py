"""Yo'l belgilarini avtotest bazasidagi ma'lumotlardan to'ldirish.

Manba: projects_avtotest dagi "Bu yo'l belgisi bildiradi: ..." turidagi savollar. Ularning rasmi (static/avtotest/bN.jpg)
bitta belgidan iborat, to'g'ri javobi esa belgining nomi. Tavsiflar shu rasmga tegishli boshqa savollarning
to'g'ri javoblaridan olingan. Ruscha/inglizcha nomlar bazadagi mashina tarjimasi o'rniga rasmiy nomlarga to'g'rilangan.
Belgi raqamlari bazada yo'q — admin panel orqali qo'shiladi.
"""

import shutil
from pathlib import Path

from django.conf import settings
from django.db import migrations

IMAGE_DIR = "tests/road_signs/images"

# (rasm, toifa, nomi uz, ru, en, tavsif uz, ru, en)
SIGNS = [
    # Ogohlantiruvchi belgilar
    ("b1.jpg", "warning", "Shlagbaumli temir yo'l kesishmasi", "Железнодорожный переезд со шлагбаумом", "Level crossing with barrier", "", "", ""),
    ("b2.jpg", "warning", "Shlagbaumsiz temir yo'l kesishmasi", "Железнодорожный переезд без шлагбаума", "Level crossing without barrier", "", "", ""),
    ("b3.jpg", "warning", "Bir izli temir yo'l kesishmasi", "Однопутная железная дорога", "Single-track railway crossing", "", "", ""),
    ("b4.jpg", "warning", "Ko'p izli temir yo'l kesishmasi", "Многопутная железная дорога", "Multi-track railway crossing",
     "Ko'p izli, shlagbaumsiz temir yo'l kesishmasidan ogohlantiradi.",
     "Предупреждает о многопутном железнодорожном переезде без шлагбаума.",
     "Warns of a multi-track railway crossing without a barrier."),
    ("b5.jpg", "warning", "Temir yo'l kesishmasiga yaqinlashuv", "Приближение к железнодорожному переезду", "Approaching a level crossing", "", "", ""),
    ("b8.jpg", "warning", "Tramvay yo'li bilan kesishuv", "Пересечение с трамвайной линией", "Crossing with a tram line", "", "", ""),
    ("b9.jpg", "warning", "Teng ahamiyatli yo'llar kesishuvi", "Пересечение равнозначных дорог", "Crossroads of equal roads",
     "Bu belgi o'rnatilgan chorrahada o'ng tomondan kelayotgan transport vositasiga yo'l beriladi.",
     "На таком перекрёстке нужно уступить дорогу транспортному средству, приближающемуся справа.",
     "At such a crossroads, give way to vehicles approaching from the right."),
    ("b10.jpg", "warning", "Aylanma harakat bilan kesishuv", "Пересечение с круговым движением", "Roundabout ahead", "", "", ""),
    ("b11.jpg", "warning", "Svetofor bilan tartibga solish", "Светофорное регулирование", "Traffic signals ahead", "", "", ""),
    ("b12.jpg", "warning", "Ko'tarma ko'prik", "Разводной мост", "Opening bridge", "", "", ""),
    ("b13.jpg", "warning", "Sohilga chiqish", "Выезд на набережную", "Quayside or river bank", "", "", ""),
    ("b14.jpg", "warning", "Xavfli burilish", "Опасный поворот", "Dangerous bend", "", "", ""),
    ("b15.jpg", "warning", "Yo'lning chapga burilishi", "Опасный поворот налево", "Dangerous bend to the left", "", "", ""),
    ("b16.jpg", "warning", "Xavfli burilishlar (birinchisi o'ngga)", "Опасные повороты (первый направо)", "Double bend, first to the right", "", "", ""),
    ("b18.jpg", "warning", "Tik nishablik", "Крутой спуск", "Steep descent", "", "", ""),
    ("b19.jpg", "warning", "Tik balandlik", "Крутой подъём", "Steep ascent", "", "", ""),
    ("b20.jpg", "warning", "Sirpanchiq yo'l", "Скользкая дорога", "Slippery road",
     "Bu belgi o'rnatilgan joyda haydovchi tezlikni kamaytirishi, keskin to'xtamasligi va keskin burilmasligi lozim.",
     "В зоне действия знака водитель должен снизить скорость, не тормозить и не поворачивать резко.",
     "Within the sign's zone the driver should slow down and avoid sudden braking or turning."),
    ("b21.jpg", "warning", "Notekis yo'l", "Неровная дорога", "Uneven road",
     "Bunday joyda tezlik keskin oshirilsa yoki keskin to'xtalsa, avtomobil turg'unligini yo'qotadi va ag'darilish xavfi ortadi.",
     "Если здесь резко разгоняться или тормозить, автомобиль теряет устойчивость и растёт риск опрокидывания.",
     "Sudden acceleration or braking here makes the car lose stability and raises the risk of overturning."),
    ("b22.jpg", "warning", "Tosh otilishi", "Выброс гравия", "Loose chippings",
     "Transport vositalari g'ildiragi ostidan tosh otilishi xavfi mavjudligidan ogohlantiradi.",
     "Предупреждает об опасности выброса гравия из-под колёс.",
     "Warns that stones may be thrown up by vehicle wheels."),
    ("b23.jpg", "warning", "Yo'lning ikki tomonlama torayishi", "Сужение дороги", "Road narrows on both sides", "", "", ""),
    ("b24.jpg", "warning", "Yo'lning o'ngdan torayishi", "Сужение дороги справа", "Road narrows on the right", "", "", ""),
    ("b25.jpg", "warning", "Yo'lning chapdan torayishi", "Сужение дороги слева", "Road narrows on the left", "", "", ""),
    ("b26.jpg", "warning", "Ikki tomonlama harakatlanish", "Двустороннее движение", "Two-way traffic", "", "", ""),
    ("b27.jpg", "warning", "Piyodalar o'tish joyi", "Пешеходный переход", "Pedestrian crossing",
     "Yo'lning piyodalar o'tish joyi bo'lgan qismidan ogohlantiradi.",
     "Предупреждает об участке дороги с пешеходным переходом.",
     "Warns of a section of road with a pedestrian crossing."),
    ("b28.jpg", "warning", "Bolalar", "Дети", "Children",
     "Yo'lning bu qismida bolalar yo'lga chiqib qolishi mumkinligidan ogohlantiradi.",
     "Предупреждает, что на этом участке на дорогу могут выйти дети.",
     "Warns that children may run onto the road on this section."),
    ("b29.jpg", "warning", "Velosiped yo'lkasi bilan kesishuv", "Пересечение с велосипедной дорожкой", "Cycle lane crossing", "", "", ""),
    ("b30.jpg", "warning", "Ta'mirlash ishlari", "Дорожные работы", "Road works", "", "", ""),
    ("b31.jpg", "warning", "Mol haydab o'tish", "Перегон скота", "Cattle crossing",
     "Yo'lga mol-qo'y podasi chiqib qolishi mumkinligidan ogohlantiradi.",
     "Предупреждает, что на дорогу может выйти стадо скота.",
     "Warns that livestock may come onto the road."),
    ("b32.jpg", "warning", "Yovvoyi hayvonlar", "Дикие животные", "Wild animals",
     "Yo'lga yovvoyi hayvonlar chiqib qolishi mumkinligidan ogohlantiradi.",
     "Предупреждает, что на дорогу могут выйти дикие животные.",
     "Warns that wild animals may come onto the road."),
    ("b33.jpg", "warning", "Toshlar tushishi", "Падение камней", "Falling rocks", "", "", ""),
    ("b34.jpg", "warning", "Yonlama shamol", "Боковой ветер", "Crosswind",
     "Yonlama shamol mavjudligidan ogohlantiradi.", "Предупреждает о боковом ветре.", "Warns of crosswinds."),
    ("b36.jpg", "warning", "Tonnel", "Тоннель", "Tunnel",
     "Peshtoqi ko'rinishi cheklangan va yoritilmagan tonnelga yaqinlashuvdan ogohlantiradi.",
     "Предупреждает о приближении к неосвещённому тоннелю с ограниченной видимостью въездного портала.",
     "Warns of an unlit tunnel whose entrance has limited visibility."),
    ("b37.jpg", "warning", "Burilish yo'nalishi", "Направление поворота", "Direction of bend", "", "", ""),
    ("b39.jpg", "warning", "Burilish yo'nalishlari", "Направления поворота", "Directions of bend", "", "", ""),
    # Imtiyoz belgilari
    ("b41.jpg", "priority", "Ikkinchi darajali yo'l bilan kesishuv", "Пересечение со второстепенной дорогой", "Crossroads with a minor road", "", "", ""),
    ("b42.jpg", "priority", "Ikkinchi darajali yo'lning tutashuvi", "Примыкание второстепенной дороги", "Minor road junction", "", "", ""),
    ("b44.jpg", "priority", "Yo'l bering", "Уступите дорогу", "Give way", "", "", ""),
    ("b45.jpg", "priority", "To'xtamasdan harakatlanish taqiqlangan", "Движение без остановки запрещено", "Stop", "", "", ""),
    ("b46.jpg", "priority", "Ro'paradan harakatlanishning ustunligi", "Преимущество встречного движения", "Priority to oncoming traffic", "", "", ""),
    ("b47.jpg", "priority", "Ro'paradagi harakatlanishga nisbatan imtiyoz", "Преимущество перед встречным движением", "Priority over oncoming traffic", "", "", ""),
    ("b48.jpg", "priority", "Asosiy yo'l", "Главная дорога", "Priority road",
     "Asosiy yo'lning boshlanishini bildiradi. 7.13 qo'shimcha axborot belgisi bilan qo'llanilishi mumkin.",
     "Обозначает начало главной дороги. Может применяться с табличкой 7.13.",
     "Marks the start of a priority road. May be used with additional plate 7.13."),
    ("b49.jpg", "priority", "Asosiy yo'lning oxiri", "Конец главной дороги", "End of priority road", "", "", ""),
    # Taqiqlovchi belgilar
    ("b50.jpg", "prohibitory", "Kirish taqiqlangan", "Въезд запрещён", "No entry",
     "Belgilangan yo'nalishli transport vositalaridan tashqari barcha transport vositalarining kirishi taqiqlanadi.",
     "Запрещён въезд всех транспортных средств, кроме маршрутных.",
     "Entry is prohibited for all vehicles except route (public transport) vehicles."),
    ("b52.jpg", "prohibitory", "Harakatlanish taqiqlangan", "Движение запрещено", "No vehicles", "", "", ""),
    ("b54.jpg", "prohibitory", "Yuk avtomobillarining harakatlanishi taqiqlangan", "Движение грузовых автомобилей запрещено", "No goods vehicles",
     "Belgida 8 t ko'rsatilgan bo'lsa, to'la vazni 8 tonnadan og'ir transport vositalarining harakati taqiqlanadi.",
     "Если на знаке указано 8 т, запрещено движение транспортных средств с полной массой более 8 тонн.",
     "When the sign shows 8 t, vehicles with a gross weight over 8 tonnes are prohibited."),
    ("b55.jpg", "prohibitory", "Mototsikllarda harakatlanish taqiqlangan", "Движение мотоциклов запрещено", "No motorcycles",
     "Faqat mototsikllar harakati taqiqlanadi.", "Запрещено движение только мотоциклов.", "Only motorcycles are prohibited."),
    ("b57.jpg", "prohibitory", "Tirkama bilan harakatlanish taqiqlangan", "Движение с прицепом запрещено", "No vehicles with trailers",
     "Bu belgi o'rnatilgan yo'llarda tirkama bilan harakatlanish taqiqlanadi.",
     "На дорогах с этим знаком запрещено движение с прицепом.",
     "Driving with a trailer is prohibited on roads with this sign."),
    ("b60.jpg", "prohibitory", "Piyodalar harakatlanishi taqiqlangan", "Движение пешеходов запрещено", "No pedestrians", "", "", ""),
    ("b61.jpg", "prohibitory", "Umumiy vazn cheklangan", "Ограничение массы", "Weight limit", "", "", ""),
    ("b62.jpg", "prohibitory", "O'qqa tushadigan og'irlik cheklangan", "Ограничение массы, приходящейся на ось транспортного средства", "Axle weight limit", "", "", ""),
    ("b63.jpg", "prohibitory", "Balandlik cheklangan", "Ограничение высоты", "Height limit", "", "", ""),
    ("b64.jpg", "prohibitory", "Kenglik cheklangan", "Ограничение ширины", "Width limit", "", "", ""),
    ("b65.jpg", "prohibitory", "Uzunlik cheklangan", "Ограничение длины", "Length limit", "", "", ""),
    ("b66.jpg", "prohibitory", "O'ngga burilish taqiqlangan", "Поворот направо запрещён", "No right turn",
     "Belgilangan yo'nalishli transport vositalaridan tashqari barcha avtomobillarning o'ngga burilishi taqiqlanadi.",
     "Запрещён поворот направо всем транспортным средствам, кроме маршрутных.",
     "Turning right is prohibited for all vehicles except route vehicles."),
    ("b67.jpg", "prohibitory", "Chapga burilish taqiqlangan", "Поворот налево запрещён", "No left turn",
     "Haydovchiga o'ngga, to'g'riga harakatlanish va qayrilish ruxsat etiladi.",
     "Разрешается движение направо, прямо и разворот.",
     "Turning right, going straight and U-turns are allowed."),
    ("b69.jpg", "prohibitory", "Quvib o'tish taqiqlangan", "Обгон запрещён", "No overtaking", "", "", ""),
    ("b73.jpg", "prohibitory", "Eng yuqori tezlik cheklangan", "Ограничение максимальной скорости", "Maximum speed limit", "", "", ""),
    ("b78.jpg", "prohibitory", "Oyning toq kunlarida to'xtab turish taqiqlangan", "Стоянка запрещена по нечётным числам месяца", "No parking on odd days of the month", "", "", ""),
    ("b79.jpg", "prohibitory", "Oyning juft kunlarida to'xtab turish taqiqlangan", "Стоянка запрещена по чётным числам месяца", "No parking on even days of the month", "", "", ""),
    # Buyuruvchi belgilar
    ("b81.jpg", "mandatory", "To'g'riga harakatlanish", "Движение прямо", "Ahead only",
     "Haydovchi faqat to'g'riga harakatlanishi mumkin.", "Разрешается движение только прямо.", "Only straight-ahead travel is allowed."),
    ("b82.jpg", "mandatory", "O'ngga harakatlanish", "Движение направо", "Turn right only", "", "", ""),
    ("b83.jpg", "mandatory", "Chapga harakatlanish", "Движение налево", "Turn left only",
     "Chapga burilish va orqaga qayrilishga ruxsat etiladi.", "Разрешаются поворот налево и разворот.", "Turning left and U-turns are allowed."),
    ("b84.jpg", "mandatory", "To'g'riga yoki o'ngga harakatlanish", "Движение прямо или направо", "Ahead or turn right", "", "", ""),
]

# Lotin -> kirill (o'zbek). Ikki harfli birikmalar birinchi tekshiriladi.
_PAIRS = [("yo'", "йў"), ("o'", "ў"),("g'", "ғ"), ("sh", "ш"), ("ch", "ч"), ("yo", "ё"), ("yu", "ю"), ("ya", "я"), ("ye", "е")]
_CHARS = dict(zip("abdefghijklmnopqrstuvxyz'", "абдэфгҳижклмнопқрстувхйзъ"))


def to_cyrillic(text):
    out, i, low = [], 0, text.lower()
    while i < len(text):
        for lat, cyr in _PAIRS:
            if low.startswith(lat, i):
                out.append(cyr[0].upper() + cyr[1:] if text[i].isupper() else cyr)
                i += len(lat)
                break
        else:
            ch = text[i]
            cyr = _CHARS.get(ch.lower())
            if cyr is None:
                out.append(ch)
            else:
                # "e" so'z boshida "э", ichida "е"
                if ch.lower() == "e" and i > 0 and low[i - 1].isalpha():
                    cyr = "е"
                out.append(cyr.upper() if ch.isupper() else cyr)
            i += 1
    return "".join(out)


def seed(apps, schema_editor):
    RoadSignCategories = apps.get_model("tests", "RoadSignCategories")
    RoadSigns = apps.get_model("tests", "RoadSigns")
    categories = {c.code: c for c in RoadSignCategories.objects.all()}
    src_dir = Path(settings.BASE_DIR) / "static" / "avtotest"
    dst_dir = Path(settings.MEDIA_ROOT) / IMAGE_DIR
    dst_dir.mkdir(parents=True, exist_ok=True)

    for index, (image, code, uz, ru, en, d_uz, d_ru, d_en) in enumerate(SIGNS, start=1):
        category = categories.get(code)
        if category is None:
            continue
        name = f"{IMAGE_DIR}/{image}"
        if RoadSigns.objects.filter(image=name).exists():
            continue  # qayta ishga tushirilsa yoki admin'da tahrirlangan bo'lsa — tegilmaydi
        if not (dst_dir / image).exists() and (src_dir / image).exists():
            shutil.copyfile(src_dir / image, dst_dir / image)
        RoadSigns.objects.create(
            category=category,
            number="",
            name_uz_uz=uz,
            name_uz_crl=to_cyrillic(uz),
            name_ru_ru=ru,
            name_en_us=en,
            description_uz_uz=d_uz,
            description_uz_crl=to_cyrillic(d_uz),
            description_ru_ru=d_ru,
            description_en_us=d_en,
            image=name,
            sort_order=index,
        )


def unseed(apps, schema_editor):
    RoadSigns = apps.get_model("tests", "RoadSigns")
    RoadSigns.objects.filter(image__in=[f"{IMAGE_DIR}/{s[0]}" for s in SIGNS]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("tests", "0020_seed_road_sign_categories"),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
