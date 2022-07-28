from django.urls import include, path
from rest_framework import routers
from vimeoapi.views import *

router = routers.DefaultRouter()
urlpatterns = [
   path('', include(router.urls)),
   path('uploadVideo', uploadVideo),
   path('createfolder', createfolder),
   path('listfolders', listfolders),
   path('specificfoldersdetail', specificfoldersdetail),
   path('uploadvideotospecificfolder', uploadvideotospecificfolder),
   path('getvideospresentinspecificfolder', getvideospresentinspecificfolder),
   path('webhookzoom', webhookzoom),
   path('listzoomrecording', listzoomrecording),
   path('getspecificmeeting', getspecificmeeting),
   path('downloadzoomrecording', downloadzoomrecording),

   
]