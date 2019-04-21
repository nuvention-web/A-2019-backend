from django.conf.urls import url
from . import views
from .views import Recommendation

urlpatterns = [
        url(r'^predict/$', Recommendation.as_view()),
]
