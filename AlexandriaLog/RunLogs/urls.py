from django.urls import path
from . import views
## allg_S5...
urlpatterns = [
    path('', views.index,name=""),
    path('update-task/<str:pk>', views.Updating, name="update-task"),
    path('delete-task/<str:pk>', views.DeleteTask, name="delete-task"),
    path('show-more/<str:pk>', views.ShowMore, name="show-more"),
    path('bkp', views.LocalBackUp, name="bkp"),
    path('sbkp', views.SecureBackUp, name="sbkp"),
]