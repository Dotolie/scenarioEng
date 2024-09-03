from django.urls import include, path
from rest_framework import routers
from . import views #views.py import
from . import views

router = routers.DefaultRouter() #DefaultRouter를 설정
router.register('Item', views.ItemViewSet) #itemviewset 과 item이라는 router 등록
router.register('content', views.contentViewSet) #itemviewset 과 item이라는 router 등록

urlpatterns = [
    path('', include(router.urls)),
    path('scenario/', views.loadScenarioFile),
    path('scenario/<int:id>', views.readOneScenario),
    path('device/', views.readAllDevice),
    path('result/<int:id>', views.readOneResult),
    path('result/', views.readAllResult),
    path('test/<int:id>', views.testOne),
]