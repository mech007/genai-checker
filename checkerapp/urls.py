from django.urls import path
from django.shortcuts import redirect
from . import views

# urlpatterns = [
#     path('', lambda request: redirect('maker_form')),  # Redirect root URL to maker form
#     path('maker/form/', views.maker_form_view, name='maker_form'),
#     path('checker/review/', views.checker_view, name='checker_review'),
# ]

urlpatterns = [
    path('', views.login_view),  # 👈 This handles the root URL
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('submit/', views.submit_form_view, name='submit_form'),
    path('edit/<int:form_id>/', views.edit_form_view, name='edit_form'),
    path('logout/', views.logout_view, name='logout'),
]

