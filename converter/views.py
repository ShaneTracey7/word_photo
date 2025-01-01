from django.http import HttpResponse
from django.template import loader
#from .models import Member
# Create your views here.


def home(request):
  #mymembers = Member.objects.all().values()
  template = loader.get_template('home.html')
  context = {
    'isImage': False,
  }
  return HttpResponse(template.render(context, request))