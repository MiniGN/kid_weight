from django.conf.urls import url, include
from django.contrib import admin
from weight import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^add_weight/', views.add_weight, name='add_weight'),
    url(r'^remove_weight/', views.remove_weight, name='remove_weight'),
    url(r'^async_weight_table/', views.async_weight_table, name='async_weight_table'),
    url(r'^async_weight_chart/', views.async_weight_chart, name='async_weight_chart'),
    url(r'^edit_desc_weight/', views.edit_desc_weight, name='edit_desc_weight'),

]