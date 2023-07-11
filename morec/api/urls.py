from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .docs import urlpatterns as docs_urlpatterns
from .views.movies import MoviesViewSet
from .views.categories import CategoryViewSet
from .views.genres import GenreViewSet
from .views.countries import CountryViewSet

v1_router = DefaultRouter()
v1_router.register('movies', MoviesViewSet)
v1_router.register('categories', CategoryViewSet)
v1_router.register('gangres', GenreViewSet)
v1_router.register('countries', CountryViewSet)


urlpatterns = [
    path('docs/', include(docs_urlpatterns)),
    path('v1/', include(v1_router.urls)),
]
