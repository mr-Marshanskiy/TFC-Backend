from django.urls import path
from common.views import file

app_name = 'common'


urlpatterns = [
    # Files
    path('files/', file.FileUploadView.as_view()),
    path('files/remove/<id>/', file.FileDeleteView.as_view()),

]
