"""patchmate URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf import settings
from django.urls import path, include
from django.views.generic import TemplateView
from patchmate import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),

    # home page
    path('', TemplateView.as_view(template_name='index.html')),
    path('default', TemplateView.as_view(template_name='index.html'), name="default"),
    path('home', TemplateView.as_view(template_name='index.html'), name="home"),
    path('index', TemplateView.as_view(template_name='index.html'), name="index"),

    # project-level
    path('about', TemplateView.as_view(template_name='custom/about.html'), name="about"),
    path('register', views.RegisterUser.as_view(), name='register'),
    path('robots.txt', TemplateView.as_view(template_name='custom/robots.txt'), name="robots"),
    path('sitemap.xml', TemplateView.as_view(template_name='custom/sitemap.xml'), name="sitemap"),

    # app urls
    path('userextensions/', include('userextensions.urls'), ),

    # userextension views
    path('list_recents/', views.ListRecents.as_view(), name='list_recents'),
    path('list_favorites/', views.ListFavorites.as_view(), name='list_favorites'),
    path('detail_user/', views.ShowUserProfile.as_view(), name='detail_user'),

    # swagger API docs
    path('swagger', views.schema_view, name="swagger"),

]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [path('__debug__/', include(debug_toolbar.urls)), ] + urlpatterns
