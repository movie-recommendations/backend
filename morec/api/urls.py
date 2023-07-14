from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .docs import urlpatterns as docs_urlpatterns
from .views.movies import MoviesViewSet

v1_router = DefaultRouter()
v1_router.register('movies', MoviesViewSet)


urlpatterns = [
    path('docs/', include(docs_urlpatterns)),
    path('v1/', include(v1_router.urls)),
]
