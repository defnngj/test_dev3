from django.urls import path
from app_variable import views


urlpatterns = [
    # 变量管理
    path('', views.variable_list),
    path('save_variable/', views.save_variable),
]