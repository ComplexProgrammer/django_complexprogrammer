from django.urls import path
# from .views import GetAnswers, GetBooks, GetExchangeRates, GetBilet, GetChangeTextData, GetGroups, GetQuestions, GetSavol, GetTopics, GetTranslateLanguages, GetTranslateResult, TextToSpeech, base, bubbleshooter, car, changetext, duckhunt, exchangerates, ip, motorcycle, pingpong, privacy, projects, project_item, instagram_downloader_, remove_file, remove_file_, send_adstxt, send_app_adstxt, send_bing_site_auth, send_file, send_file_, send_google_verification, send_robots, send_rss, send_sitemap, send_yandex_verification, send_zen_verification, sitemap, snake, snake2, terms, tetris, tictactoe, youtube_downloader_, coins, C0mplexTranslate, ImageCompare, avtotest, avtotest_item, password_generator
from projects import views

urlpatterns=[
    path('', views.base, name='base'),
    path('send_file/', views.send_file, name='send_file'),
    path('remove_file/', views.remove_file, name='remove_file'), # type: ignore
    # path('cartoonize/', views.cartoonize, name='cartoonize' ),
    path('instagram-downloader/', views.instagram_downloader_, name='instagram_downloader_' ), # type: ignore
    path('youtube_downloader/', views.youtube_downloader_, name='youtube_downloader'), # type: ignore
    path('coins/', views.coins, name='coins'),
    path('GetTranslateLanguages/', views.GetTranslateLanguages, name='GetTranslateLanguages'),
    path('TextToSpeech/', views.TextToSpeech, name='TextToSpeech'),
    path('GetTranslateResult/', views.GetTranslateResult, name='GetTranslateResult'),
    path('translate/', views.C0mplexTranslate, name='translate'),
    path('imagecompare/', views.ImageCompare, name='imagecompare'), # type: ignore
    path('avtotest/', views.avtotest, name='avtotest'),
    path('avtotest/<int:bilet>/', views.avtotest_item, name='avtotest'),
    path('GetSavol/', views.GetSavol, name='GetSavol'),
    path('GetBilet/', views.GetBilet, name='GetBilet'),
    path('exchangerates/', views.exchangerates, name='exchangerates'),
    path('GetExchangeRates/', views.GetExchangeRates, name='GetExchangeRates'),
    path('changetext/', views.changetext, name='changetext'),
    path('GetChangeTextData/', views.GetChangeTextData, name='GetChangeTextData'), # type: ignore
    path('ip/', views.ip, name='ip'),
    path('map',views.map, name="map"),
    path('password_generator/', views.password_generator, name='password_generator'),
    path('sitemap/', views.sitemap, name='sitemap'),
    path('snake/', views.snake, name='snake'),
    path('snake2/', views.snake2, name='snake2'),
    path('car/', views.car, name='car'),
    path('duckhunt/', views.duckhunt, name='duckhunt'),
    path('motorcycle/', views.motorcycle, name='motorcycle'),
    path('bubbleshooter/', views.bubbleshooter, name='bubbleshooter'),
    path('pingpong/', views.pingpong, name='pingpong'),
    path('tictactoe/', views.tictactoe, name='tictactoe'),
    path('tetris/', views.tetris, name='tetris'),
    path('terms/', views.terms, name='terms'),
    path('privacy/', views.privacy, name='privacy'),
    path('yandex_6bd5e2cc7d84e7b1.html/', views.send_yandex_verification, name='send_yandex_verification'),
    path('googleed00602540a61448.html/', views.send_google_verification, name='send_google_verification'),
    path('zen_7l9bCOKi66HKyY4ilLYmulKUQTlrZLJrS3HSjTiMhq0GoD4ap8COxE7Bjw1oYf26.html/', views.send_zen_verification, name='send_zen_verification'),
    path('sitemap.xml/', views.send_sitemap, name='send_sitemap'),
    path('BingSiteAuth.xml/', views.send_bing_site_auth, name='send_bing_site_auth'),
    path('rss.xml/', views.send_rss, name='send_rss'),
    path('app-ads.txt/', views.send_app_adstxt, name='send_app_adstxt'),
    path('ads.txt/', views.send_adstxt, name='send_adstxt'),
    path('robots.txt/', views.send_robots, name='send_robots'),
    
    path('projects/', views.projects, name='projects'),
    path('project/<int:id>/', views.project_item, name='item'),


    # path('GetGroups/', views.GetGroups, name='GetGroups'),
    # path('GetBooks/', views.GetBooks, name='GetBooks'), # type: ignore
    # path('GetTopics/', views.GetTopics, name='GetTopics'), # type: ignore
    # path('GetQuestions/', views.GetQuestions, name='GetQuestions'), # type: ignore
    # path('GetAnswers/', views.GetAnswers, name='GetAnswers'), # type: ignore
]