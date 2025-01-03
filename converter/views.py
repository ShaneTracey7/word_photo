from xml.etree.ElementTree import tostring
from django.http import HttpResponse
from django.template import loader
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files import File

from converter.models import Image
import cv2 as cv
import numpy as np
import os



def home(request):
  #empties Image table in DB
  clearDB()
  template = loader.get_template('home.html')
  context = {
    'isConverted': False,
  }
  return HttpResponse(template.render(context, request))

def result(request):
  dbImage = Image.objects.all() # should only be one
  if len(dbImage) > 0:
    img = dbImage[0]
    template = loader.get_template('result.html')
    context = {
        'value' : convertImage(img),
      }
    return HttpResponse(template.render(context, request))
  else:
    template = loader.get_template('home.html')
    context = {
        'value' : ['empty'],
      }
    print('nothing in db')
    return HttpResponse(template.render(context,request))
@csrf_exempt
def handleImage(request,id=id):
  if request.method =='POST':
    img = request.FILES.get('image_file')
    myFile = File(img)
    i = Image.create(myFile)
    i.save()
    return JsonResponse('Saved image',safe=False)
  else:
    print('not post')
    return JsonResponse('incorrect request method',safe=False)

def clearDB():
   Image.objects.all().delete()
   #find how to delete contents of folder (images folder)

# my phone can have 65 lowercase 'L's in each line max
# about 12 rows of that would look complete 

def convertImage(image):

  
  row_num = 12 # OG = 12
  col_num = 66 # OG = 66
  #dbImage = Image.objects.get(image_file=i.image_file)
  print('i.path: ' + image.image_file.path)

  # Reading the image using imread() function
  img = cv.imread(image.image_file.path,cv.IMREAD_GRAYSCALE)
  

  # Extracting the height and width of an image
  h, w = img.shape[:2]
  # Displaying the height and width
  print("Height = {}, Width = {}".format(h, w))

  #crop image to make square
  if h > w:
    
    print('height is larger')
    row_start = (h//2) - (w//2)
    row_end = (h//2) + (w//2)
    # [rows, columns] 
    cropped_image = img[row_start:row_end,0:w]
  else:
    print('width is larger')
    col_start = (w//2) - (h//2)
    col_end = (w//2) + (h//2)
    # [rows, columns] 
    cropped_image = img[0:h,col_start:col_end]
  #img_75 = cv.resize(img, None, fx = 0.75, fy = 0.75)
  resized_img = cv.resize(cropped_image, (792,792)) # OG = 792,792
  cv.imwrite('testcv.jpg', resized_img)# saves changed file to filesystem
  
  edges = cv.Canny(resized_img,100,200)
  cv.imwrite('testcv3.jpg', edges)
  im = cv.imread('testcv3.jpg')
  white = [255,255,255]

  # Get X and Y coordinates of all blue pixels
  X, Y = np.where(np.all(im==white,axis=2))
  
  #def condenseX(num):
   # return num #// 65
  
  #def condenseY(num):
   # return num // 12
  
  #filtered_x = filter(condenseX, X)
  #filtered_y = filter(condenseY, Y)
  # Convert filter object to a list
  #list_x = list(filtered_x)
  #list_y = list(filtered_y)
  #remove duplicates
  #list_x  = list(dict.fromkeys(list_x))
  #list_y  = list(dict.fromkeys(list_y))
  
  
  zipped = np.column_stack((X,Y))
  print('zipped: ')
  for coord in zipped:
    #print(coord)
    coord[1] = coord[1] // (row_num / 2) #6
    
  new = [] #defining a new array     
     
  for i in zipped:
    if list(i) not in new:
        new.append(list(i))
 
  new = np.array(new)

  #displaying the new array with updated/unique elements
  print("New Array : ")
  for c in new:
    c[0] = c[0] // (col_num / 3) #11

  new2 = [] #defining a new array     
     
  for i in new:
    if list(i) not in new2:
        new2.append(list(i))

  new2 = np.array(new2)

  charArr = [] #set a empty char array
  #nneded for testing
  #charArr.append(['|'] * (col_num * 2))#132
  #charArr.append(['.'] * (col_num * 2))#132
  #charArr.append(['I'] * (col_num * 2))#132
  for i in range(0, row_num * 3):
    arr = [' '] * (col_num * 2)#132
    charArr.append(arr)      
  
  strArr = []
  row = 0
  for i in new2:
    charArr[i[0]][i[1]] = 'I'
  
  print("Char Array : ")
  for c in charArr:
    s = "".join(str(e) for e in c)
    strArr.append([s])
   
  for c in strArr:
    print(c)

  i_name = image.image_file.name
  #very last step
  image.delete() #deletes from db
  os.remove(image.image_file.name)#deletes image from folder
  print('Image converted')

  return strArr




  