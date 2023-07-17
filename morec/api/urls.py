from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .docs import urlpatterns as docs_urlpatterns
from .views.movies import MoviesViewSet
from .views.categories import CategoryViewSet
from .views.genres import GenreViewSet
from .views.countries import CountryViewSet
from .views.compilations import (
    CompliationSoloViewSet,
    ComplilationRedactorionListViewSet,
    ComplilationFavoriteListViewSet
)
from .views.users import user_verify_email

v1_router = DefaultRouter()
v1_router.register('movies', MoviesViewSet)
v1_router.register('categories', CategoryViewSet)
v1_router.register('gangres', GenreViewSet)
v1_router.register('countries', CountryViewSet)
v1_router.register(
    'complilations/redactorion',
    ComplilationRedactorionListViewSet,
    basename="comp-redac"
)
v1_router.register(
    'complilations/favorite',
    ComplilationFavoriteListViewSet,
    basename="comp-favorite"
)

urlpatterns = [
    path('users/verify-email/', user_verify_email),
    path('docs/', include(docs_urlpatterns)),
    path('v1/', include(v1_router.urls)),

    path(
        'v1/complilations/<int:pk>/',
        CompliationSoloViewSet.as_view(),
        name="complilation"
    ),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),

]
