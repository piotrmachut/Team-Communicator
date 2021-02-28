"""teamcommunicator URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from engine import views as engine_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', engine_views.IndexView.as_view(), name='index'),
    path('accounts/signup/', engine_views.SignUp.as_view(), name='sign-up'),
    path('accounts/logged-out/', engine_views.LoggedOut.as_view(), name='logged-out'),
    path('accounts/profile/', engine_views.Profile.as_view(), name='profile'),
    path('accounts/profile/settings/', engine_views.ProfileSettings.as_view(), name='profile-settings'),
    path('accounts/profile/settings/delete/', engine_views.ProfileDelete.as_view(), name='profile-delete'),
    path('accounts/team/<int:id>/', engine_views.TeamChannel.as_view(), name='team-channel'),
    path('accounts/team/add/', engine_views.TeamAdd.as_view(), name='team-add'),
    path('accounts/team/settings/<int:id>/', engine_views.TeamSettings.as_view(), name='team-settings'),
    path('accounts/team/settings/edit/<int:id>/', engine_views.TeamSettingsEdit.as_view(), name='team-edit'),
    path('accounts/team/settings/add-user/<int:id>/', engine_views.TeamSettingsAddUser.as_view(), name='team-add-user'),
    path('accounts/team/settings/delete/<int:id>/', engine_views.TeamSettingsDelete.as_view(), name='team-delete'),
    path('accounts/private/', engine_views.PrivateList.as_view(), name='private-list'),
    path('accounts/private/<int:id>/', engine_views.PrivateChannel.as_view(), name='private-channel'),
]
