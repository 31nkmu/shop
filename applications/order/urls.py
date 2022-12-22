from django.urls import path
from rest_framework.routers import DefaultRouter

from applications.order import views

router = DefaultRouter()
router.register('', views.OrderViewSet)

urlpatterns = [
    path('confirm/<uuid:activation_code>/', views.OrderConfirmApiView.as_view()),
]

urlpatterns += router.urls
