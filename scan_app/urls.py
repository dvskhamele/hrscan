from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('user_logout/', views.user_logout, name="logout"),
    path('adminpanel/', views.adminpanel, name='adminpanel'),
    path('adminpanel/cv/', views.getcv, name='cv'),
    path('adminpanel/cv/<int:id>', views.deletecv),
    path('adminpanel/addkeywords/<str:kw>', views.addKW),
    #path('adminpanel/api/v1/addcollege', views.CreateApplicantCollege.as_view()),
    #path('adminpanel/api/v1/addcdegree', views.CreateApplicantDegree.as_view()),
    path('adminpanel/api/v1/addkeywords', views.CreateCVKeywords.as_view()),
    path('adminpanel/api/v1/processcv', views.processCV),

    path('adminpanel/pdftest/', views.pdftest),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
