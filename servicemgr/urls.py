from django.urls import path
from django.conf.urls import include

# import views
import servicemgr.views as gui

app_name = 'servicemgr'

urlpatterns = [
    # list views
    path('list_services/', gui.ListServices.as_view(), name='list_services'),

    # detail views
    path('detail_service_controls/<int:pk>/', gui.DetailServiceControls.as_view(), name='detail_service_controls'),
    path('detail_service_status/<int:pk>/', gui.DetailServiceStatus.as_view(), name='detail_service_status'),

]
