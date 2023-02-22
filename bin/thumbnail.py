from PIL import Image
import PIL
import os
import sys


def thumbnail(filename, ratio):
    if ratio is None:
        ratio = 0.5
    """save as jpg"""
    filename = os.path.expanduser(filename)
    with open(filename, 'rb') as f:
        img: PIL.Image = Image.open(f)
        w, h = img.size
        w = int(w*ratio)
        h = int(h*ratio)
        img.thumbnail((w, h))
        img.save(filename, 'jpeg')


def main():
    args = sys.argv[1:]
    if len(args) <= 0:
        print('python thumbnail.py filename ratio')
        return
    filename = args[0]
    ratio = args[1] if len(args) > 1 else None 
    thumbnail(filename, ratio=ratio)

if __name__ == '__main__':
    main()