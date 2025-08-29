from django.contrib import admin
from django.urls import path
from django.http import JsonResponse
from django.conf import settings
from django.conf.urls.static import static
from graphene_file_upload.django import FileUploadGraphQLView
from django.views.decorators.csrf import csrf_exempt
from Project.schema import schema
from graphene_django.settings import graphene_settings
from django.http import HttpResponse

# for dev only
def download_schema(request, *args, **kwargs):
    if not settings.DEBUG:
        return HttpResponse("Not Found", status=404)
    sdl = str(schema) 
    
    response = HttpResponse(sdl, content_type="text/plain; charset=utf-8")
    response['Content-Disposition'] = 'attachment; filename=schema.graphql'
    return response

urlpatterns = [
    path('admin/', admin.site.urls),
    path("graphql/", csrf_exempt(FileUploadGraphQLView.as_view(graphiql=True, schema=schema))),
    path("", lambda request: JsonResponse({"message": "Welcome to the API"})),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [path("schema/", download_schema)]
