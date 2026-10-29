# avtotest_bot/texts.py
# O'zbekcha va Ruscha matnlar to'plami

TEXTS = {
    "uz": {
        "welcome": (
            "🚗 <b>Assalomu alaykum, {name}!</b>\n\n"
            "<b>@AvtoTestUzbBot</b> rasmiy avtotest botiga xuş kelibsiz!\n\n"
            "Bu bot orqali siz Özbekiston YHXBB rasmiy imtihon bazasidagi "
            "<b>108 ta bilet (1080 ta savol)</b> böyiça töliq tayyorgarlik körişingiz, "
            "haqiqiy imtihon rejimida özingizni sinab körişingiz va xatolaringiz ustida işlaşingiz mumkin.\n\n"
            "📱 <b>Bizning mobil ilova:</b> <a href='https://play.google.com/store/apps/details?id=uzbavtotest.complexprogrammer.uz'>Google Play'da Avto Test Uzb</a>\n"
            "🌐 <b>Rasmiy veb-saytimiz:</b> <a href='https://complexprogrammer.uz/avtotest/?utm_source=telegram&utm_medium=bot&utm_campaign=info'>complexprogrammer.uz</a>\n"
            "📢 <b>Rasmiy kanalimiz:</b> @complexprogrammeruzchannel\n\n"
            "Quyidagi menyudan kerakli bölimni tanlang 👇"
        ),
        "lang_chosen": "✅ Til muvaffaqiyatli tanlandi: <b>Özbek tili 🇺🇿</b>",
        "select_lang": "🌐 <b>Iltimos, özingizga qulay tilni tanlang / Пожалуйста, выберите язык:</b>",
        # Tugmalar
        "btn_bilets": "🚗 Biletlar (1-108)",
        "btn_exam": "🎲 Imtihon (20 savol)",
        "btn_cdl": "🇺🇸 AQŞ CDL testi",
        "btn_mistakes": "❌ Xatolar ustida işlaş",
        "btn_stats": "📊 Mening natijalarim",
        "btn_lang": "🌐 Tilni özgartiriş",
        "btn_help": "ℹ️ Bot haqida",
        "btn_webapp": "📱 Saytda imtihon",
        "btn_quick": "⚡ Tezkor maşq (5 savol)",
        "quick_title": "⚡ Tezkor maşq (5 savol)",
        "remind_ask": (
            "⏰ <b>Har kuni eslatib turaymi?</b>\n\n"
            "Keçqurun, agar öşa kuni maşq qilmagan bölsangiz, bitta qisqa xabar yuboraman. "
            "Kuniga 10 ta savol — imtihonga eng işonçli tayyorgarlik."
        ),
        "btn_remind_yes": "✅ Ha, eslatib tur",
        "btn_remind_no": "Kerak emas",
        "remind_declined": "Yaxşi, eslatma yubormayman. Fikringiz özgarsa: /eslatma",
        "resume_nudge": (
            "📌 <b>{title}</b> testini {done}/{total} savolda töxtatib qöygansiz.\n\n"
            "Qolgan {left} ta savolni hozir tugatamizmi?"
        ),
        "btn_resume": "▶️ Davom ettiriş",
        "no_session": "Faol test topilmadi. Boş menyudan yangisini boşlang.",
        "invite_hint": "\n\n🤝 Imtihonga tayyorlanayotgan döstingiz bormi? /taklif",
        # Biletlar bo'limi
        "bilet_title": "🚗 <b>Biletni tanlang:</b>\n<i>(Har bir biletda 10 tadan savol bor)</i>",
        "page_info": "Sahifa: {page}/{total_pages}",
        # Test jarayoni
        "question_header": "🚗 <b>{title}</b>\n📌 <b>Savol {current}/{total}</b>  {bar}\n\n",
        "correct_answer_feedback": "✅ <b>Töğri javob! Barakalla!</b>",
        "wrong_answer_feedback": "❌ <b>Notöğri javob!</b>\n\nTöğri javob: <b>{correct_text}</b>",
        "btn_next_question": "Keyingi savol ➡️",
        "btn_finish_quiz": "Natijani köriş 🏁",
        "btn_cancel_quiz": "⏹ Töxtatiş",
        "quiz_cancelled": "⏹ Test töxtatildi. Boş menyuga qaytildi.",
        # Yakuniy natijalar
        "result_header": "🏁 <b>TEST YAKUNLANDI!</b>\n\n",
        "result_info": (
            "📋 <b>Bilet / Rejim:</b> {title}\n"
            "📊 <b>Jami savollar:</b> {total} ta\n"
            "✅ <b>Töğri javoblar:</b> {score} ta\n"
            "❌ <b>Xato javoblar:</b> {mistakes} ta\n"
            "🎯 <b>Natija:</b> {percentage}%\n\n"
        ),
        "result_passed": "🎉 <b>TABRIKLAYMIZ!</b>\nSiz imtihon sinovidan muvaffaqiyatli ötdingiz! 👏🚗",
        "result_failed": "⚠️ <b>AFSUSKI ÖTA OLMADINGIZ!</b>\nÖtiş bali: 90%. Bilimingizni mustahkamlab, yana qayta topşiring! 💪",
        # Tugmalar yakunida
        "btn_retry": "🔄 Qaytadan işlaş",
        "btn_next_bilet": "➡️ Keyingi bilet ({next_bilet})",
        "btn_review_mistakes": "❌ Xatolarni tahlil qiliş",
        "btn_home": "🏠 Boş menyu",
        # Xatolar bo'limi
        "no_mistakes": (
            "🎉 <b>Ajoyib! Sizda xato qilingan savollar yöq!</b>\n"
            "Biletlarni yoki Imtihon rejimini işlaşda davom eting."
        ),
        "mistakes_start": "❌ <b>Xatolar ustida işlaş:</b>\nSiz oldin xato qilgan {count} ta savol böyiça maşq boşlanmoqda.",
        # Statistika
        "stats_title": (
            "📊 <b>SIZNING ŞAXSIY NATIJALARINGIZ</b>\n\n"
            "👤 <b>Foydalanuvçi:</b> {name}\n"
            "📅 <b>Röyxatdan ötgan:</b> {registered_date}\n\n"
            "🚗 <b>Işlangan testlar soni:</b> {total_tests} ta\n"
            "❓ <b>Yeçilgan barça savollar:</b> {total_questions} ta\n"
            "✅ <b>Töğri berilgan javoblar:</b> {correct_answers} ta\n"
            "❌ <b>Xato berilgan javoblar:</b> {wrong_answers} ta\n"
            "🎯 <b>Örtaça aniqlik foizi:</b> {accuracy}%\n\n"
            "<i>Maşq qilişda davom eting va bilimingizni 100% ga yetkazing!</i>"
        ),
        # Bot haqida
        "help_text": (
            "ℹ️ <b>@AvtoTestUzbBot haqida ma'lumot:</b>\n\n"
            "🚗 <b>Loyiha maqsadi:</b> Özbekistonda haydovçilik guvohnomasini oluvçilar uçun "
            "YHXBB rasmiy imtihoniga mukammal tayyorlaniş imkoniyatini taqdim etiş.\n\n"
            "📱 <b>Mobil ilovamiz:</b> <a href='https://play.google.com/store/apps/details?id=uzbavtotest.complexprogrammer.uz'>Google Play'da Avto Test Uzb</a>\n"
            "🌐 <b>Veb-saytimiz:</b> <a href='https://complexprogrammer.uz/avtotest/?utm_source=telegram&utm_medium=bot&utm_campaign=info'>complexprogrammer.uz</a>\n\n"
            "❓ <b>Savollar va takliflar uçun:</b> @complexprogrammeruzchannel"
        ),
        # Kunlik eslatma
        "remind_on": (
            "⏰ <b>Kunlik eslatma yoqildi!</b>\n\n"
            "Har kuni keçqurun, agar öşa kuni maşq qilmagan bölsangiz, eslatib turamiz. "
            "Öçiriş uçun yana /eslatma yuboring."
        ),
        "remind_off": "🔕 Kunlik eslatma öçirildi. Qayta yoqiş uçun /eslatma yuboring.",
        "ref_info": (
            "🤝 <b>Döstlaringizni taklif qiling!</b>\n\n"
            "Imtihonga tayyorlanayotgan döstlaringizga şu havolani yuboring:\n{link}\n\n"
            "👥 Siz taklif qilganlar: <b>{count}</b> ta"
        ),
        "ref_joined": "🎉 <b>{name}</b> sizning havolangiz orqali qöşildi! Jami taklif qilganlaringiz: <b>{count}</b> ta.",
        "remind_daily": (
            "🚗 <b>Bugungi maşğulot vaqti keldi!</b>\n\n"
            "Imtihonga tayyorgarlikni töxtatmang — kuniga 10 ta savol ham katta natija beradi.\n\n"
            "🎲 /exam — 20 savollik imtihon\n"
            "❌ /mistakes — xatolar ustida işlaş\n"
            "🎯 <a href='https://complexprogrammer.uz/avtotest/imtihon/?utm_source=telegram&utm_medium=bot&utm_campaign=eslatma'>Saytdagi imtihon simulyatori</a>\n\n"
            "<i>Eslatmani öçiriş: /eslatma</i>"
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
            "🌐 <b>Наш сайт:</b> <a href='https://complexprogrammer.uz/avtotest/?utm_source=telegram&utm_medium=bot&utm_campaign=info'>complexprogrammer.uz</a>\n"
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
        "btn_quick": "⚡ Быстрая тренировка (5 вопросов)",
        "quick_title": "⚡ Быстрая тренировка (5 вопросов)",
        "remind_ask": (
            "⏰ <b>Напоминать каждый день?</b>\n\n"
            "Вечером, если вы ещё не занимались в этот день, я пришлю одно короткое сообщение. "
            "10 вопросов в день — самая надёжная подготовка к экзамену."
        ),
        "btn_remind_yes": "✅ Да, напоминай",
        "btn_remind_no": "Не нужно",
        "remind_declined": "Хорошо, напоминаний не будет. Если передумаете: /eslatma",
        "resume_nudge": (
            "📌 Вы остановились на тесте <b>{title}</b> на вопросе {done}/{total}.\n\n"
            "Закончим оставшиеся {left} вопросов?"
        ),
        "btn_resume": "▶️ Продолжить",
        "no_session": "Активный тест не найден. Начните новый из главного меню.",
        "invite_hint": "\n\n🤝 Есть друг, который готовится к экзамену? /taklif",
        # Билеты
        "bilet_title": "🚗 <b>Выберите билет:</b>\n<i>(В каждом билете по 10 вопросов)</i>",
        "page_info": "Страница: {page}/{total_pages}",
        # Процесс теста
        "question_header": "🚗 <b>{title}</b>\n📌 <b>Вопрос {current}/{total}</b>  {bar}\n\n",
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
            "🌐 <b>Наш сайт:</b> <a href='https://complexprogrammer.uz/avtotest/?utm_source=telegram&utm_medium=bot&utm_campaign=info'>complexprogrammer.uz</a>\n\n"
            "❓ <b>Вопросы и поддержка:</b> @complexprogrammeruzchannel"
        ),
        "remind_on": (
            "⏰ <b>Ежедневное напоминание включено!</b>\n\n"
            "Каждый вечер, если вы ещё не занимались в этот день, мы напомним. "
            "Чтобы отключить, снова отправьте /eslatma."
        ),
        "remind_off": "🔕 Ежедневное напоминание отключено. Чтобы включить, отправьте /eslatma.",
        "ref_info": (
            "🤝 <b>Пригласите друзей!</b>\n\n"
            "Отправьте эту ссылку друзьям, которые готовятся к экзамену:\n{link}\n\n"
            "👥 Вы пригласили: <b>{count}</b>"
        ),
        "ref_joined": "🎉 <b>{name}</b> присоединился по вашей ссылке! Всего приглашено: <b>{count}</b>.",
        "remind_daily": (
            "🚗 <b>Время для сегодняшней тренировки!</b>\n\n"
            "Не прерывайте подготовку — даже 10 вопросов в день дают большой результат.\n\n"
            "🎲 /exam — экзамен из 20 вопросов\n"
            "❌ /mistakes — работа над ошибками\n"
            "🎯 <a href='https://complexprogrammer.uz/ru/avtotest/imtihon/?utm_source=telegram&utm_medium=bot&utm_campaign=eslatma'>Симулятор экзамена на сайте</a>\n\n"
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
