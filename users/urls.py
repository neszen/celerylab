
from django.urls import path
from users.views import *

urlpatterns = [
    path('', home_page, name="home"),
    path('upload/', upload_csv, name="upload"),
    path('login/', login_page, name="login"),
    path('logout/', logout_page, name="logout"),
    path('signup/', signup_view, name="signup"),
]
