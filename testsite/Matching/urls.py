from django.conf.urls import url
from .views import *

urlpatterns = [
        url(r'^clothInfo/$', ClothInfo.as_view()),
        url(r'^purchaseRecommend/$', RecommendPurchase.as_view()),
        url(r'^weatherInfo/$', WeatherInfo.as_view()),
        url(r'^dailyOutfit/$', GetDailyOutfit.as_view())
]
