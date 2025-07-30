import os
import base64

from django.shortcuts import render, redirect
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
from django.template.defaultfilters import slugify
from django.utils.crypto import get_random_string
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from djangoldp.utils import is_authenticated_user

from djangoldp_uploader.forms import DocumentForm
from djangoldp_uploader.models import Document, File


def home(request):
    documents = Document.objects.all()
    return render(request, 'home.html', { 'documents': documents })


def demo_sib(request):
    return render(request, 'demo_sib.html')


def upload(request):
    if True: #is_authenticated_user(request.user): to delete when issue https://git.startinblox.com/framework/sib-core/issues/741 closed
        try:
            file_obj = request.FILES['file']
            fs = FileSystemStorage()
            file_name, file_ext = os.path.splitext(file_obj.name)
            file_name = slugify(file_name) + file_ext
            filename = fs.save(file_name, file_obj)
            uploaded_file_url = fs.url(filename)

            return Response(status=204, headers={'Location': "{}{}".format(settings.SITE_URL, uploaded_file_url)})

        except:
            return HttpResponse(status=400)

    else:
        return HttpResponse(status=403)


def compose_filename(hashcode, filename, fileext):
    file_name = '{}_slash_{}{}'.format(hashcode, filename, fileext)
    return file_name


def upload_put(request, hashcode, filename, fileext):
    if is_authenticated_user(request.user):
        try:
            file_name = compose_filename(hashcode, filename, fileext)
            file_obj = request.FILES['file']
            request_path = request.path
            content_type = request.content_type
            uploaded_file_url = settings.MEDIA_URL + file_name

            with open(uploaded_file_url[1:], 'wb+') as f:
                for chunk in file_obj.chunks():
                    f.write(chunk)

            file_model = File(
                stored_url = uploaded_file_url,
                original_url = request_path,
                content_type = content_type
            ).save()

            return HttpResponse(status=201)

        except:
            return HttpResponse(status=400)

    else:
        return HttpResponse(status=403)


class FileUploadPostView(APIView):
    def dispatch(self, request, *args, **kwargs):
        request.csrf_processing_done = True
        response = super().dispatch(request, *args, **kwargs)
        response["Access-Control-Allow-Origin"] = request.headers.get('origin')
        response["Access-Control-Allow-Methods"] = "POST,OPTIONS"
        response["Access-Control-Allow-Headers"] = "authorization, Content-Type, if-match, accept, sentry-trace, dpop"
        response["Access-Control-Expose-Headers"] = "Location, User"
        response["Access-Control-Allow-Credentials"] = 'true'

        return response

    def post(self, request):
        if request.FILES['file']:
            response = upload(request)
            
            return response

        else:
            return HttpResponse('No file provided', status=400)

class FileUploadView(APIView):
    parser_classes = (FileUploadParser,)

    def dispatch(self, request, *args, **kwargs):
        request.csrf_processing_done = True
        '''overriden dispatch method to append some custom headers'''
        response = super().dispatch(request, *args, **kwargs)
        response["Access-Control-Allow-Origin"] = request.headers.get('origin')
        response["Access-Control-Allow-Methods"] = "GET,POST,PUT,OPTIONS"
        response["Access-Control-Allow-Headers"] = "authorization, Content-Type, if-match, accept, sentry-trace, dpop"
        response["Access-Control-Expose-Headers"] = "Location, User"
        response["Access-Control-Allow-Credentials"] = 'true'

        return response


    def options(self, request, hashcode, filename, fileext):
        return HttpResponse(status=204)


    def post(self, request):
        if request.FILES['file']:
            response = upload(request)

            return response

        else:
            return HttpResponse('No file provided', status=400)


    def put(self, request, hashcode, filename, fileext):
        filename, fileext = os.path.splitext(request.path)
        filename = slugify(filename.split('/')[-1])

        if request.FILES['file']:
            if File.objects.filter(original_url = request.path).exists():
                return HttpResponse('File already existing at URL', status=409)
            
            else:
                response = upload_put(request, hashcode, filename, fileext)

                return response

        else:
            return self.get(request, hashcode, filename, fileext)


    def get(self, request, hashcode, filename, fileext):
        if File.objects.filter(original_url = request.path).exists():
            file_model = File.objects.get(original_url = request.path)
            return redirect(file_model.stored_url)
                
        else:
            return HttpResponse('No file found at URL', status=404)


def upload_view(request):
    if request.method == 'POST' and request.FILES['file']:
        uploaded_file_url = upload(request)
        return render(request, 'simple_upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'simple_upload.html')


def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = DocumentForm()
    return render(request, 'model_form_upload.html', {
        'form': form
    })
