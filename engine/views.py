from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.contrib.auth.models import User
from .models import *
from django.db import models

# Create your views here.

class LoggedOut(View):

    def get(self, request):
        return render(request, 'successful_logout.html')


class IndexView(View):

    def get(self, request):
        return render(request, 'index.html')


class SignUp(View):

    def get(self, request):
        return render(request, 'registration/signup.html')
    
    def post(self, request):
        new_username = request.POST.get('username')
        new_first_name = request.POST.get('first_name')
        new_last_name = request.POST.get('last_name')
        new_email = request.POST.get('email')
        new_password = request.POST.get('password')
        User.objects.create_user(
            username=new_username, 
            first_name=new_first_name, 
            last_name=new_last_name,
            email=new_email,
            password=new_password
            )
        return HttpResponseRedirect('/accounts/profile/')


class Profile(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    def get(self, request):
        sender = request.user.id
        sender_name = request.user.first_name
        team_channels_list = Team.objects.all().order_by('id') # TODO All teams not teams related to user
        messages_list = MainChannelMessage.objects.all().select_related('sender').order_by('id')
        ctx = {
            'sender_name': sender_name,
            'team_channels_list': team_channels_list,
            'messages_list': messages_list
        }
        return render(request, 'profile.html', context=ctx)
    
    def post(self, request):
        sender = request.user.id
        new_message = request.POST.get('message_field')
        database_record = MainChannelMessage(message=new_message, sender_id=sender)
        database_record.save()
        return HttpResponseRedirect('/accounts/profile/')


class ProfileSettings(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    def get(sefl, request):
        return render(request, 'profile_settings.html')
    
    def post(self, request):
        sender_first_name = request.POST.get('first_name')
        sender_last_name = request.POST.get('last_name')
        sender_email = request.POST.get('email')
        database_record = User.objects.get(pk=request.user.id)
        database_record.first_name = sender_first_name
        database_record.last_name = sender_last_name
        database_record.email = sender_email
        database_record.save()
        database_record_succes = True
        ctx = {
            'info': database_record_succes
        }
        return render(request, 'profile_settings.html', context=ctx)


class ProfileDelete(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        return render(request, 'profile_settings_delete.html')
    
    def post(self, request):
        database_record = User.objects.get(pk=request.user.id)
        database_record.delete()
        return HttpResponseRedirect(f'/accounts/login/')


class TeamChannel(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request, id):
        team = Team.objects.get(pk=id)
        sender = request.user.id
        sender_name = request.user.first_name
        messages_list = TeamMessage.objects.select_related('sender').filter(team_id=id)
        ctx = {
            'team': team,
            'sender_name': sender_name,
            'messages_list': messages_list
        }
        return render(request, 'team_channel.html', context=ctx)
    
    def post(self, request, id):
        sender = request.user.id
        new_message = request.POST.get('message_field')
        team_id = request.POST.get('team_id')
        database_record = TeamMessage(message=new_message, sender_id=sender, team_id=id)
        database_record.save()
        return HttpResponseRedirect(f'/accounts/team/{id}/')


class TeamAdd(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        team_channels_list = Team.objects.all().order_by('id') # TODO All teams not teams related to user
        ctx = {
            'team_channels_list': team_channels_list,
        }
        return render(request, 'team_add.html', context=ctx)
    
    def post(self, request):
        team_name = request.POST.get('team_name')
        team_description = request.POST.get('team_description')
        team_owner = request.user.id
        database_user_record = User.objects.get(pk=team_owner)
        database_team_record = Team(name=team_name, description=team_description, owner_id=team_owner)
        database_team_record.save()
        database_team_record.users.add(database_user_record)
        return HttpResponseRedirect(f'/accounts/team/{database_team_record.id}/')


class TeamSettings(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request, id):
        team = Team.objects.get(pk=id)
        ctx = {
            'team': team,
        }
        return render(request, 'team_settings.html', context=ctx)


class TeamSettingsEdit(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request, id):
        team = Team.objects.get(pk=id)
        owner = team.owner_id
        sender = request.user.id
        if owner == sender:
            ctx = {
                'team': team,
            }
            return render(request, 'team_settings_edit.html', context=ctx)
        else:
            ctx = {
                'team': team,
            }
            return render(request, 'team_settings_denied.html', context=ctx)
            
    
    def post(self, request, id): # TODO if do posta
        team = Team.objects.get(pk=id)
        owner = team.owner_id
        sender = request.user.id
        if owner == sender:
            team.name = request.POST.get('team_name')
            team.description = request.POST.get('team_description')
            team.save()
            return HttpResponseRedirect(f'/accounts/team/settings/{team.id}/')
        else:
            ctx = {
                'team': team,
            }
            return render(request, 'team_settings_denied.html', context=ctx)


class TeamSettingsAddUser(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request, id):
        team = Team.objects.get(pk=id)
        owner = team.owner_id
        sender = request.user.id
        if owner == sender:
            ctx = {
                'team': team,
            }
            return HttpResponse('nowy użytkownik')
        else:
            ctx = {
                'team': team,
            }
            return render(request, 'team_settings_denied.html', context=ctx)
    
    def post(self, request, id):
        pass


class TeamSettingsDelete(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request, id):
        team = Team.objects.get(pk=id)
        owner = team.owner_id
        sender = request.user.id
        if owner == sender:
            ctx = {
                'team': team,
            }
            return render(request, 'team_settings_delete.html', context=ctx)
        else:
            ctx = {
                'team': team,
            }
            return render(request, 'team_settings_denied.html', context=ctx)
    
    def post(self, request, id):
        team = Team.objects.get(pk=id)
        owner = team.owner_id
        sender = request.user.id
        if owner == sender:
            team.delete()
            return HttpResponseRedirect(f'/accounts/profile/')
        else:
            ctx = {
                'team': team,
            }
            return render(request, 'team_settings_denied.html', context=ctx)
