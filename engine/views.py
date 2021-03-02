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
        """Render view with confirmation of succesfull log out."""
        return render(request, 'successful_logout.html')


class IndexView(View):

    def get(self, request):
        """Render landing page of application."""
        return render(request, 'index.html')


class SignUp(View):

    def get(self, request):
        """Render sign up form."""
        return render(request, 'registration/signup.html')
    
    def post(self, request):
        """Create new user in auth_user database table and render main page."""
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
    """View available after successful user authorization."""
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        """Render site with main chat channell."""
        sender = request.user.id
        sender_name = request.user.first_name
        team_channels_list = Team.objects.all().order_by('id')
        messages_list = MainChannelMessage.objects.all().select_related('sender').order_by('id')
        ctx = {
            'sender_name': sender_name,
            'team_channels_list': team_channels_list,
            'messages_list': messages_list
        }
        return render(request, 'profile.html', context=ctx)
    
    def post(self, request):
        """Save new message to MainChannelMessage table with the id of the authorized user. Redirect to view from GET method."""
        sender = request.user.id
        new_message = request.POST.get('message_field')
        database_record = MainChannelMessage(message=new_message, sender_id=sender)
        database_record.save()
        return HttpResponseRedirect('/accounts/profile/')


class ProfileSettings(LoginRequiredMixin, View):
    """View available after successful user authorization."""
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    def get(sefl, request):
        """Render profile settings form of authorized user."""
        return render(request, 'profile_settings.html')
    
    def post(self, request):
        """Update data of authorized user in auth_user database table. Redirect to view from GET method."""
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
    """View available after successful user authorization."""
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        """Render view with user delete confirmation."""
        return render(request, 'profile_settings_delete.html')
    
    def post(self, request):
        """Delete user and redirect to log in form."""
        database_record = User.objects.get(pk=request.user.id)
        database_record.delete()
        return HttpResponseRedirect(f'/accounts/login/')


class TeamChannel(LoginRequiredMixin, View):
    """View available after successful user authorization."""
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request, id):
        """Render view with team messages channel.
        Keyword arguments:

        id -- parameter passed with GET method from Profile view. Id of a team.
        """
        team = Team.objects.get(pk=id)
        assigned_users_list = Team.objects.get(pk=id).users.all()
        if request.user in assigned_users_list:
            sender = request.user.id
            sender_name = request.user.first_name
            messages_list = TeamMessage.objects.select_related('sender').filter(team_id=id)
            ctx = {
                'team': team,
                'sender_name': sender_name,
                'messages_list': messages_list
            }
            return render(request, 'team_channel.html', context=ctx)
        else:
            ctx = {
                'team': team
            }
            return render(request, 'team_denied.html', context=ctx)
    
    def post(self, request, id):
        """Save new message record to TeamMessage database table. Redirect to view form GET method."""
        sender = request.user.id
        new_message = request.POST.get('message_field')
        team_id = request.POST.get('team_id')
        database_record = TeamMessage(message=new_message, sender_id=sender, team_id=id)
        database_record.save()
        return HttpResponseRedirect(f'/accounts/team/{id}/')


class TeamAdd(LoginRequiredMixin, View):
    """View is available after successful user authorization"""
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        """Render view with new channel form."""
        team_channels_list = Team.objects.all().order_by('id') # TODO All teams not teams related to user
        ctx = {
            'team_channels_list': team_channels_list,
        }
        return render(request, 'team_add.html', context=ctx)
    
    def post(self, request):
        """Create new record in Team database table. Create relation between team creator and team members table."""
        team_name = request.POST.get('team_name')
        team_description = request.POST.get('team_description')
        team_owner = request.user.id
        database_user_record = User.objects.get(pk=team_owner)
        database_team_record = Team(name=team_name, description=team_description, owner_id=team_owner)
        database_team_record.save()
        database_team_record.users.add(database_user_record)
        return HttpResponseRedirect(f'/accounts/team/{database_team_record.id}/')


class TeamSettings(LoginRequiredMixin, View):
    """View available after successful user authorization."""
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request, id):
        """Render settings view for a team.

        Keyword arguments:
        id -- parameter passed with GET method from TeamChannel view. Id of a team.
        """
        assigned_users_list = Team.objects.get(pk=id).users.all()
        team = Team.objects.get(pk=id)
        if request.user in assigned_users_list:
            ctx = {
                'team': team,
            }
            return render(request, 'team_settings.html', context=ctx)
        else:
            ctx = {
                'team': team
            }
            return render(request, 'team_denied.html', context=ctx)


class TeamSettingsEdit(LoginRequiredMixin, View):
    """View available after successful user authorization"""
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request, id):
        """Check if authorized user is owner of a team.
        If True: render form with team name and description.
        If Flase: redner view with information about the lack of permissions.

        Keyword arguments:
        id -- parameter passed with GET method from TeamSettings view. Id of a team.
        """
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
            
    
    def post(self, request, id):
        """Check if authorized user is owner of a team.
        If True: save new record with name and description to Team database table.
        If False: redner view with information about the lack of permissions.

        Keyword arguments:
        id -- parameter passed with GET method from TeamSettings view. Id of a team.
        """
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
    """View available after successful user authorization."""
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request, id):
        """Check if authorized user is owner of a team.
        If True: render view with new user - team relation form.
        If False: redner view with information about the lack of permissions.

        Keyword arguments:
        id -- parameter passed with GET method from TeamSettings view. Id of a team.
        """
        team = Team.objects.get(pk=id)
        owner = team.owner_id
        sender = request.user.id
        if owner == sender:
            all_users_list = User.objects.all().order_by('first_name')
            assigned_users_list = Team.objects.get(pk=id).users.all()
            ctx = {
                'team': team,
                'all_users_list': all_users_list,
                'assigned_users_list': assigned_users_list,
            }
            return render(request, 'team_settings_add_user.html', context=ctx)
        else:
            ctx = {
                'team': team,
            }
            return render(request, 'team_settings_denied.html', context=ctx)
    
    def post(self, request, id):
        """Check if authorized user is owner of a team.
        If True: save new record with new relation between auth_user table and Team table.
        If False: redner view with information about the lack of permissions.

        Keyword arguments:
        id -- parameter passed with GET method from TeamSettings view. Id of a team.
        """
        team = Team.objects.get(pk=id)
        new_user = request.POST.get('add-user')
        team.users.add(new_user)
        return HttpResponseRedirect(f'/accounts/team/settings/add-user/{id}/')


class TeamSettingsDelete(LoginRequiredMixin, View):
    """View available after successful user authorization."""
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request, id):
        """Check if authorized user is owner of a team.
        If True: render view with team delate confirmation.
        If False: redner view with information about the lack of permissions.

        Keyword arguments:
        id -- parameter passed with GET method from TeamSettings view. Id of a team.
        """
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
        """Check if authorized user is owner of a team.
        If True: delete record from Team table.
        If False: redner view with information about the lack of permissions.

        Keyword arguments:
        id -- parameter passed with GET method from TeamSettings view. Id of a team.
        """
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


class PrivateList(LoginRequiredMixin, View):
    """View available after successful user authorization."""
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        """Render view with form containg dropdown with list of users (authorised user excluded)."""
        users_list = User.objects.all().order_by('first_name')
        ctx = {
            'users_list': users_list
        }
        return render(request, 'private_list.html', context=ctx)

    def post(self, request):
        """Redirect to PrivateChannel view for choosen recipient."""
        recipient = request.POST.get('recipient')
        if recipient == None:
            return HttpResponseRedirect(f'/accounts/private/')
        else:
            return HttpResponseRedirect(f'/accounts/private/{recipient}/')


class PrivateChannel(LoginRequiredMixin, View):
    """View available after successful user authorization."""
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request, id):
        """Render view with communication between authorised user and choosen recipient.
        
        Keyword arguments:
        id -- parameter passed with GET method from PrivateList view. Id of a recipient.
        """
        sender_id = request.user.id
        receiver_id = id
        receiver_object = User.objects.get(pk=id)
        sides_of_conversation = [sender_id, receiver_id]
        messages_list = PrivateMessage.objects.filter(receiver_id__in=sides_of_conversation).filter(sender_id__in=sides_of_conversation)
        ctx = {
            'messages_list': messages_list,
            'receiver': receiver_object
        }
        return render(request, 'private_channel.html', context=ctx)
    
    def post(self, request, id):
        """Save new message record to PrivateMessage database table. Redirect to view from GET method.

        Keyword arguments:
        id -- parameter passed with GET method from PrivateList view. Id of a recipient.
        """
        sender = request.user.id
        receiver = id
        new_message = request.POST.get('message_field')
        database_record = PrivateMessage(message=new_message, receiver_id=receiver, sender_id=sender)
        database_record.save()
        return HttpResponseRedirect(f'/accounts/private/{receiver}/')
