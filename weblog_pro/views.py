from django.shortcuts import render
from WebLogSetting.models import Site_Setting, photo_page
from WebLog.models import web_log


def nav(request):
    sitesetting = Site_Setting.objects.first()

    contex = {'setting': sitesetting}
    return render(request, 'Header/navbar.html', contex)


def footer(request, *args, **kwargs):
    sitesetting = Site_Setting.objects.first()
    last_weblog = web_log.objects.filter(is_active=True,is_delete=False).order_by('-date')[:2]
    context = {'setting': sitesetting, 'weblog': last_weblog}
    return render(request, 'Footer/footer.html', context)


def test(request):
    salam=web_log.objects.get(pk=2)
    x=salam.gallery
    return render(request, '503.html', {})
