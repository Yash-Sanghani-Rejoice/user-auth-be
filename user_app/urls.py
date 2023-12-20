from django.urls import path
from .views import *

urlpatterns = [
          path("register-api/",RegisterAPI.as_view()),
          path("login-api/",LoginAPI.as_view()),
          path('get-user-data/', GetUserDataAPI.as_view()),
          path('product-data/', ProductDataAPI.as_view()),
          path('product-data-update/<int:id>', ProductDataUpdateAPI.as_view()),
]
