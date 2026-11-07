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
from arxiv.views import archive_document

# Arxiv hujjatlari umumiy /media/ dan oldin tekshiriladi (yopiq hujjatlar faqat xodimlarga)
urlpatterns = [re_path(r"^media/arxiv/documents/(?P<path>.+)$", archive_document)]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
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
    path("favicon.ico", RedirectView.as_view(url="/static/img/favicon.ico", permanent=True)),
    path(".well-known/traffic-advice", core_views.traffic_advice, name="traffic_advice"),
    path(".well-known/traffic-advice/", core_views.traffic_advice),
    re_path(r"^static/avtotest/\{\{.*$", core_views.empty_204),
    re_path(r"^site_clones(?:/.*)?$", RedirectView.as_view(url="/projects/", permanent=True)),
    path("sitemap.xml", core_views.sitemap_xml, name="sitemap_xml"),
    path("sitemap.xml/", core_views.sitemap_xml),
    re_path(r"^sitemap-(?P<slug>[a-z]+)\.xml$", core_views.sitemap_section_xml, name="sitemap_section_xml"),
    path("post-sitemap.xml", RedirectView.as_view(url="/sitemap-blog.xml", permanent=True)),
    path("product-sitemap.xml", RedirectView.as_view(url="/sitemap-loyihalar.xml", permanent=True)),
    re_path(
        r"^(?:category-sitemap|author-sitemap|wp-sitemap-users-1|sitemap_agentic_discovery)\.xml$",
        RedirectView.as_view(url="/sitemap.xml", permanent=True),
    ),
    path("sitemap.rss", RedirectView.as_view(url="/rss.xml/", permanent=True)),
    path("rss.xml", RedirectView.as_view(url="/rss.xml/", permanent=True)),
    path("robots.txt", core_views.robots_txt, name="robots_txt"),
    re_path(r"^(?P<key>[0-9a-f]{32})\.txt$", core_views.indexnow_key, name="indexnow_key"),
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
    # "BTC Markets" loyihasining manzili (bazada url="market") — kripto bozorlar sahifasi
    path("market", RedirectView.as_view(url="/cryptomarket/", permanent=True)),
    path("market/", RedirectView.as_view(url="/cryptomarket/", permanent=True)),
    path("news/", include("news.urls")),
    path("blog/", include("blog.urls")),
    path("", include("comments.urls")),
    path("cryptomarket/", include("cryptomarket.urls")),
    path("", include("arxiv.urls")),
    re_path(r"^ckeditor/", include("ckeditor_uploader.urls")),
]
if getattr(settings, "CKEDITOR5_ENABLED", False):
    urlpatterns.append(path("ckeditor5/", include("django_ckeditor_5.urls")))
