from django.urls import path
from .views import GetAnswers, GetBooks, GetExchangeRates, GetBilet, GetChangeTextData, GetGroups, GetQuestions, GetSavol, GetTopics, GetTranslateLanguages, GetTranslateResult, TextToSpeech, base, bubbleshooter, car, changetext, duckhunt, exchangerates, ip, motorcycle, pingpong, privacy, projects, project_item, instagram_downloader_, remove_file, remove_file_, send_adstxt, send_bing_site_auth, send_file, send_file_, send_google_verification, send_robots, send_rss, send_sitemap, send_yandex_verification, send_zen_verification, sitemap, snake, snake2, terms, tetris, tictactoe, youtube_downloader_, coins, C0mplexTranslate, ImageCompare, avtotest, avtotest_item, password_generator

urlpatterns=[
    path('', base, name='base'),
    path('send_file/', send_file, name='send_file'),
    path('remove_file/', remove_file, name='remove_file'), # type: ignore
    # path('cartoonize/', cartoonize, name='cartoonize' ),
    path('instagram-downloader/', instagram_downloader_, name='instagram_downloader_' ), # type: ignore
    path('youtube_downloader/', youtube_downloader_, name='youtube_downloader'), # type: ignore
    path('coins/', coins, name='coins'),
    path('GetTranslateLanguages/', GetTranslateLanguages, name='GetTranslateLanguages'),
    path('TextToSpeech/', TextToSpeech, name='TextToSpeech'),
    path('GetTranslateResult/', GetTranslateResult, name='GetTranslateResult'),
    path('translate/', C0mplexTranslate, name='translate'),
    path('imagecompare/', ImageCompare, name='imagecompare'), # type: ignore
    path('avtotest/', avtotest, name='avtotest'),
    path('avtotest/<int:bilet>/', avtotest_item, name='avtotest'),
    path('static/avtotest/<str>', tetris, name='avtotest'),
    path('GetSavol/', GetSavol, name='GetSavol'),
    path('GetBilet/', GetBilet, name='GetBilet'),
    path('exchangerates/', exchangerates, name='exchangerates'),
    path('GetExchangeRates/', GetExchangeRates, name='GetExchangeRates'),
    path('changetext/', changetext, name='changetext'),
    path('GetChangeTextData/', GetChangeTextData, name='GetChangeTextData'), # type: ignore
    path('ip/', ip, name='ip'),
    path('password_generator/', password_generator, name='password_generator'),
    path('sitemap/', sitemap, name='sitemap'),
    path('snake/', snake, name='snake'),
    path('snake2/', snake2, name='snake2'),
    path('car/', car, name='car'),
    path('duckhunt/', duckhunt, name='duckhunt'),
    path('motorcycle/', motorcycle, name='motorcycle'),
    path('bubbleshooter/', bubbleshooter, name='bubbleshooter'),
    path('pingpong/', pingpong, name='pingpong'),
    path('tictactoe/', tictactoe, name='tictactoe'),
    path('tetris/', tetris, name='tetris'),
    path('terms/', terms, name='terms'),
    path('privacy/', privacy, name='privacy'),
    path('yandex_6bd5e2cc7d84e7b1.html/', send_yandex_verification, name='send_yandex_verification'),
    path('googleed00602540a61448.html/', send_google_verification, name='send_google_verification'),
    path('zen_7l9bCOKi66HKyY4ilLYmulKUQTlrZLJrS3HSjTiMhq0GoD4ap8COxE7Bjw1oYf26.html/', send_zen_verification, name='send_zen_verification'),
    path('sitemap.xml/', send_sitemap, name='send_sitemap'),
    path('BingSiteAuth.xml/', send_bing_site_auth, name='send_bing_site_auth'),
    path('rss.xml/', send_rss, name='send_rss'),
    path('app-ads.txt/', send_adstxt, name='send_adstxt'),
    path('robots.txt/', send_robots, name='send_robots'),
    
    path('projects/', projects, name='projects'),
    path('project/<int:id>/', project_item, name='item'),


    path('GetGroups/', GetGroups, name='GetGroups'),
    path('GetBooks/', GetBooks, name='GetBooks'), # type: ignore
    path('GetTopics/', GetTopics, name='GetTopics'), # type: ignore
    path('GetQuestions/', GetQuestions, name='GetQuestions'), # type: ignore
    path('GetAnswers/', GetAnswers, name='GetAnswers'), # type: ignore
]
