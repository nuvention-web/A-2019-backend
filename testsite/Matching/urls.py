from django.conf.urls import url
from . import views
from .views import *

urlpatterns = [
        url(r'^predict/$', Recommendation.as_view()),
        url(r'^clothInfo/$', ClothInfo.as_view()),
        url(r'^purchaseRecommend/$', RecommendPurchase.as_view())
]
