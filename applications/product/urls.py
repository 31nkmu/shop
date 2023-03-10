from rest_framework.routers import DefaultRouter

from applications.product import views

router = DefaultRouter()
router.register('category', views.CategoryViewSet)
router.register('', views.ProductViewSet)

urlpatterns = router.urls
