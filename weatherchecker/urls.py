"""weatherchecker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
import conditions.views as condition_views
import NewsFeed.views as NewsFeedViews
from django.contrib.auth.models import User
import documentation.views as documentation_views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('conditions/<int:pk>', condition_views.view_conditions, name="view_conditions"),
    path('', condition_views.home, name="home"),
    path('nehal/documentation/interfaces/', documentation_views.all_interfaces, name="all_interfaces"),
    path('nehal/documentation/interfaces/<int:pk>/', documentation_views.view_interface, name="view_interface"),
    path('nehal/documentation/projects/', documentation_views.all_projects, name='all_projects'),
    path('nehal/documentation/projects/<int:pk>/', documentation_views.view_project_interfaces, name='view_project_interfaces'),
    path('nehal/newsfeed/headlines/', NewsFeedViews.GetHeadlines, name='get_headlines'),
]
