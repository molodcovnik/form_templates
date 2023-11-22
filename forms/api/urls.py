from django.urls import path, include
from .views import FieldsView, TemplateView, SearchView, SearchFormView


urlpatterns = [
    path('', FieldsView.as_view()),
    path('forms/', TemplateView.as_view()),
    path('get_form/', SearchView.as_view()),
    path('get_form2/', SearchFormView.as_view()),
]