from django.conf.urls import url
from users import views

urlpatterns = [
    url(r'^facebook/login/$', views.FBUserLogin.as_view()),
    url(r'^facebook/$', views.FBUserRedirect.as_view()),
]
