from django.contrib import admin
from django.urls import path, include
#from django.conf.urls import path, include


# здесь прописываем пути ко всем приложениям
urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('training/', include('training.urls', namespace='training')),
]
