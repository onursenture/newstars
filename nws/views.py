from newstars.nws.models import *

from django.contrib import *
from django.core import serializers
from django.utils import simplejson
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db import connection, transaction
from datetime import date

@csrf_exempt
def login_screen(request):
  return render_to_response("login.html")

@csrf_exempt
def login(request):
  ID = request.POST['uid']
  pwd = request.POST['pwd']
  user = auth.authenticate(username=ID, password=pwd)
  if user is not None:
    if user.is_active:
      auth.login(request, user)
      return HttpResponseRedirect('/index/')
  else:
    return render_to_response("login.html",{'message':'Invalid username and/or password.'})

@login_required(redirect_field_name='')
def logout(request):
  if request.user.is_authenticated:
     auth.logout(request)
  return HttpResponseRedirect("/index/")

@login_required(redirect_field_name='')
def home(request):
  try:
    s = Student.objects.get(user=request.user)
    sections = s.enrolled.filter(year=current_year,semester=current_semester)
    s_dict={}
    for se in sections:
        s_dict[se.courseCode] = se.meets.all()
    return render_to_response('index.html',{'student':s,'sections':s_dict,'width':range(8),'height':range(12)})
  except:
    i = Instructor.objects.get(user=request.user)
    sections = Section.objects.filter(instructor=i,year=current_year,semester=current_semester)
    s_dict={}
    for se in sections:
        s_dict[se.courseCode+":"+str(se.id)] = se.meets.all()
    degree = ' '.join(map(lambda x: '%s.'%x ,i.degree.split(' ')))
    return render_to_response('instructor.html',{'instructor':i,'degree':degree,'sections':s_dict,'width':range(8),'height':range(12)})

@login_required(redirect_field_name='')
def register(request):
  s = Student.objects.get(user=request.user)
  departments = Department.objects.all()
  sections = s.enrolled.filter(year=current_year,semester=current_semester)
  s_dict={}
  for se in sections:
    s_dict[se.courseCode] = se.meets.all()
  return render_to_response('registration.html',{'student':s,'sections':s_dict,'width':range(8),'height':range(12),'departments':departments,'mysecs':sections,'current_year':current_year,'current_semester':current_semester})

@login_required(redirect_field_name='')
def transcript(request):
  st = Student.objects.get(user=request.user)
  y_dict={}
  enrollments = Enrollment.objects.filter(student=st).order_by('-year','-semester')
  for e in enrollments:
    se = e.section
    c = Course.objects.get(code=se.courseCode)
    try:
        y_dict[str(e.year)+' '+str(e.semester)].append({'semester':e.semester,'year':e.year,'name':c.name,'grade':e.grade,'credits':c.credits})
    except:
        y_dict[str(e.year)+' '+str(e.semester)]=[{'semester':e.semester,'year':e.year,'name':c.name,'grade':e.grade,'credits':c.credits}]
    
  return render_to_response('transcript.html',{'student':st,'courses':y_dict})

@login_required(redirect_field_name='')
def course(request,code):
  c = Course.objects.get(code=code)
  st = Student.objects.get(user=request.user)
  assignments = serializers.serialize('json',Assignment.objects.filter(student=st,course=c))
  attendances = serializers.serialize('json',Attendance.objects.filter(student=st,course=c))
  instructor = st.enrolled.get(courseCode=c.code).instructor
  iname = '%s %s'%(instructor.name, instructor.surname)

  return HttpResponse('{"cCode":"%s","instructor":"%s","assignments":%s,"attendances":%s}'%(c.code,iname,assignments,attendances))


@login_required(redirect_field_name='')
def course_inst(request,code,secID):
  c = Course.objects.get(code=code)
  i = Instructor.objects.get(user=request.user)
  section = Section.objects.get(id = secID, year=current_year ,semester=current_semester)
  studentsss = section.enrollment_set.all().values('student')
  students = Person.objects.filter(ID__in=studentsss)
  return HttpResponse('{"cCode":"%s","cName":"%s","students":%s}'%(code,c.name,serializers.serialize('json',students)))

@login_required(redirect_field_name='')
def read_element(request,type,id):
  if type=='attnd':
   a=Attendance.objects.get(id=id)
  elif type=='assgn':
   a=Assignment.objects.get(id=id)
  a.checked = True
  a.save()
  return HttpResponse(a.checked)

@csrf_exempt
def add_element(request,type):
    if type=='grade':
      gtype  = request.POST['type']
      ggrade = request.POST['grade']
      gnote  = request.POST['notes']
      gid    = request.POST['ID']
      gCode  = request.POST['code']
      s = Student.objects.get(ID=gid)
      c = Course.objects.get(code=gCode)
      elem = Assignment.objects.create(student=s,course=c,type=gtype,grade=ggrade,notes=gnote)
      elem.save()
    elif type=='attend':
      attend  = request.POST['attend']
      aweek = request.POST['week']
      aid    = request.POST['ID']
      aCode  = request.POST['code']
      s = Student.objects.get(ID=aid)
      c = Course.objects.get(code=aCode)
      se = s.enrolled.get(courseCode=aCode)
      amax=0
      for e in se.meets.all(): amax+=e.duration
      elem = Attendance.objects.create(student=s,course=c,attended=attend,week=aweek,max=amax)
      elem.save()
    return HttpResponse()


def get_sec_data(request,s_id):
  s = Section.objects.get(id=s_id)
  meets = serializers.serialize('json',s.meets.all())
  return HttpResponse('{"cCode":"%s","meets":%s}'%(s.courseCode,meets))

def get_all_secs(request):
  s = Student.objects.get(user=request.user)
  departments = Department.objects.all()
  sections = s.enrolled.filter(year=current_year,semester=current_semester)
  s_dict={}
  for se in sections:
    s_dict[se.courseCode] = serializers.serialize('json',se.meets.all())
  sch = simplejson.dumps(s_dict)
  return HttpResponse(sch)

@login_required(redirect_field_name='')
def drop_section(request,s_id):
  se = Section.objects.get(id=s_id)
  st = Student.objects.get(user=request.user)
  se.current-=1
  se.save()
  Enrollment.objects.filter(student=st,section=se,year=se.year,semester=se.semester).delete()
  return HttpResponse(status=200)

@login_required(redirect_field_name='')
def add_section(request,s_id):
  se = Section.objects.get(id=s_id)
  st = Student.objects.get(user=request.user)
  cpr = st.enrolled.filter(courseCode=se.courseCode,year=current_year,semester=current_semester)
  if se.current<se.max:
    schlist = []
    can_add = True
    for e in st.enrolled.filter(year=current_year,semester=current_semester):
      for k in e.meets.all():
        schlist.append(k)
    for pos in se.meets.all():
      for cur in schlist:
        if (pos.day==cur.day and pos.hour==cur.hour): can_add = False 
    if(can_add):
      se.current+=1
      se.save()
      if len(cpr)!=0: Enrollment.objects.filter(student=st,section=cpr[0],year=se.year,semester=se.semester).delete()
      Enrollment.objects.create(student=st,section=se,year=se.year,semester=se.semester,grade="NA")
      return HttpResponse(status=200)
  return HttpResponse(status=400)

