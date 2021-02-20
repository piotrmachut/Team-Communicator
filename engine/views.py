from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout

# Create your views here.

class LoggedOut(View):

    def get(self, request):
        return render(request, 'successful_logout.html')


class IndexView(View):

    def get(self, request):
        return render(request, 'index.html')


class Profile(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        user_id = request.user.id
        user_name = request.user.first_name
        ctx = {
            'my_name': user_id,
            'user_name': user_name,
        }
        return render(request, 'profile.html', context=ctx)


class ProfileSettings(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    def get(sefl, request):
        return HttpResponse('Profile settings view test')


class TeamChannel(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request, id):
        return HttpResponse('Team view test')


class TeamAdd(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        return HttpResponse('Team add test')


class TeamSettings(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request, id):
        return HttpResponse('Team settings test')
