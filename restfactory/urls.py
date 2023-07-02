from django.contrib import admin
from django.contrib.auth.views import LogoutView

from django.urls import path
from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view

from restfactory.additional_urls import additionalurlpattern

API_TITLE = "RESTFactory API"
API_DESCRIPTION = "A web API for creating and editing your favourite items"

urlpatterns = [
    path('admin-restfactory/', admin.site.urls),
    path('docs/', include_docs_urls(title=API_TITLE, description=API_DESCRIPTION)),  # human-readable doc
    path('schema/', get_schema_view(title=API_TITLE)),  # machine-readable doc
    path('logout/', LogoutView.as_view(), name='logout'),
]

# Custom App
urlpatterns += additionalurlpattern
