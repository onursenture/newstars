from django.db import models
from django.contrib.auth.models import User

days = ("Monday","Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
current_year = 2012
current_semester = 2

class Person(models.Model):
  name        = models.CharField(max_length=50)
  surname     = models.CharField(max_length=50)
  ID          = models.IntegerField(default=0,primary_key=True)
  regDate     = models.DateField(auto_now_add=True)
  affiliation = models.ForeignKey('Department')
  user        = models.ForeignKey(User) 

  def __unicode__(self): return '%s %s'%(self.name,self.surname)

class Student(Person):
  GPA      = models.FloatField(default=0.0)
  year     = models.IntegerField(default=1)
  standing = models.CharField(max_length=15)
  major    = models.CharField(max_length = 20)
  address  = models.TextField(default='')
  enrolled = models.ManyToManyField('Section',through='Enrollment')

class Instructor(Person):
  telephone = models.IntegerField()
  office    = models.CharField(max_length=6)
  status    = models.CharField(max_length=10)
  degree    = models.CharField(max_length=10)
  advises   = models.ForeignKey(Student)
  teaches   = models.ManyToManyField('Course')

class GradStudent(Student):
  telephone = models.IntegerField()
  office    = models.CharField(max_length=6)
  degree    = models.CharField(max_length=10)
  assists   = models.ManyToManyField('Course',db_table='assists')

class VisitingProf(Instructor):
  visitStart = models.DateField(auto_now_add=True)
  visitEnd   = models.DateField()

class Department(models.Model):
  code      = models.CharField(max_length=5,primary_key=True)
  name      = models.CharField(max_length=80)
  chairman  = models.ForeignKey(Instructor,null=True)
  offerings = models.ManyToManyField('Course',db_table='offerings')

  def __unicode__(self): return self.code

class Course(models.Model):
  code          = models.CharField(max_length=8,primary_key=True)
  deptCode      = models.CharField(max_length=5)
  name          = models.CharField(max_length=80)
  credits       = models.IntegerField(null=True)
  sections      = models.ManyToManyField('Section',db_table='sections')
  prerequisites = models.ManyToManyField('Course',db_table='requires')

  def __unicode__(self): return self.code

class Section(models.Model):
  courseCode = models.CharField(max_length=8)
  #section info
  secNo      = models.IntegerField()
  year       = models.IntegerField()
  semester   = models.IntegerField()
  meets      = models.ManyToManyField('Schedule',db_table='meets')
  instructor = models.ForeignKey('Instructor')
  #quota Fields
  max        = models.IntegerField() 
  current    = models.IntegerField()

  def __unicode__(self): return "%s:%d"%(self.courseCode, self.secNo)

class Schedule(models.Model):
  room      = models.CharField(max_length=5)
  day       = models.IntegerField()
  hour      = models.IntegerField()
  duration  = models.IntegerField()

  class Meta:
    unique_together = ('room','day','hour')

  def __unicode__(self): return "%s @ %d.40 to %d.30 in %s"%(days[self.day-1], self.hour+7, self.hour+7+self.duration, self.room)

class Enrollment(models.Model):
  student  = models.ForeignKey('Student')
  section  = models.ForeignKey('Section')
  year     = models.IntegerField()
  semester = models.IntegerField()
  grade    = models.CharField(max_length=2)

class Assignment(models.Model):
  type    = models.CharField(max_length=3)
  grade   = models.IntegerField(default=0)
  notes   = models.CharField(max_length=200)
  checked = models.BooleanField(default=False)
  course  = models.ForeignKey('Course')
  student = models.ForeignKey('Student')

class Attendance(models.Model):
  week     = models.IntegerField()
  course   = models.ForeignKey('Course')
  student  = models.ForeignKey('Student')
  attended = models.IntegerField(default=0)
  checked  = models.BooleanField(default=False)
  max      = models.IntegerField()


