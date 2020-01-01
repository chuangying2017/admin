from django.urls import path
import home.views as v


urlpatterns = [
    path('login/', v.UserVerify.as_view(), name='admin.login'),
    path('index/', v.IndexView.as_view(), name='admin.index'),
]
