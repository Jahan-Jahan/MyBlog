from django.urls import path
from . import views

urlpatterns = [
    path("", views.blog_index, name="blog_index"),
    path("post/<str:pk>/", views.blog_detail, name="blog_detail"),
    path("category/<category>/", views.blog_category, name="blog_category"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("message_success/<str:pk>/", views.message_success, name="message_success"),
    path("resume/", views.resume, name="resume"),
    path("search/", views.search, name="search"),
]