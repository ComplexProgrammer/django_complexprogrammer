# avtotest_bot/texts.py
# O'zbekcha va Ruscha matnlar to'plami

TEXTS = {
    "uz": {
        "welcome": (
            "🚗 <b>Assalomu alaykum, {name}!</b>\n\n"
            "<b>@AvtoTestUzbBot</b> rasmiy avtotest botiga xush kelibsiz!\n\n"
            "Bu bot orqali siz O'zbekiston YHXBB rasmiy imtihon bazasidagi "
            "<b>108 ta bilet (1080 ta savol)</b> bo'yicha to'liq tayyorgarlik ko'rishingiz, "
            "haqiqiy imtihon rejimida o'zingizni sinab ko'rishingiz va xatolaringiz ustida ishlashingiz mumkin.\n\n"
            "📱 <b>Bizning mobil ilova:</b> <a href='https://play.google.com/store/apps/details?id=uzbavtotest.complexprogrammer.uz'>Google Play'da Avto Test Uzb</a>\n"
            "🌐 <b>Rasmiy veb-saytimiz:</b> <a href='https://complexprogrammer.uz/avtotest/'>complexprogrammer.uz</a>\n"
            "📢 <b>Rasmiy kanalimiz:</b> @complexprogrammeruzchannel\n\n"
            "Quyidagi menyudan kerakli bo'limni tanlang 👇"
        ),
        "lang_chosen": "✅ Til muvaffaqiyatli tanlandi: <b>O'zbek tili 🇺🇿</b>",
        "select_lang": "🌐 <b>Iltimos, o'zingizga qulay tilni tanlang / Пожалуйста, выберите язык:</b>",
        # Tugmalar
        "btn_bilets": "🚗 Biletlar (1-108)",
        "btn_exam": "🎲 Imtihon (20 savol)",
        "btn_cdl": "🇺🇸 AQSh CDL testi",
        "btn_mistakes": "❌ Xatolar ustida ishlash",
        "btn_stats": "📊 Mening natijalarim",
        "btn_lang": "🌐 Tilni o'zgartirish",
        "btn_help": "ℹ️ Bot haqida",
        "btn_webapp": "📱 Saytda imtihon",
        # Biletlar bo'limi
        "bilet_title": "🚗 <b>Biletni tanlang:</b>\n<i>(Har bir biletda 10 tadan savol bor)</i>",
        "page_info": "Sahifa: {page}/{total_pages}",
        # Test jarayoni
        "question_header": "🚗 <b>{title}</b>\n📌 <b>Savol {current}/{total}:</b>\n\n",
        "correct_answer_feedback": "✅ <b>To'g'ri javob! Barakalla!</b>",
        "wrong_answer_feedback": "❌ <b>Noto'g'ri javob!</b>\n\nTo'g'ri javob: <b>{correct_text}</b>",
        "btn_next_question": "Keyingi savol ➡️",
        "btn_finish_quiz": "Natijani ko'rish 🏁",
        "btn_cancel_quiz": "⏹ To'xtatish",
        "quiz_cancelled": "⏹ Test to'xtatildi. Bosh menyuga qaytildi.",
        # Yakuniy natijalar
        "result_header": "🏁 <b>TEST YAKUNLANDI!</b>\n\n",
        "result_info": (
            "📋 <b>Bilet / Rejim:</b> {title}\n"
            "📊 <b>Jami savollar:</b> {total} ta\n"
            "✅ <b>To'g'ri javoblar:</b> {score} ta\n"
            "❌ <b>Xato javoblar:</b> {mistakes} ta\n"
            "🎯 <b>Natija:</b> {percentage}%\n\n"
        ),
        "result_passed": "🎉 <b>TABRIKLAYMIZ!</b>\nSiz imtihon sinovidan muvaffaqiyatli o'tdingiz! 👏🚗",
        "result_failed": "⚠️ <b>AFSUSKI O'TA OLMADINGIZ!</b>\nO'tish bali: 90%. Bilimingizni mustahkamlab, yana qayta topshiring! 💪",
        # Tugmalar yakunida
        "btn_retry": "🔄 Qaytadan ishlash",
        "btn_next_bilet": "➡️ Keyingi bilet ({next_bilet})",
        "btn_review_mistakes": "❌ Xatolarni tahlil qilish",
        "btn_home": "🏠 Bosh menyu",
        # Xatolar bo'limi
        "no_mistakes": (
            "🎉 <b>Ajoyib! Sizda xato qilingan savollar yo'q!</b>\n"
            "Biletlarni yoki Imtihon rejimini ishlashda davom eting."
        ),
        "mistakes_start": "❌ <b>Xatolar ustida ishlash:</b>\nSiz oldin xato qilgan {count} ta savol bo'yicha mashq boshlanmoqda.",
        # Statistika
        "stats_title": (
            "📊 <b>SIZNING SHAXSIY NATIJALARINGIZ</b>\n\n"
            "👤 <b>Foydalanuvchi:</b> {name}\n"
            "📅 <b>Ro'yxatdan o'tgan:</b> {registered_date}\n\n"
            "🚗 <b>Ishlangan testlar soni:</b> {total_tests} ta\n"
            "❓ <b>Yechilgan barcha savollar:</b> {total_questions} ta\n"
            "✅ <b>To'g'ri berilgan javoblar:</b> {correct_answers} ta\n"
            "❌ <b>Xato berilgan javoblar:</b> {wrong_answers} ta\n"
            "🎯 <b>O'rtacha aniqlik foizi:</b> {accuracy}%\n\n"
            "<i>Mashq qilishda davom eting va bilimingizni 100% ga yetkazing!</i>"
        ),
        # Bot haqida
        "help_text": (
            "ℹ️ <b>@AvtoTestUzbBot haqida ma'lumot:</b>\n\n"
            "🚗 <b>Loyiha maqsadi:</b> O'zbekistonda haydovchilik guvohnomasini oluvchilar uchun "
            "YHXBB rasmiy imtihoniga mukammal tayyorlanish imkoniyatini taqdim etish.\n\n"
            "📱 <b>Mobil ilovamiz:</b> <a href='https://play.google.com/store/apps/details?id=uzbavtotest.complexprogrammer.uz'>Google Play'da Avto Test Uzb</a>\n"
            "🌐 <b>Veb-saytimiz:</b> <a href='https://complexprogrammer.uz/avtotest/'>complexprogrammer.uz</a>\n\n"
            "❓ <b>Savollar va takliflar uchun:</b> @complexprogrammeruzchannel"
        ),
        # Kunlik eslatma
        "remind_on": (
            "⏰ <b>Kunlik eslatma yoqildi!</b>\n\n"
            "Har kuni kechqurun, agar o'sha kuni mashq qilmagan bo'lsangiz, eslatib turamiz. "
            "O'chirish uchun yana /eslatma yuboring."
        ),
        "remind_off": "🔕 Kunlik eslatma o'chirildi. Qayta yoqish uchun /eslatma yuboring.",
        "remind_daily": (
            "🚗 <b>Bugungi mashg'ulot vaqti keldi!</b>\n\n"
            "Imtihonga tayyorgarlikni to'xtatmang — kuniga 10 ta savol ham katta natija beradi.\n\n"
            "🎲 /exam — 20 savollik imtihon\n"
            "❌ /mistakes — xatolar ustida ishlash\n"
            "🎯 <a href='https://complexprogrammer.uz/avtotest/imtihon/'>Saytdagi imtihon simulyatori</a>\n\n"
            "<i>Eslatmani o'chirish: /eslatma</i>"
        ),
    },
    "ru": {
        "welcome": (
            "🚗 <b>Здравствуйте, {name}!</b>\n\n"
            "Добро пожаловать в официальный бот <b>@AvtoTestUzbBot</b>!\n\n"
            "Здесь вы можете подготовиться к сдаче экзамена в ГАИ (СБДД) Узбекистана "
            "по официальной базе из <b>108 билетов (1080 вопросов)</b>, "
            "сдать случайный экзамен и провести работу над ошибками.\n\n"
            "📱 <b>Наше приложение:</b> <a href='https://play.google.com/store/apps/details?id=uzbavtotest.complexprogrammer.uz'>Avto Test Uzb в Google Play</a>\n"
            "🌐 <b>Наш сайт:</b> <a href='https://complexprogrammer.uz/avtotest/'>complexprogrammer.uz</a>\n"
            "📢 <b>Наш канал:</b> @complexprogrammeruzchannel\n\n"
            "Выберите нужный раздел в меню ниже 👇"
        ),
        "lang_chosen": "✅ Язык успешно выбран: <b>Русский 🇷🇺</b>",
        "select_lang": "🌐 <b>Пожалуйста, выберите язык / Iltimos, tilni tanlang:</b>",
        # Кнопки
        "btn_bilets": "🚗 Билеты (1-108)",
        "btn_exam": "🎲 Экзамен (20 вопросов)",
        "btn_cdl": "🇺🇸 Тест США CDL",
        "btn_mistakes": "❌ Работа над ошибками",
        "btn_stats": "📊 Моя статистика",
        "btn_lang": "🌐 Сменить язык",
        "btn_help": "ℹ️ О боте",
        "btn_webapp": "📱 Экзамен на сайте",
        # Билеты
        "bilet_title": "🚗 <b>Выберите билет:</b>\n<i>(В каждом билете по 10 вопросов)</i>",
        "page_info": "Страница: {page}/{total_pages}",
        # Процесс теста
        "question_header": "🚗 <b>{title}</b>\n📌 <b>Вопрос {current}/{total}:</b>\n\n",
        "correct_answer_feedback": "✅ <b>Правильный ответ! Отлично!</b>",
        "wrong_answer_feedback": "❌ <b>Неправильный ответ!</b>\n\nПравильный ответ: <b>{correct_text}</b>",
        "btn_next_question": "Следующий вопрос ➡️",
        "btn_finish_quiz": "Посмотреть результат 🏁",
        "btn_cancel_quiz": "⏹ Прервать",
        "quiz_cancelled": "⏹ Тест прерван. Вы вернулись в главное меню.",
        # Финал
        "result_header": "🏁 <b>ТЕСТ ЗАВЕРШЕН!</b>\n\n",
        "result_info": (
            "📋 <b>Билет / Режим:</b> {title}\n"
            "📊 <b>Всего вопросов:</b> {total}\n"
            "✅ <b>Правильных ответов:</b> {score}\n"
            "❌ <b>Ошибок:</b> {mistakes}\n"
            "🎯 <b>Результат:</b> {percentage}%\n\n"
        ),
        "result_passed": "🎉 <b>ПОЗДРАВЛЯЕМ!</b>\nВы успешно сдали экзамен! 👏🚗",
        "result_failed": "⚠️ <b>К СОЖАЛЕНИЮ, ЭКЗАМЕН НЕ СДАН!</b>\nПроходной балл: 90%. Повторите правила и попробуйте снова! 💪",
        # Кнопки в конце
        "btn_retry": "🔄 Пройти заново",
        "btn_next_bilet": "➡️ Следующий билет ({next_bilet})",
        "btn_review_mistakes": "❌ Работа над ошибками",
        "btn_home": "🏠 Главное меню",
        # Ошибки
        "no_mistakes": (
            "🎉 <b>Превосходно! У вас нет сохраненных ошибок!</b>\n"
            "Продолжайте решать билеты или сдайте экзамен."
        ),
        "mistakes_start": "❌ <b>Работа над ошибками:</b>\nНачинаем тренировку по {count} вопросам, где вы ошиблись ранее.",
        # Статистика
        "stats_title": (
            "📊 <b>ВАША ЛИЧНАЯ СТАТИСТИКА</b>\n\n"
            "👤 <b>Пользователь:</b> {name}\n"
            "📅 <b>Дата регистрации:</b> {registered_date}\n\n"
            "🚗 <b>Пройдено тестов:</b> {total_tests}\n"
            "❓ <b>Решено вопросов:</b> {total_questions}\n"
            "✅ <b>Правильных ответов:</b> {correct_answers}\n"
            "❌ <b>Неправильных ответов:</b> {wrong_answers}\n"
            "🎯 <b>Средняя точность:</b> {accuracy}%\n\n"
            "<i>Продолжайте тренироваться каждый день!</i>"
        ),
        # О боте
        "help_text": (
            "ℹ️ <b>О боте @AvtoTestUzbBot:</b>\n\n"
            "🚗 <b>Цель проекта:</b> Предоставить кандидатам в водители качественный и удобный "
            "инструмент для сдачи официального экзамена СБДД Узбекистана.\n\n"
            "📱 <b>Приложение Android:</b> <a href='https://play.google.com/store/apps/details?id=uzbavtotest.complexprogrammer.uz'>Avto Test Uzb в Google Play</a>\n"
            "🌐 <b>Наш сайт:</b> <a href='https://complexprogrammer.uz/avtotest/'>complexprogrammer.uz</a>\n\n"
            "❓ <b>Вопросы и поддержка:</b> @complexprogrammeruzchannel"
        ),
        "remind_on": (
            "⏰ <b>Ежедневное напоминание включено!</b>\n\n"
            "Каждый вечер, если вы ещё не занимались в этот день, мы напомним. "
            "Чтобы отключить, снова отправьте /eslatma."
        ),
        "remind_off": "🔕 Ежедневное напоминание отключено. Чтобы включить, отправьте /eslatma.",
        "remind_daily": (
            "🚗 <b>Время для сегодняшней тренировки!</b>\n\n"
            "Не прерывайте подготовку — даже 10 вопросов в день дают большой результат.\n\n"
            "🎲 /exam — экзамен из 20 вопросов\n"
            "❌ /mistakes — работа над ошибками\n"
            "🎯 <a href='https://complexprogrammer.uz/ru/avtotest/imtihon/'>Симулятор экзамена на сайте</a>\n\n"
            "<i>Отключить напоминание: /eslatma</i>"
        ),
    },
}


def get_text(key: str, lang: str = "uz", **kwargs) -> str:
    texts = TEXTS.get(lang, TEXTS["uz"])
    template = texts.get(key, TEXTS["uz"].get(key, ""))
    if kwargs:
        try:
            return template.format(**kwargs)
        except Exception:
            return template
    return template
