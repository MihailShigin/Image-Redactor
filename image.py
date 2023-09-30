import os

from PIL import Image
from PIL import ImageFilter


class ImageEditor():
    def __init__ (self):
        self.filename = ""
        self.original = None
        self.changed = list()

    def do_name(self):
        filename_parts = self.filename.split(".")
        filename = filename_parts[0]
        extension = filename_parts[1]
        colichestvo = len(self.changed)
        naming = filename + str(colichestvo) + '.' + extension
        return naming

    def open(self, path):
        self.filename = os.path.basename(path)
        try:
            self.original = Image.open(path)
        except:
            print('Error: File not found')

    def do_bw(self):
        original_gray = self.original.convert('L')
        new_name = self.do_name() 
        self.changed.append(original_gray)
        return original_gray
        

    def do_blur(self):
        blur = self.original.filter(ImageFilter.BLUR)
        new_name = self.do_name() 
        self.changed.append(blur)
        return blur

    def do_up(self):
        up = self.original.transpose(Image.ROTATE_180)
        up.save('original_up.jpg')
        self.changed.append(up)
        up.show()

    def do_upu(self):
        upu = self.original.transpose(Image.FLIP_LEFT_RIGHT)
        upu.save('original_upu.jpg')
        self.changed.append(upu)
        upu.show()

    def do_cropped(self):
        box = (100, 100, 600, 450)
        cropped = self.original.crop(box)
        cropped.save('original_cropped.jpg')
        self.changed.append(cropped)
        cropped.show()