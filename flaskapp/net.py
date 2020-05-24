import random
# бибилиотека keras для НС
import keras
# входной слой сети и модель сети
from keras.layers import Input
from keras.models import Model

# одна из предобученных сетей
from keras.applications.resnet50 import preprocess_input, decode_predictions
import os
# модуль работы с изображениями
from PIL import Image
import numpy as np


# для конфигурации gpu
from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession

# настраиваем работу с GPU, для CPU эта часть не нужна
config = ConfigProto()
config.gpu_options.per_process_gpu_memory_fraction = 0.
config.gpu_options.allow_growth = True
session = InteractiveSession(config=config)

height = 224
width = 224
nh=224
nw=224
ncol=3

# загружаем и создаем стандартную уже обученную сеть keras
visible2 = Input(shape=(nh,nw,ncol),name ='imginp')
resnet = keras.applications.resnet_v2.ResNet50V2(include_top=True,
weights='imagenet', input_tensor=visible2,
input_shape=None, pooling=None, classes=1000)

# чтение изображений из каталога
# учтите если там есть файлы не соответствующие изображениям или каталоги
# возникнет ошибка
def read_image_files(files_max_count,dir_name):
    files = [item.name for item in os.scandir(dir_name) if item.is_file()]
    files_count = files_max_count
    if(files_max_count>len(files)): # определяем количество файлов не больше max
        files_count = len(files)
    image_box = [[]]*files_count
    for file_i in range(files_count): # читаем изображения в список
        image_box[file_i] = Image.open(dir_name+'/'+files[file_i]) # / ??
    return files_count, image_box

# возвращаем результаты работы нейронной сети
def getresult(image_box):
    files_count = len(image_box)
    images_resized = [[]]*files_count
    # нормализуем изображения и преобразуем в numpy
    for i in range(files_count):
        images_resized[i] = np.array(image_box[i].resize((height,width)))/255.
    images_resized = np.array(images_resized)
    # подаем на вход сети изображение в виде numpy массивов
    out_net = resnet.predict(images_resized)
    # декодируем ответ сети в один распознанный класс top=1 (можно больше классов)
    decode = decode_predictions(out_net, top=1)
    return decode

# заранее вызываем работу сети, так как работа с gpu требует времени
# из-за инициализации библиотек
fcount, fimage = read_image_files(1,'./static')
decode = getresult(fimage)