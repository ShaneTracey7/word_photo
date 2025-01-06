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
  parent = "/Users/Jarvis/Desktop/wpVirtEnv/word_photo/"
  folder_path = os.path.join(parent, "images")
  # check if directory contain
  if len(os.listdir(folder_path)) == 0:
    print("Directory is empty")
  else:    
    print("Directory is not empty")
    # List all files in the directory
    for filename in os.listdir(folder_path):
      file_path = os.path.join(folder_path, filename)
      os.remove(file_path)  # Remove the file
      print(f"Deleted file: {filename}")

# my phone can have 65 lowercase 'L's in each line max
# about 12 rows of that would look complete 

def convertImage(image):

  row_num = 12 # OG = 12
  col_num = 66 # OG = 66
  
  # Reading the image using imread() function
  print('i.path: ' + image.image_file.path)
  img = cv.imread(image.image_file.path,cv.IMREAD_GRAYSCALE)
  
  # Extracting the height and width of an image
  h, w = img.shape[:2]
  #print("Height = {}, Width = {}".format(h, w))

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
    coord[1] = coord[1] // (row_num / 2) #6 OG 792/6 = 132
    #coord[1] = coord[1] // 2 #3

  condensedArr1 = [] #defining a new array     
     
  for i in originalArr:
    if list(i) not in condensedArr1:
        condensedArr1.append(list(i))
 
  condensedArr1 = np.array(condensedArr1)

  #displaying the new array with updated/unique elements
  print("condensedArr1 : ")
  for c in condensedArr1:                                                           # X  x  Y
    c[0] = c[0] // (col_num /6)#((col_num / 3) / 3) #11 or (col_num / 9)   792/7.3 = 108 or 72     108 x 132
                                                                                   #  36 x  44 (plotted on char array)
                                                                                   #  36   x  66   (char array)
  condensedArr2 = [] #defining a new array     
     
  for i in condensedArr1:
    if list(i) not in condensedArr2:
        condensedArr2.append(list(i))

  condensedArr2 = np.array(condensedArr2)

  #print("Array b4 sort: ")
  #for c in new2:
    #print(c)

  Index = 1
  colSortArr = condensedArr2[condensedArr2[:,Index].argsort()]
  #print("Array after 1st sort: ")
  #for c in colSortArr :
    #print(c)
  #
  finalSortArr = extraSort(colSortArr) #extraSort(colSortArr) #finalSortArr = extraSort(colSortArr) 
  print("Array after final sort: ")
  for c in finalSortArr:
    print(c)

  #creates and sets char array
  strArr = createCharArr(finalSortArr,row_num,col_num)


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

  start = time.time()
  arrLength = np.size(inArr,axis=0)
  print('array length: ')
  print(arrLength)
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
  end = time.time() 
  print(end - start)

  return inArr





def createCharArr2(arr,row_num,col_num):
  
  charArr = [] #set a empty char array

  for i in range(0, (row_num * 3) + 1): #for small
  #for i in range(0, (row_num * 3) * 3): #(row_num * 9) for big
    row = [' '] * (int(col_num * (2/3)))#44 for small
    #row = [' '] * (col_num) #66
    #row = [' '] * (col_num * 2)#132 for big
    charArr.append(row)      
  
  strArr = []
  
  for i in arr:
    #charArr[i[0]][i[1]] = '|' #I for big
    charArr[int(i[0]/3)][int(i[1]/3)] = '|' #I  # for small
  
  print("Char Array : ")
  for c in charArr:
    s = "".join(str(e) for e in c)
    strArr.append([s])
   
  for c in strArr:
    print(c)

  return strArr
  



def createCharArr(inArr,row_num,col_num):

  top = "'"
  middle = ':'#could also be <:> or <•>
  bottom = ','
  mb = '¡' # upside down !
  tm = 'I' # should be capital 'i'
  all = '|'
  tb = ';' # top and bottom option 
  

  charArr = [] #set a empty char array

  #initializes charArr with empty values
  for i in range(0, (row_num * 3)+ 1): #(row_num * 9)
    row = [' '] * (int(col_num * (2/3)))# was *2 132
    #row = [' '] * (col_num)#
    charArr.append(row)   

  arrLength = np.size(inArr,axis=0)
  print('array length: ')
  print(arrLength)
  #for i in range(0, arrLength-1): # iterate through each coordinate
  i = 0
  while i < arrLength-1: # iterate through each coordinate
    if i == 0:
      print('col:')
      print(inArr[i][1])
      print('row:')
      print(inArr[i][0])
    col = inArr[i][1] # was 1 26 y 108 inArr[0] = 108
    row = inArr[i][0] # was 0 31 x

    #get first value (find range) (x // 3) * 3 (returns first value in range)
    fv = (row // 3) * 3
    if row % fv == 2:
      print('3rd')
      print('col: ' + str(col))
      #is bottom
      #fv / 3 = new y-coord in charArr
      #charArr[int(col/3)][int(fv/3)] = bottom
      i = i + 1#increment i
      charArr[int(fv/3)][int(col/3)] = bottom
      
    elif row % fv == 1:
      print('2nd')
      #is middle/middle & bottom
      nextCol = inArr[i+1][1]
      nextRow = inArr[i+1][0]
      if nextCol == col:
        print('same col 2nd: ' + str(nextCol))
        if nextRow == (row+1):
          #is middle & bottom
          charArr[int(fv/3)][int(col/3)] = mb
          i = i + 2#increment i
        else:
          #is middle
          i = i + 1#increment i
          charArr[int(fv/3)][int(col/3)] = middle
      else:
        #is middle
        i = i + 1#increment i
        charArr[int(fv/3)][int(col/3)] = middle

    else: #row % fv == 0
      print('1st')
      #is top/top & middle/top & bottom/all
      nextCol = inArr[i+1][1]
      nextRow = inArr[i+1][0]
      if nextCol == col:
        print('same col 1st: ' + str(nextCol))
        if nextRow == (row+1):
          #is top & middle
          #is top & middle/ all
          if i+2 == arrLength:
            charArr[int(fv/3)][int(col/3)] = tm
            i = i + 1#increment i
            break
          else:
            nextNextCol = inArr[i+2][1]
            nextNextRow = inArr[i+2][0]
            if nextNextCol == col:
              print('same col 1st 2nd: '+ str(nextNextCol))
              if nextNextRow == (row+2):
                #is all
                print('all')
                charArr[int(fv/3)][int(col/3)] = all
                i = i + 3#increment i
              else:
                #is top & middle
                print('top & middle')
                charArr[int(fv/3)][int(col/3)] = tm
                i = i + 2#increment i
            else:
              #is top & middle
              charArr[int(fv/3)][int(col/3)] = tm
              i = i + 2#increment i
        else:
          if nextRow == (row+2):
            #is top & bottom
            charArr[int(fv/3)][int(col/3)] = tb
            i = i + 2#increment i
          else:
            #is top
            i = i + 1#increment i
            charArr[int(fv/3)][int(col/3)] = top

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