import matplotlib
from flask_bootstrap import Bootstrap
from flask import Flask

app = Flask(__name__)
bootstrap = Bootstrap(app)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)

from flask import render_template



@app.route("/data_to")
def data_to():
    some_pars = {'user': 'Ivan', 'color': 'red'}
    some_str = 'Hello my dear frend!'
    some_value = 10
    return render_template('simple.html', some_str=some_str,
                           some_value=some_value, some_pars=some_pars)


from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, FloatField, SelectField, IntegerField

from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired

app.config['RECAPTCHA_USE_SSL'] = False
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LcXn_sUAAAAAEbvg1fqCMPOA_pgZiVcteIA9wCy'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LcXn_sUAAAAAPnsHebESwEcexSbONmIPTcIHVPS'
app.config['RECAPTCHA_OPTIONS'] = {'theme': 'white'}
app.config['SECRET_KEY'] = 'secret'


# создаем форму для загрузки файла
class NetForm(FlaskForm):
    # поле для введения строки, валидируется наличием данных
    # валидатор проверяет введение данных после нажатия кнопки submit
    # и указывает пользователю ввести данные если они не введены
    # или неверны
    openid = StringField('openid', validators=[DataRequired()])
    # поле загрузки файла
    # здесь валидатор укажет ввести правильные файлы
    upload = FileField('Load image', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    # поле формы с capture
    recaptcha = RecaptchaField()
    # кнопка submit, для пользователя отображена как send
    submit = SubmitField('send')

class SinForm(FlaskForm):
    # Фаза
    phase = FloatField('Фаза')
    # Амплитуда
    amplitude = FloatField('Амплитуда')
    # Частота
    rate = FloatField('Частота')
    # Диапазон
    range_from = FloatField('От:')
    range_to = FloatField('До: ')

    points_amount = IntegerField('Количество точек')

    # Формат вывода
    output_select = SelectField('Выбор вывода:', choices=[('txt','Текстовый список'), ('html','HTML-таблица'), ('md','Markdown-таблица')])

    submit = SubmitField('Отправить')

# функция обработки запросов на адрес 127.0.0.1:5000/net
# модуль проверки и преобразование имени файла
# для устранения в имени символов типа / и т.д.
from werkzeug.utils import secure_filename
import os
# подключаем наш модуль и переименовываем
# для исключения конфликта имен
import net as neuronet


# метод обработки запроса GET и POST от клиента
@app.route("/net", methods=['GET', 'POST'])
def net():
    # создаем объект формы
    form = NetForm()
    # обнуляем переменные передаваемые в форму
    filename = None
    neurodic = {}
    # проверяем нажатие сабмит и валидацию введенных данных
    if form.validate_on_submit():
        # файлы с изображениями читаются из каталога static
        filename = os.path.join('./static', secure_filename(form.upload.data.filename))
        fcount, fimage = neuronet.read_image_files(10, './static')
        # передаем все изображения в каталоге на классификацию
        # можете изменить немного код и передать только загруженный файл
        decode = neuronet.getresult(fimage)
        # записываем в словарь данные классификации
        for elem in decode:
            neurodic[elem[0][1]] = elem[0][2]

        # сохраняем загруженный файл
        form.upload.data.save(filename)
    # передаем форму в шаблон, так же передаем имя файла и результат работы нейронной
    # сети если был нажат сабмит, либо передадим falsy значения
    return render_template('net.html', form=form, image_name=filename, neurodic=neurodic)

import lxml.etree as ET
from math import sin
from lxml.builder import E
import matplotlib.pyplot as plt

@app.route("/sin", methods=['POST', 'GET'])
def sin_calc():
    selected_output = None
    form = SinForm()

    res_path = None

    if form.validate_on_submit():
        phase = float(form.phase.data)
        amplitude = float(form.amplitude.data)
        frequency = float(form.rate.data)
        high = float(form.range_to.data)
        low = float(form.range_from.data)
        points_cnt = float(form.points_amount.data)
        choice = form.output_select.data

        xs = []
        ys = []

        step = (high - low) / points_cnt
        x = low

        xml_data = None

        xslt_path = f'./static/xml/sin_to_{choice}.xslt'
        xml_data = ET.XML(f'<?xml-stylesheet type="text/xsl" href="{xslt_path}"?><sin></sin>')
        xml_sin_tag = xml_data.find('sin')

        while x <= high:
            xs.append(x)
            ys.append(sin(frequency * x + phase))

            xml_value_tag = ET.Element('value')

            xml_x_axis = ET.Element('x_axis')
            xml_x_axis.text = xs[-1]

            xml_y_axis = ET.Element('y_axis')
            xml_y_axis.text = ys[-1]

            xml_value_tag.append(xml_x_axis)
            xml_value_tag.append(xml_y_axis)
            xml_sin_tag.append(xml_value_tag)

            x += step

        res_path = './static/graph.png'
        
        plt.clf()
        plt.plot(xs, ys)
        plt.savefig(res_path)

        dom = ET.parse(xml_data)
        xslt = ET.parse(xslt_path)  # получаем трансформер
        transform = ET.XSLT(xslt)
        new_dom = transform(dom)
        # преобразуем из памяти dom в строку, возможно, понадобится указать кодировку
        selected_output = ET.tostring(new_dom)

    return render_template('sin.html', form=form, img_url=res_path, selected_output=selected_output)

    

from flask import request
from flask import Response
import base64
from PIL import Image
from io import BytesIO
import json

# метод для обработки запроса от пользователя
@app.route("/apinet", methods=['GET', 'POST'])
def apinet():
    # проверяем что в запросе json данные
    if request.mimetype == 'application/json':
        # получаем json данные
        data = request.get_json()
        # берем содержимое по ключу, где хранится файл # закодированный строкой base64
        # декодируем строку в массив байт используя кодировку utf-8
        # первые 128 байт ascii и utf-8 совпадают, потому можно
        filebytes = data['imagebin'].encode('utf-8')
        # декодируем массив байт base64 в исходный файл изображение
        cfile = base64.b64decode(filebytes)
        # чтобы считать изображение как файл из памяти используем BytesIO
        img = Image.open(BytesIO(cfile))
        decode = neuronet.getresult([img])
        neurodic = {}
        for elem in decode:
            neurodic[elem[0][1]] = str(elem[0][2])
            print(elem)
        # пример сохранения переданного файла
        # handle = open('./static/f.png','wb')
        # handle.write(cfile)
        # handle.close()
    # преобразуем словарь в json строку
    ret = json.dumps(neurodic)
    # готовим ответ пользователю
    resp = Response(response=ret,
                    status=200,
                    mimetype="application/json")
    # возвращаем ответ
    return resp

@app.route("/apixml", methods=['GET', 'POST'])
def apixml():
    # парсим xml файл в dom
    dom = ET.parse("./static/xml/file.xml")  # парсим шаблон в dom
    xslt = ET.parse("./static/xml/file.xslt")  # получаем трансформер
    transform = ET.XSLT(xslt)
    # преобразуем xml с помощью трансформера xslt
    newhtml = transform(dom)
    # преобразуем из памяти dom в строку, возможно, понадобится указать кодировку
    strfile = ET.tostring(newhtml)
    return strfile
  

import os
from matplotlib import pyplot as plt
from PIL import Image, ImageFilter


# метод обработки запроса GET и POST от клиента
@app.route("/imgfilter", methods=['GET', 'POST'])
def imgfilter():
    # создаем объект формы
    form = NetForm()
    # проверяем нажатие сабмит и валидацию введенных данных
    filename1 = None
    filename2 = None
    if form.validate_on_submit():
        filename1 = Image.open('./static/image0008.png')
        filename2 = filename1.filter(ImageFilter.MedianFilter(size=9))
        filename2.savefig('./static/result.png')

        # сохраняем загруженный файл
        form.upload.data.save('./static/result.png')
    # передаем форму в шаблон, так же передаем имя файла и результат работы нейронной
    # сети если был нажат сабмит, либо передадим falsy значения
    return render_template('imgfilter.html', form=form, image_name1=filename1, image_name2=filename2,)