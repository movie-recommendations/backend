from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .docs import urlpatterns as docs_urlpatterns
from .views.movies import MoviesViewSet
from api.views.compilations import (CompliationSoloViewSet,
                                    ComplilationRedactorionListViewSet,
                                    ComplilationFavoriteListViewSet
                                    )


v1_router = DefaultRouter()
v1_router.register('movies', MoviesViewSet)
v1_router.register('complilations/redactorion',
                   ComplilationRedactorionListViewSet,
                   basename="comp-redac")
v1_router.register('complilations/favorite',
                   ComplilationFavoriteListViewSet,
                   basename="comp-favorite")


urlpatterns = [
    path('docs/', include(docs_urlpatterns)),
    path('v1/', include(v1_router.urls)),

    path('v1/complilations/<int:pk>/',
         CompliationSoloViewSet.as_view(),
         name="complilation"),
]
