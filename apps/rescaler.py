from PIL import Image
from tkinter import filedialog
img = filedialog.askopenfilename(title='Enter the image to rescale:')
image = Image.open(img)
image.crop((16, 16, 496, 496))
image.save(img)