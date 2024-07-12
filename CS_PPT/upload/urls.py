# upload/urls.py

from django.urls import path
from .views import upload_file, signup, user_login, user_logout

urlpatterns = [
    path('upload/', upload_file, name='upload_file'),
    path('signup/', signup, name='signup'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
]