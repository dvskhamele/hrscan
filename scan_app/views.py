from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .models import *
from .serializer import *
from rest_framework import generics, pagination

from .read_colleges import *
from .preprocessing_degree import *
from .selected_resume import *
import json

#[{<FieldFile: CV1.docx>: [1]}, {<FieldFile: CV3.docx>: [39]}]
#[{<FieldFile: CV1.docx>: [2, 12, 5]}, {<FieldFile: CV2.docx>: [34, 3]}, {<FieldFile: CV3.docx>: []}]
#[{<FieldFile: CV1.docx>: 334.61309523809524}, {<FieldFile: CV2.docx>: 169.60119047619048}, {<FieldFile: CV3.docx>: 193.44642857142858}]


def index(request):
    if request.method == 'POST' and request.FILES['usercv']:
        cname = request.POST['cname']
        myfile = request.FILES['usercv']

        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        #print(uploaded_file_url)
        url = uploaded_file_url.split('/media/')
        #print(uploaded_file_url.split('/media/'))
        a = ApplicantCV(applicant_name = cname, applicant_cv = url[1])
        a.save()
        #request.session['status'] = "CV Submitted"
        return HttpResponse("<script>alert('Your CV is Submitted');window.location.href='./';</script>")
    else:
        return render(request, 'index.html')

def user_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('adminpanel'))
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('adminpanel'))
            else:
                context['status'] = "Your account was inactive."
                return render(request, 'login.html', context)
        else:
            context['status'] = "Invalid login details given"
            return render(request, 'login.html', context)
    else:
        return render(request, 'login.html', context)

@login_required(login_url='../login/')
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))

@login_required(login_url='../login/')
def adminpanel(request):
    context = {}
    context['college'] = ApplicantCollege.objects.all();
    context['degree'] = ApplicantDegree.objects.all();
    context['keywords'] = CVKeywords.objects.all()
    return render(request, 'admin.html', context)

def processCV(request):
    college = ApplicantCollege.objects.all();
    degree = ApplicantDegree.objects.all();
    applicant_cv = ApplicantCV.objects.all()
    cv_keywords = CVKeywords.objects.all()
    neg_keywords = Neg_keywords.objects.all()
    college_count = ApplicantCollege.objects.count();
    degree_count = ApplicantDegree.objects.count();

    clg = clgCombination(college)
    deg = degreeCombination(degree)
    clean_text = textClean(applicant_cv)

    collegerank = collegeRank(clg, applicant_cv, clean_text)
    degreerank = degreeRank(deg, applicant_cv, clean_text)
    keywordrank = keywordRank(applicant_cv, cv_keywords, clean_text, neg_keywords)
    #keywordrank = 0
    response = json.dumps({
        'collegeRank': collegerank,
        'degreeRank': degreerank,
        'keywordRank':keywordrank,
        'college_count': college_count,
        'degree_count': degree_count
    })
    return HttpResponse(response)

def addKW(request, kw=None):
    if kw!=None:
        cv = CVKeywords.objects.create(k_value=kw)
        cv.save()
        return HttpResponse('saved')

class CreateApplicantCollege(generics.CreateAPIView):
    queryset = ApplicantCollege.objects.all()
    serializer_class = ApplicantCollegeSerializer

class CreateApplicantDegree(generics.CreateAPIView):
    queryset = ApplicantDegree.objects.all()
    serializer_class = ApplicantDegreeSerializer

class CreateCVKeywords(generics.CreateAPIView):
    queryset = CVKeywords.objects.all()
    serializer_class = CVKeywordsSerializer
