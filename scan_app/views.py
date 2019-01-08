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
from django.views.decorators.csrf import csrf_exempt
import os

def index(request):
    if request.method == 'POST' and request.FILES['usercv']:
        cname = request.POST['cname']
        myfile = request.FILES['usercv']
        fext = os.path.splitext(str(myfile))
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        #print(uploaded_file_url)
        url = uploaded_file_url.split('/media/')
        #print(uploaded_file_url.split('/media/'))
        fext = fext[len(fext)-1]
        a = ApplicantCV(applicant_name = cname, applicant_cv = url[1], cv_ext=fext)
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

@csrf_exempt
def processCV(request):
    cv_keywords = request.POST['keyvalues[]']
    cv_keywords = json.loads(cv_keywords)

    college = ApplicantCollege.objects.all();
    degree = ApplicantDegree.objects.all();
    applicant_cv = ApplicantCV.objects.all()
    applicant_cv = getDictCV(applicant_cv)
    #c_data['applicant_cv_1'] = applicant_cv_1
    #c_data['clean_text']
    #print(applicant_cv[0]['applicant_name'])
    #cv_keywords = CVKeywords.objects.all()
    neg_keywords = Neg_keywords.objects.all()
    college_count = ApplicantCollege.objects.count();
    degree_count = ApplicantDegree.objects.count();

    clg = clgCombination(college)
    deg = degreeCombination(degree)
    c_data = textClean(applicant_cv)

    collegerank = collegeRank(clg, c_data['applicant_cv_1'], c_data['clean_text'])
    degreerank = degreeRank(deg, c_data['applicant_cv_1'], c_data['clean_text'])
    keywordrank = keywordRank(c_data['applicant_cv_1'], cv_keywords, c_data['clean_text'], neg_keywords)
    #keywordrank = 0
    print(len(c_data['applicant_cv_1']))
    response = json.dumps({
        'collegeRank': collegerank,
        'degreeRank': degreerank,
        'keywordRank':keywordrank,
        'college_count': college_count,
        'degree_count': degree_count,
        'exclude_cv': c_data['exclude_cv']
    })

    #response = 0
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

def getcv(request):
    context = {}
    context['applicant_cv'] = ApplicantCV.objects.all()
    return render(request, 'cv.html', context)

def deletecv(request, id=None):
    app = ApplicantCV.objects.get(id=id)
    app.delete()
    return HttpResponse('Deleted')

import PyPDF2
def pdftest(request):
    applicant_cv = ApplicantCV.objects.all()
    applicant_cv = getDictCV(applicant_cv)
    for cv in applicant_cv:
        data = ""
        if cv['cv_ext']=='.pdf':
            pdfFileObj = open(cv['applicant_cv'].path,'rb')     #'rb' for read binary mode
            pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
            for p in range(pdfReader.numPages):
                pageObj = pdfReader.getPage(p)          #'9' is the page number
                data += pageObj.extractText()
    return render(request, "pdftest.html", {'data':data})
