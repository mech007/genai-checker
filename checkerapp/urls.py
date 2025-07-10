from django.urls import path
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path('', lambda request: redirect('maker_form')),  # Redirect root URL to maker form
    path('maker/form/', views.maker_form_view, name='maker_form'),
    path('checker/review/', views.checker_view, name='checker_review'),
]
