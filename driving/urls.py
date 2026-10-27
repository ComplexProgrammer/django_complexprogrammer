from django.urls import path

from driving import views

urlpatterns = [
    path("avtotest/<int:bilet>/<int:raqam>/", views.question, name="avtotest_question"),
    path("avtotest/imtihon/", views.exam, name="avtotest_exam"),
    path("avtotest/imtihon/natija/", views.exam_share, name="avtotest_exam_share"),
    path("avtotest/imtihon/natija.png", views.exam_card, name="avtotest_exam_card"),
    path("avtotest/mavzular/", views.topics_index, name="avtotest_topics"),
    path("avtotest/pdf/", views.avtotest_pdf, name="avtotest_pdf"),
    path("avtotest/kun-savoli/", views.daily_question, name="avtotest_daily"),
    path("avtotest/mavzu/<slug:slug>/", views.topic, name="avtotest_topic"),
    path("avtotest/reyting/", views.leaderboard, name="avtotest_leaderboard"),
    path("yhq/", views.yhq_index, name="yhq"),
    path("yhq/<slug:slug>-bob/", views.yhq_chapter, name="yhq_chapter"),
    path("yol-belgilari/", views.signs, name="road_signs"),
    path("yol-belgilari/<int:pk>/", views.sign, name="road_sign"),
    path("jarimalar/", views.fines, name="fines"),
    path("profil/", views.profile, name="profile"),
    path("auth/telegram/", views.telegram_login, name="telegram_login"),
    path("auth/telegram/webapp/", views.telegram_webapp_login, name="telegram_webapp_login"),
    path("auth/logout/", views.logout_view, name="logout"),
    path("api/avtotest/progress/", views.api_progress, name="api_avtotest_progress"),
    path("api/avtotest/exam/", views.api_exam, name="api_avtotest_exam"),
]
