
from PIL import Image
import sys

# img = Image.open('./img/16001.JPG')
# largura = img.size[0]
# altura = img.size[1]
#
# new_img = img.resize((largura, altura), Image.ANTIALIAS)
# new_img.save('./img/newImage' + '.JPG', optimize=True)

basewidth = 400
img = Image.open('./img/teste.jpg')

wpercent = (basewidth/float(img.size[0]))
hsize = int((float(img.size[1])*float(wpercent)))
img = img.resize((basewidth,hsize), Image.ANTIALIAS)
img.save('./img/new_img.JPG')