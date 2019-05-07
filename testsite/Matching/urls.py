from django.conf.urls import url
from . import views
from .views import Recommendation, ClothInfo

urlpatterns = [
        url(r'^predict/$', Recommendation.as_view()),
        url(r'^clothInfo/$', ClothInfo.as_view())
]
