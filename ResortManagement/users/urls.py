from django.contrib import admin
from django.urls import path
from . import views


urlpatterns=[
            path('home/',views.userHomeView,name="userhome"),
            path('<int:pk>/me',views.ProfileView.as_view(),name="userprofile"),
            path('views<int:pk>/me/edit',views.EditProfileView.as_view(),name="useredit"),
            path('viewsregister/',views.userRegisterView,name="userregister"),
            path('viewsmyreservation/',views.MyReservationView.as_view(),name="myreservations"),
            path('login/',views.loginView,name="login"),
            path('logout/',views.logoutView,name="logout"),
            path('staffregister/',views.StaffCreationView.as_view(),name="staffregister"),
            path('staffhome/',views.staffHomeView,name="staffhome"),
            ]

