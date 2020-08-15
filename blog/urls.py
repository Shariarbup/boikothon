from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.index, name="index"),
    path('author/<name>/', views.getauthor, name="author"),
    path('article/<int:id>/', views.getsingle, name="single_post"),
    path('category/<name>/', views.getcategory, name="category"),
    path('login/', views.getlogin, name="login"),
    path('register/', views.getregister, name="register"),
    path('logout/', views.getlogout, name="logout"),
    path('create/', views.getcreate, name="create"),
    path('profile/', views.getprofile, name="profile"),
    path('profile/<int:id>/', views.getupdateprofile, name="update-profile"),
    path('update/<int:id>/', views.getupdate, name="update"),
    path('delete/<int:id>/', views.getdelete, name="delete"),
    path('topics/', views.gettopic, name="topics"),
    path('create/topic/', views.getnewtopic, name="new-topic"),
    path('update_topic/<name>/', views.getupdatetopic, name="update-topic"),
    path('delete_topic/<name>/', views.getdeletetopic, name="delete-topic"),

    #account confirmation
    path('activate/<uid>/<token>', views.activate, name='activate')


]
