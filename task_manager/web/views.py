from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.utils.translation import gettext as _


class IndexView(View):
    def get(self, request):
        return render(request, 'pages/index.html')
