from django.http import HttpResponse
from django.template import loader
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
#from .models import Member
# Create your views here.


def home(request):
  #mymembers = Member.objects.all().values()
  template = loader.get_template('home.html')
  context = {
    'isConverted': False,
  }
  return HttpResponse(template.render(context, request))

@csrf_exempt
def handleImage(request):
  if request.method =='POST':
    img = request.FILES.get('image_file')
    template = loader.get_template('home.html')
    context = {
      'isConverted': True,
      'value' : convertImage(img),
    }
    return HttpResponse(template.render(context, request))
  else:
    template = loader.get_template('home.html')
    context = {
      'isConverted': False,
    }
  return HttpResponse(template.render(context, request))

def convertImage(image):
  print('Image converted')
  text = image.name #test
  print(text)
  return text