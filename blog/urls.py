from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'blog'

router = DefaultRouter()
router.register('categories', views.CategoriesAPIViewSet, basename='categories')
router.register('posts', views.BlogPostAPIViewSet, basename='posts')
urlpatterns = router.urls

