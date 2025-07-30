"""djangoldp uploader URL Configuration"""

from django.conf import settings
from django.urls import path, re_path
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt

from djangoldp_uploader import views
from djangoldp_uploader.views import FileUploadView, FileUploadPostView

urlpatterns = [
    path('upload/', csrf_exempt(FileUploadPostView.as_view()), name='upload'),
    re_path(r'^upload/(?P<hashcode>[\w|\W-]+)/(?P<filename>[\w|\W-]+).(?P<fileext>[\w]+)$', csrf_exempt(FileUploadView.as_view()), name='upload_xmpp')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += [
        path('demo/', views.home, name='home'),
        path('demo/sib/', views.demo_sib, name='upload_sib'),
        path('demo/simple/', views.upload_view, name='simple_upload'),
        path('demo/form/', views.model_form_upload, name='model_form_upload'),
    ]
