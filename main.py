import os

from PIL import Image
from PIL import ImageFilter
from PIL import ImageEnhance

from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QPushButton, QWidget, 
                             QHBoxLayout, QVBoxLayout, 
                             QTextEdit, QLineEdit, 
                             QListWidget, QLabel)
from PyQt5.QtWidgets import QFileDialog

from image import ImageEditor


SAVE_DIR = "Changed"


app = QApplication([])
window = QWidget()

image_names = QListWidget()

label = QLabel('Картинка')

pervi_spisok = QListWidget()
vtoroi_spisok = QListWidget()

button_0 = QPushButton("Папка")
button_0.setStyleSheet('background-color:yellow')
button_1 = QPushButton('Лево')
button_2 = QPushButton('Право')
button_4 = QPushButton('Резкость')
button_5 = QPushButton('Ч/Б')

window.setWindowTitle('Умные заметки')

v_line_0 = QVBoxLayout()
v_line_1 = QVBoxLayout()
v_line_2 = QVBoxLayout()
h_line_0 = QHBoxLayout()
h_line_1 = QHBoxLayout()
v_line_1.addWidget(button_0)
v_line_1.addWidget(image_names)
v_line_2.addWidget(label)
h_line_1.addWidget(button_1)
h_line_1.addWidget(button_2)
h_line_1.addWidget(button_4)
h_line_1.addWidget(button_5)

h_line_0.addLayout(v_line_0)
h_line_0.addLayout(v_line_1)
v_line_2.addLayout(h_line_1)
h_line_0.addLayout(v_line_2)

workdir = ''

workimage = ImageEditor()


# создаётся путь к выбранной папке с файлами картинок
def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()


# показ выбранной картинки на экране
def showImage(path):
    label.hide()
    pixmap = QPixmap(path)
    w, h = label.width(), label.height()
    pixmap = pixmap.scaled(w, h, Qt.KeepAspectRatio)
    label.setPixmap(pixmap)
    label.show()


# из всех файлов выбранной папки фильтрует файлы картинок
def image_filter(files, extensions):
    result = []
    for filename in files:
        for extension in extensions:
            print(extension)
            if filename.endswith(extension):
                result.append(filename)
    return result


# по нажатию на название картинки открывается выбранная картинка
def showChosenImage():
    if image_names.currentRow() >= 0:

        filename = image_names.currentItem().text()
        image_path = os.path.join(workdir, filename)
        
        workimage.open(image_path)
        showImage(image_path)


# показ названий картинок из выбранной папки на тег-экране
def showFilenamesList():
    global workdir
    chooseWorkdir()
    filenames = os.listdir(workdir)
    extensions = ['.jpg', '.png']
    image_names.clear()
    image_filtered = image_filter(filenames, extensions)
    image_names.addItems(image_filtered)


def save_image(new_image, new_name):

    dir_path = os.path.join(workdir, SAVE_DIR)
    if not(os.path.exists(dir_path) or os.path.isdir(dir_path)):
        os.mkdir(dir_path)

    image_path = os.path.join(dir_path, new_name)
    new_image.save(image_path)

    return image_path



def black_white_image():
    new_bw_image = workimage.do_bw()
    new_name = workimage.do_name()
    bw_path = save_image(new_bw_image, new_name)
    showImage(bw_path)


def blur():
    new_blur_image = workimage.do_blur()
    new_name = workimage.do_name()
    blur_path = save_image(new_blur_image, new_name)
    showImage(blur_path)


button_4.clicked.connect(blur)
button_5.clicked.connect(black_white_image)
button_0.clicked.connect(showFilenamesList)
image_names.currentRowChanged.connect(showChosenImage)

window.setLayout(h_line_0)

window.show()
app.exec()
