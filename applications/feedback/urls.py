from rest_framework.routers import DefaultRouter

from applications.feedback import views

router = DefaultRouter()
router.register('comment', views.CommentViewSet)
router.register('favorite', views.FavoriteViewSet)

urlpatterns = router.urls
