
from django.urls import path

from . import myentity_views

app_name = "app1"

urlpatterns = [
    
    path('myentity-list/', myentity_views.myentity_list, name="myentity_list"),
    path('myentity-create/', myentity_views.myentity_create, name="myentity_create"),
    path('myentity-edit/<int:id>', myentity_views.myentity_edit, name="myentity_edit"),
    path('myentity-detail/<int:id>', myentity_views.myentity_detail, name="myentity_detail"),
    path('myentity-delete/<int:id>', myentity_views.myentity_delete, name="myentity_delete"),    

]
