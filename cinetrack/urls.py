from django.urls import path
from . import views

urlpatterns = [
    # Landing
    path('', views.landing_page, name='landing'),

    # Main
    path('titles/', views.title_list, name='title_list'),

    # Edit
    path("edit/<int:pk>/", views.edit_title, name="edit_title"),

    # Delete
    path("delete/<int:pk>/", views.delete_title, name="delete_title"),

    # Report
    path("report/", views.report_view, name="report_view"),

]