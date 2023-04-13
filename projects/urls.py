from django.urls import path
from .views import GetChangeTextData, GetSavol, base, changetext, exchangerates, ip, projects, project_item, instagram_downloader_, sitemap, youtube_downloader_, coins, C0mplexTranslate, ImageCompare, avtotest, password_generator

urlpatterns=[
    path('', base, name='base'),
    # path('cartoonize/', cartoonize, name='cartoonize' ),
    path('instagram-downloader', instagram_downloader_, name='instagram_downloader_' ),
    path('youtube_downloader', youtube_downloader_, name='youtube_downloader'),
    path('coins', coins, name='coins'),
    path('translate', C0mplexTranslate, name='translate'),
    path('imagecompare', ImageCompare, name='imagecompare'),
    path('avtotest', avtotest, name='avtotest'),
    path('GetSavol', GetSavol, name='GetSavol'),
    path('exchangerates', exchangerates, name='exchangerates'),
    path('changetext', changetext, name='changetext'),
    path('GetChangeTextData/<str:text>', GetChangeTextData, name='GetChangeTextData'),
    path('ip', ip, name='ip'),
    path('password_generator', password_generator, name='password_generator'),
    path('sitemap', sitemap, name='sitemap'),
    path('projects/', projects, name='projects'),
    path('project/<int:id>/', project_item, name='item')
]
