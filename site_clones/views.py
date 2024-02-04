from django.shortcuts import render
import urllib3

from news.models import Posts

def index(request):
    url = request.GET.get('url', False);
    if url == False:
        return render(request, 'site_clones/index.html')
    http = urllib3.PoolManager()
    r = http.request('GET', url)
    htmlSource = r.data.decode('utf-8')
    context={
        'data':htmlSource
    }
    return render(request, 'site_clones/myclonedsites.html', context=context)

def myclonedsites(request):
    url = request.GET.get('url', False);
    if url == False:
        return render(request, 'site_clones/myclonedsites.html')
    http = urllib3.PoolManager()
    r = http.request('GET', url)
    htmlSource = r.data.decode('utf-8')
    context={
        'data':htmlSource
    }
    return render(request, 'site_clones/myclonedsites.html', context=context)
def uzinfobiz_ru(request):
    http = urllib3.PoolManager()
    r = http.request('GET', 'https://uzinfobiz.ru')
    htmlSource = r.data.decode('utf-8')
    htmlSource = htmlSource.replace("<title>Oxunjon Gaybullaev blogi | Sayt yaratish va pul ishlash</title>", "<title>Complex Programmer | Sayt yaratish va pul ishlash</title>");
    htmlSource = htmlSource.replace("https://uzinfobiz.ru/wp-content/uploads/2018/03/icon.png", "https://complexprogrammer.uz/static/img/favicon.ico");
    htmlSource = htmlSource.replace("9267084582248929", "7773722896374259");
    htmlSource = htmlSource.replace("2740347621802453", "7773722896374259");
    htmlSource = htmlSource.replace("http://uzinfobiz.ru/wp-content/uploads/2018/11/logo4.png", "https://complexprogrammer.uz/static/img/C0mplex.png");
    context={
        'data':htmlSource
    }
    return render(request, 'site_clones/myclonedsites.html', context=context)

def uzinterbiz_com(request):
    http = urllib3.PoolManager()
    r = http.request('GET', 'https://uzinterbiz.com')
    htmlSource = r.data.decode('utf-8')
    htmlSource = htmlSource.replace("<title>Умиджон Обудов | Интернет оркали масофадан туриб ишлаш</title>", "<title>Complex Programmer | Интернет оркали масофадан туриб ишлаш</title>");
    htmlSource = htmlSource.replace("https://uzinterbiz.com/wp-content/uploads/2019/01/Favicon.png", "https://complexprogrammer.uz/static/img/favicon.ico");
    htmlSource = htmlSource.replace("https://uzinterbiz.com/favicon.ico", "https://complexprogrammer.uz/static/img/favicon.ico");
    htmlSource = htmlSource.replace("9267084582248929", "7773722896374259");
    htmlSource = htmlSource.replace("2740347621802453", "7773722896374259");
    htmlSource = htmlSource.replace("http://uzinfobiz.ru/wp-content/uploads/2018/11/logo4.png", "https://complexprogrammer.uz/static/img/C0mplex.png");
    htmlSource = htmlSource.replace("Блог Умиджона Обудова", "Complex Programmer");
    htmlSource = htmlSource.replace("Блог Умиджон Обудова", '<img width="100" height="50" src="https://complexprogrammer.uz/static/img/C0mplex.png" class="attachment-thumb-wide size-thumb-wide wp-post-image" alt="Talabalar uchun ish" itemprop="image" decoding="async"/> Complex Programmer');
    context={
        'data':htmlSource
    }
    return render(request, 'site_clones/myclonedsites.html', context=context)

def postda_uz(request):
    http = urllib3.PoolManager()
    r = http.request('GET', 'https://postda.uz')
    htmlSource = r.data.decode('utf-8')
    htmlSource = htmlSource.replace("/img/logo.106cf606.png", "https://postda.uz/img/logo.106cf606.png");
    htmlSource = htmlSource.replace("/img/loader.2e487c0b.svg", "https://postda.uz/img/loader.2e487c0b.svg");
    htmlSource = htmlSource.replace("/img/prev-arrow-dark.93f00cb2.svg", "https://postda.uz/img/prev-arrow-dark.93f00cb2.svg");
    htmlSource = htmlSource.replace("/img/next-arrow-dark.7fc897ce.svg", "https://postda.uz/img/next-arrow-dark.7fc897ce.svg");
    htmlSource = htmlSource.replace("/img/mobile-helper-icon1.d5c845b7.svg", "https://postda.uz/img/mobile-helper-icon1.d5c845b7.svg");
    htmlSource = htmlSource.replace("/img/mobile-helper-icon3.091d9085.svg", "https://postda.uz/img/mobile-helper-icon3.091d9085.svg");
    htmlSource = htmlSource.replace("/img/hand.db6c1fe8.png", "https://postda.uz/img/hand.db6c1fe8.png");
    htmlSource = htmlSource.replace("/img/mobile-helper-icon2.c30353a3.svg", "https://postda.uz/img/mobile-helper-icon2.c30353a3.svg");
    htmlSource = htmlSource.replace("/img/vazirlik-logo.6eb55495.png", "https://postda.uz/img/vazirlik-logo.6eb55495.png");
    htmlSource = htmlSource.replace("/img/google-store.2faad93d.png", "https://postda.uz/img/google-store.2faad93d.png");
    htmlSource = htmlSource.replace("/img/app-store.f7bda152.png", "https://postda.uz/img/app-store.f7bda152.png");
    htmlSource = htmlSource.replace("/img/prev-arrow.699ece16.svg", "https://postda.uz/img/prev-arrow.699ece16.svg");
    htmlSource = htmlSource.replace("/img/next-arrow.65166a23.svg", "https://postda.uz/img/next-arrow.65166a23.svg");
    htmlSource = htmlSource.replace("https://api.mtsh.uz/uploads/IMG_20231116_171720_2838e145be.jpg", "https://complexprogrammer.uz/static/img/C0mplex.png");
    # htmlSource = htmlSource.replace("", "https://postda.uz");
    # htmlSource = htmlSource.replace("", "https://postda.uz");
    # htmlSource = htmlSource.replace("", "https://postda.uz");
    # htmlSource = htmlSource.replace("", "https://postda.uz");
    # htmlSource = htmlSource.replace("", "https://postda.uz");
    # htmlSource = htmlSource.replace("", "https://postda.uz");
    # htmlSource = htmlSource.replace("", "https://postda.uz");
    # htmlSource = htmlSource.replace("", "https://postda.uz");
    # htmlSource = htmlSource.replace("", "https://postda.uz");
    # htmlSource = htmlSource.replace("", "https://postda.uz");
    # htmlSource = htmlSource.replace("", "https://postda.uz");
    # htmlSource = htmlSource.replace("<title>Умиджон Обудов | Интернет оркали масофадан туриб ишлаш</title>", "<title>Complex Programmer | Интернет оркали масофадан туриб ишлаш</title>");
    # htmlSource = htmlSource.replace("https://uzinterbiz.com/wp-content/uploads/2019/01/Favicon.png", "https://complexprogrammer.uz/static/img/favicon.ico");
    # htmlSource = htmlSource.replace("https://uzinterbiz.com/favicon.ico", "https://complexprogrammer.uz/static/img/favicon.ico");
    # htmlSource = htmlSource.replace("9267084582248929", "7773722896374259");
    # htmlSource = htmlSource.replace("2740347621802453", "7773722896374259");
    # htmlSource = htmlSource.replace("http://uzinfobiz.ru/wp-content/uploads/2018/11/logo4.png", "https://complexprogrammer.uz/static/img/C0mplex.png");
    # htmlSource = htmlSource.replace("Блог Умиджона Обудова", "Complex Programmer");
    # htmlSource = htmlSource.replace("Блог Умиджон Обудова", '<img width="100" height="50" src="https://complexprogrammer.uz/static/img/C0mplex.png" class="attachment-thumb-wide size-thumb-wide wp-post-image" alt="Talabalar uchun ish" itemprop="image" decoding="async"/> Complex Programmer');
    context={
        'data':htmlSource
    }
    return render(request, 'site_clones/postda.html', context=context)

def konsta_uz(request):
    http = urllib3.PoolManager()
    r = http.request('GET', 'https://konsta.uz')
    htmlSource = r.data.decode('utf-8')
    htmlSource = htmlSource.replace("8388915255381447", "7773722896374259");
    htmlSource = htmlSource.replace("<title>OFFICIAL WEB SITE OF KONSTA</title>", "<title>Complex Programmer | KONSTA</title>");
    htmlSource = htmlSource.replace("https://uzinterbiz.com/wp-content/uploads/2019/01/Favicon.png", "https://complexprogrammer.uz/static/img/favicon.ico");
    htmlSource = htmlSource.replace("img/favicon.png", "https://complexprogrammer.uz/static/img/favicon.ico");
    htmlSource = htmlSource.replace("css/normalize.css", "https://konsta.uz/css/normalize.css");
    htmlSource = htmlSource.replace("css/main.css", "https://konsta.uz/css/main.css");
    htmlSource = htmlSource.replace("css/animate.min.css", "https://konsta.uz/css/animate.min.css");
    htmlSource = htmlSource.replace("css/fontawesome-all.min.css", "https://konsta.uz/css/fontawesome-all.min.css");
    htmlSource = htmlSource.replace("css/bootstrap.min.css", "https://konsta.uz/css/bootstrap.min.css");
    htmlSource = htmlSource.replace("img/figure/bell-icon.png", "https://konsta.uz/img/figure/bell-icon.png");
    htmlSource = htmlSource.replace("js/modernizr-3.6.0.min.js", "https://konsta.uz/js/modernizr-3.6.0.min.js");
    htmlSource = htmlSource.replace("js/jquery-3.3.1.min.js", "https://konsta.uz/js/jquery-3.3.1.min.js");
    htmlSource = htmlSource.replace("js/popper.min.js", "https://konsta.uz/js/popper.min.js");
    htmlSource = htmlSource.replace("js/bootstrap.min.js", "https://konsta.uz/js/bootstrap.min.js");
    htmlSource = htmlSource.replace("vendor/vegas/vegas.min.css", "https://konsta.uz/vendor/vegas/vegas.min.css");
    htmlSource = htmlSource.replace("vendor/vegas/vegas.min.js", "https://konsta.uz/vendor/vegas/vegas.min.js");
    htmlSource = htmlSource.replace("js/pace.min.js", "https://konsta.uz/js/pace.min.js");
    htmlSource = htmlSource.replace("js/main.js", "https://konsta.uz/js/main.js");
    htmlSource = htmlSource.replace("style.css", "https://konsta.uz/style.css");
    htmlSource = htmlSource.replace("img/figure/bg3.jpg", "img/k2.png");
    htmlSource = htmlSource.replace("https://www.youtube.com/@Konsta_uz", "https://www.youtube.com/@C0mplex224");
    htmlSource = htmlSource.replace("https://konsta.uz/img/figure/bg3.jpg", "https://complexprogrammer.uz/static/img/C0mplex.png");
    htmlSource = htmlSource.replace('<p>© 2020 - 2022 <a href="http://t.me/jahongirFm">JSD WEB SECURITY </a> — All rights reserved.</p>', '<p>© 2020 - 2023 <a href="http://t.me/ComplexProgrammer">Complex Programmer </a> — All rights reserved.</p>');
    htmlSource = htmlSource.replace('http://t.me/konstainfo', 'http://t.me/ComplexProgrammer');
    htmlSource = htmlSource.replace("https://t.me/konsta", "https://t.me/ComplexProgrammer");
    htmlSource = htmlSource.replace("https://www.instagram.com/konsta_uz/", "https://www.instagram.com/complexprogrammer");
    context={
        'data':htmlSource
    }
    return render(request, 'site_clones/myclonedsites.html', context=context)