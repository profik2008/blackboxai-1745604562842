from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('industries/', views.industries, name='industries'),
    path('case-studies/', views.case_studies, name='case_studies'),
    path('blog/', views.blog, name='blog'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('careers/', views.careers, name='careers'),
    path('certifications/', views.certifications, name='certifications'),
    path('contact/', views.contact, name='contact'),
    path('news/', views.news, name='news'),
    path('api/submit-contact/', views.submit_contact, name='submit_contact'),
    path('api/subscribe-newsletter/', views.subscribe_newsletter, name='subscribe_newsletter'),
]
