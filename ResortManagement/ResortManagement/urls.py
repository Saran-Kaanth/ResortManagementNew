"""
URL configuration for ResortManagement project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from users import views as user_views
from rooms import views as rooms_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',user_views.indexView,name='index'),
    path('users/home/',user_views.userHomeView,name="userhome"),
    path('staff/staffhome/',user_views.staffHomeView,name="staffhome"),
    path('user/register/',user_views.userRegisterView,name="userregister"),
    path('login/',user_views.loginView,name="login"),
    path('logout/',user_views.logoutView,name="logout"),
    path('staff/staffregister/',user_views.StaffCreationView.as_view(),name="staffregister"),
    path('rooms/createroom/',rooms_views.RoomsCreationView.as_view(),name="createroom"),
    path('rooms/roomslist/',rooms_views.RoomsListView.as_view(),name="roomslist"),
    path('rooms/<str:pk>/detail',rooms_views.RoomDetailView.as_view(),name="roomdetail"),
    path('sample/',rooms_views.SampleView.as_view(),name='sample'),
]






# """
# URL configuration for ResortManagement project.

# The `urlpatterns` list routes URLs to views. For more information please see:
#     https://docs.djangoproject.com/en/4.2/topics/http/urls/
# Examples:
# Function views
#     1. Add an import:  from my_app import views
#     2. Add a URL to urlpatterns:  path('', views.home, name='home')
# Class-based views
#     1. Add an import:  from other_app.views import Home
#     2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
# Including another URLconf
#     1. Import the include() function: from django.urls import include, path
#     2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
# """
# from django.contrib import admin
# from django.urls import path

# urlpatterns = [
#     path("admin/", admin.site.urls),
# ]
