
from PIL import Image

img = Image.open('./img/vai.jpg')
new_img = img.resize((300, 256))
new_img.save('./img/newImage', 'jpeg')
