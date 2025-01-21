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
import time


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
        'size' : img.size
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
    size = request.POST.get('size')
    myFile = File(img)
    i = Image.create(myFile,size)
    i.save()
    return JsonResponse('Saved image',safe=False)
  else:
    print('not post')
    return JsonResponse('incorrect request method',safe=False)

def clearDB():
  Image.objects.all().delete()
  # local env testing: 'parent = "/Users/Jarvis/Desktop/wpVirtEnv/word_photo/'
  parent = "/home/shantrac/word_photo/"
  folder_path = os.path.join(parent, "images")
  # check if directory contain
  if len(os.listdir(folder_path)) == 0: 
    print("Directory is empty")
  else:   
    #doesn't work within pythonanywhere 
    print("Directory is not empty")
    # List all files in the directory
    for filename in os.listdir(folder_path):
      file_path = os.path.join(folder_path, filename)
      os.remove(file_path)  # Remove the file
      print(f"Deleted file: {filename}")

# my phone can have 65 lowercase 'L's in each line max
# about 12 rows of that would look complete 

def convertImage(image):

  size = image.size
  nums = [0,0,0,0]
  if size == 'SMALL':
    nums = [792/162,8.8,30,54]
  elif size == 'MEDIUM':
    nums = [3,5.28,50,88]
  elif size == 'LARGE':
    nums = [1.5,2.64,100,176]
  elif size == 'X-LARGE':
    nums = [1,1.76,150,264]

  row_num = 12 # OG = 12
  col_num = 66 # OG = 66 11,
  
  # Reading the image using imread() function
  print('i.path: ' + image.image_file.path)
  img = cv.imread(image.image_file.path,cv.IMREAD_GRAYSCALE)
  
  #increases contrast for lighter pictures
  #alpha = 1.25 # Contrast control
  #beta = -120 # Brightness control

  #img = cv.convertScaleAbs(img, alpha=alpha, beta=beta)

  # Extracting the height and width of an image
  h, w = img.shape[:2]

  #crop image to make square
  if h > w:
    
    row_start = (h//2) - (w//2)
    row_end = (h//2) + (w//2)
    # [rows, columns] 
    cropped_image = img[row_start:row_end,0:w]
  else:
    col_start = (w//2) - (h//2)
    col_end = (w//2) + (h//2)
    # [rows, columns] 
    cropped_image = img[0:h,col_start:col_end]

  resized_img = cv.resize(cropped_image, (792,792)) # OG = 792,792
  cv.imwrite('testcv.jpg', resized_img)# saves changed file to filesystem
  
  #returns tracing of image in white and black (white lines)
  edges = cv.Canny(resized_img,100,200)
  cv.imwrite('testcv3.jpg', edges)
  im = cv.imread('testcv3.jpg')
  white = [255,255,255]

  # Get X and Y coordinates of all white pixels
  X, Y = np.where(np.all(im==white,axis=2))

  #create 2D-array of coordinates
  originalArr = np.column_stack((X,Y))
  
  print('originalArr: ')
  for coord in originalArr:
    coord[1] = coord[1] // (nums[0]) 

  condensedArr1 = [] #defining a new array     
     
  for i in originalArr:
    if list(i) not in condensedArr1:
        condensedArr1.append(list(i))
 
  condensedArr1 = np.array(condensedArr1)

  #displaying the new array with updated/unique elements
  print("condensedArr1 : ")
  for c in condensedArr1:                                                           
    c[0] = c[0] // (nums[1])

  condensedArr2 = [] #defining a new array     
     
  for i in condensedArr1:
    if list(i) not in condensedArr2:
        condensedArr2.append(list(i))

  condensedArr2 = np.array(condensedArr2)

  Index = 1
  colSortArr = condensedArr2[condensedArr2[:,Index].argsort()]
 
  finalSortArr = extraSort(colSortArr)
  #print("Array after final sort: ")
  #for c in finalSortArr:
    #print(c)

  #creates and sets char array
  strArr = createCharArr(finalSortArr,nums[2],nums[3])

  i_name = image.image_file.name
  #very last step
  image.delete() #deletes from db
  os.remove(image.image_file.name)#deletes image from folder
  print('Image converted')

  return strArr

# called after inArr has been sorted by column coordinate (Y-value)
# sorts groups of coordinates with same Y-value , by their X-value 
#keeps giving me index out of 
def extraSort(inArr):

  #start = time.time()
  arrLength = np.size(inArr,axis=0)
  for i in range(0, arrLength-1):
    col = inArr[i][1]
    count = 1
    arr = [inArr[i]]
    while col == inArr[i+count][1]:
      arr.append(inArr[i+count])
      if (i + count) == (arrLength - 1): # (arrLength-1)
        break
      else:
        count = count + 1
    group_size = np.size(arr,axis=0)
    if group_size > 1:
      arr = np.sort(arr,axis=0)
      for e in range(0, group_size):
        inArr[i+e] = arr[e]
      i = i + group_size -1 # -1 bc loop already increments 1 i think

  #for testinf purposes
  #end = time.time() 
  #print(end - start)
  return inArr

# less detailed char arr
def createCharArr2(arr,num2,num3):
  
  charArr = [] #set a empty char array

  for i in range(0, num2): 
    row = [' '] * (num3)
    charArr.append(row)      
  
  strArr = []
  
  for i in arr:
    charArr[int(i[0]/3)][int(i[1]/3)] = '|'
  
  print("Char Array : ")
  for c in charArr:
    s = "".join(str(e) for e in c)
    strArr.append([s])
   
  for c in strArr:
    print(c)

  return strArr
  


# more detailed char arr
def createCharArr(inArr,num2,num3):

  top = "'"
  middle = ':'#could also be <:> or <•>
  bottom = ','
  mb = '¡' # upside down !
  tm = 'I' # should be capital 'i'
  all = '|'
  tb = ';' # top and bottom option 
  
  charArr = [] #set a empty char array

  #initializes charArr with empty values
  for i in range(0, num2):
    row = [' '] * (num3)
    charArr.append(row)   

  arrLength = np.size(inArr,axis=0)

  i = 0
  while i < arrLength-1: # iterate through each coordinate
    #if i == 0:
      #print('col:')
      #print(inArr[i][1])
      #print('row:')
      #print(inArr[i][0])
    col = inArr[i][1] 
    row = inArr[i][0] 

    #get first value (find range) (x // 3) * 3 (returns first value in range)
    fv = (row // 3) * 3
    if row % fv == 2:
      #print('3rd')
      #print('col: ' + str(col))
      #is bottom
      i = i + 1#increment i 
      charArr[int(fv/3)][int(col/3)] = bottom
      
    elif row % fv == 1:
      #print('2nd')
      #is middle/middle & bottom
      nextCol = inArr[i+1][1]
      nextRow = inArr[i+1][0]
      if nextCol == col:
        #print('same col 2nd: ' + str(nextCol))
        if nextRow == (row+1):
          #is middle & bottom
          charArr[int(fv/3)][int(col/3)]  = mb
          i = i + 2#increment i
        else:
          #is middle
          i = i + 1#increment i
          charArr[int(fv/3)][int(col/3)]  = middle
      else:
        #is middle
        i = i + 1#increment i
        charArr[int(fv/3)][int(col/3)]  = middle

    else: 
      #print('1st')
      #is top/top & middle/top & bottom/all
      nextCol = inArr[i+1][1]
      nextRow = inArr[i+1][0]
      if nextCol == col:
        #print('same col 1st: ' + str(nextCol))
        if nextRow == (row+1):
          #is top & middle
          #is top & middle/ all
          if i+2 == arrLength:
            charArr[int(fv/3)][int(col/3)]  = tm
            i = i + 1#increment i
            break
          else:
            nextNextCol = inArr[i+2][1]
            nextNextRow = inArr[i+2][0]
            if nextNextCol == col:
              #print('same col 1st 2nd: '+ str(nextNextCol))
              if nextNextRow == (row+2):
                #is all
                #print('all')
                charArr[int(fv/3)][int(col/3)]  = all
                i = i + 3#increment i
              else:
                #is top & middle
                #print('top & middle')
                charArr[int(fv/3)][int(col/3)]  = tm
                i = i + 2#increment i
            else:
              #is top & middle
              charArr[int(fv/3)][int(col/3)]  = tm
              i = i + 2#increment i
        else:
          if nextRow == (row+2):
            #is top & bottom
            charArr[int(fv/3)][int(col/3)]  = tb
            i = i + 2#increment i
          else:
            #is top
            i = i + 1#increment i
            charArr[int(fv/3)][int(col/3)]  = top

      else:
        #is top
        i = i + 1#increment i
        charArr[int(fv/3)][int(col/3)] = top

  strArr = []

  for c in charArr:
    s = "".join(str(e) for e in c)
    strArr.append([s])

  for c in strArr:
    print(c)

  return strArr