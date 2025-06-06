"""django_complexprogrammer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve
from django.conf.urls.i18n import i18n_patterns
from django.views.generic import RedirectView
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', include('projects.urls')),
#     path('', include('tests.urls')),
#     path('', include('pdf_tools.urls')),
#     path('markets/', include('markets.urls')),
#     path('news/', include('news.urls')),
#     re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
# ]
urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += [path('i18n/', include('django.conf.urls.i18n')),]
urlpatterns = [
    *i18n_patterns(*urlpatterns, prefix_default_language=False),
    ]
urlpatterns += [re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT, }), ]
if settings.DEBUG:
    urlpatterns +=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += [
    path('admin/', admin.site.urls),
    path('', include('projects.urls')),
    #path('avtotest/', views.tests),
    # path('avtotest/', RedirectView.as_view(url='/tests/?book_id=49', permanent=True)),
    path('', include('tests.urls')),
    path('tests/', include('tests.urls')),
    path('pdf_tools', include('pdf_tools.urls')),
    path('markets/', include('markets.urls')),
    path('news/', include('news.urls')),
    path('blog/', include('blog.urls')),
    path('', include('comments.urls')),
    path('cryptomarket/', include('cryptomarket.urls')),
    path('site_clones/', include('site_clones.urls')),
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
]