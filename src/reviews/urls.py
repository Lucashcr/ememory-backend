from django.urls import include, path
from rest_framework.routers import DefaultRouter

from reviews.views import ReviewInfoViewSet, SubjectsViewSet


router = DefaultRouter()
router.register("subjects", SubjectsViewSet, "subjects")
router.register("", ReviewInfoViewSet, "reviews")

urlpatterns = [
    path("", include(router.urls)),
]
