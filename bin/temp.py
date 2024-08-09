from PIL import ImageGrab

data = ImageGrab.grabclipboard()
print(data)

import pyperclip 

data = pyperclip.paste()
print(data)