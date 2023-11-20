from django.urls import path
from . import views

urlpatterns = [
    path('', views.speech_recognition, name='speech_recognition'),
    path('result/', views.result_view, name='result'),
    path('input_analyze/', views.input_analyze, name='input_analyze'),
    path('generate_campaign/', views.generate_campaign, name='generate_campaign'),
    path('preview_campaign/', views.preview_campaign_view, name='preview_campaign_view'),
    path('save_campaign', views.save_campaign, name='save_campaign'),
]