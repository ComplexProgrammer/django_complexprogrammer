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
    print(htmlSource)
    context={
        'data':htmlSource
    }
    return render(request, 'site_clones/index.html', context=context)

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
    return render(request, 'site_clones/index.html', context=context)

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
    return render(request, 'site_clones/index.html', context=context)

def postda_uz(request):
    http = urllib3.PoolManager()
    r = http.request('GET', 'https://postda.uz')
    htmlSource = r.data.decode('utf-8')
    print(htmlSource)
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
    print(htmlSource)
    context={
        'data':htmlSource
    }
    return render(request, 'site_clones/postda.html', context=context)