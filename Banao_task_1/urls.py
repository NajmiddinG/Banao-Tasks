from django.contrib import admin
from django.urls import path
from medicine.views import login, dashboard, logout, create, delete, edit
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login, name="login"),
    path('', dashboard, name="dashboard"),
    path('create/post/', create, name="create"),
    path('edit/post/<int:id>/', edit, name="edit"),
    path('delete/post/<int:id>/', delete, name="delete"),
    path('logout/', logout, name='logout'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)