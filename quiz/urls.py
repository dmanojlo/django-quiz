from django.urls import path, include
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
from .views import ( home_view)


app_name = 'quiz' # za url putanju do appa

urlpatterns = [
     path('home/', home_view, name='home'),
    # path('register/', register_view, name='register'),
    # path('login/', login_view, name='login'),
    # path('logout/', logout_view, name='logout'),
    # #path('item_create/', item_create_view, name='item_create_view'),
    # path('admin_panel/', item_create_view, name='item_create_view'),
    # #path('item_list/', item_list, name='item_list'),
    # path('shop_list/', item_list, name='item_list'),
    # path('decrement_quantity/<int:pk>/', decrement_quantity, name='decrement_quantity'),
    # path('delete/<int:pk>/', item_delete_view, name='item_delete_view'),
    # path('edit/<int:pk>/', item_edit_view, name='item_edit_view'),
    # # path('article_create/', ArticleCreateView.as_view(), name='article-create'),
    # # path('<int:id>/', ArticleDetailView.as_view(), name='article-detail'),
    # # path('<int:id>/delete/', ArticleDeleteView.as_view(), name='article-delete'),
]
