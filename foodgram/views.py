from django.shortcuts import render


def page_not_found(request, exception=None):
    return render(request, '404.html', status=404)


def server_error(request):
    return render(request, 'misc/500.html', status=500)
