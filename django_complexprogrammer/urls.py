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
from django.views.generic import RedirectView

from core import views as core_views
from tests import views as tests_views

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
urlpatterns += [
    path("i18n/", include("django.conf.urls.i18n")),
]
# Til URL prefiksi (/ru/...) bilan emas, cookie (django_language) orqali tanlanadi.
# i18n_patterns(prefix_default_language=False) ishlatilsa, Django prefikssiz
# sahifalarda cookie'ni e'tiborsiz qoldirib doim LANGUAGE_CODE'ni yoqadi.
urlpatterns += [
    re_path(
        r"^media/(?P<path>.*)$",
        serve,
        {
            "document_root": settings.MEDIA_ROOT,
        },
    ),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += [
    path("admin/", admin.site.urls),
    path("sitemap.xml", core_views.sitemap_xml, name="sitemap_xml"),
    path("sitemap.xml/", core_views.sitemap_xml),
    path("robots.txt", core_views.robots_txt, name="robots_txt"),
    path("robots.txt/", core_views.robots_txt),
    path("search/", core_views.search, name="search"),
    path("sw.js", core_views.service_worker, name="service_worker"),
    path("offline/", core_views.offline, name="offline"),
    path("", include("driving.urls")),
    path("", include("projects.urls")),
    # path('avtotest/', views.tests),
    # path('avtotest/', RedirectView.as_view(url='/tests/?book_id=49', permanent=True)),
    path("tests/xatolar/", tests_views.tests_mistakes, name="tests_mistakes"),
    path("", include("tests.urls")),
    path("tests/", include("tests.urls")),
    path("pdf_tools/", include("pdf_tools.urls")),
    path("markets/", include("markets.urls")),
    path("news/", include("news.urls")),
    path("blog/", include("blog.urls")),
    path("", include("comments.urls")),
    path("cryptomarket/", include("cryptomarket.urls")),
    path("site_clones/", include("site_clones.urls")),
    path("", include("arxiv.urls")),
    re_path(r"^ckeditor/", include("ckeditor_uploader.urls")),
]
