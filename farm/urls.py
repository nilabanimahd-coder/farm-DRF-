from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register("",views.FieldView)

urlpatterns = [
    path('farm/',views.FarmView.as_view(),name="farm"),
    path('field/',include(router.urls)),
    path('farm/<int:pk>/',views.FarmDetailView.as_view(),name="farmdetail"),

]
