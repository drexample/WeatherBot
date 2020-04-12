import requests
from flask import Flask, render_template

from flask_wtf import FlaskForm

from wtforms import TextField, FileField
from wtforms.validators import Required

import os

app = Flask(__name__)
DEBUG = True
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
city_id = 0
appid = "2fc8d987a6c4f8b6f6c5e0c07b84e97e"



class WeatherForm(FlaskForm):
    Place = TextField("Населенный пункт: ")

@app.route('/index', methods=['GET', 'POST'])
def index():
    form = WeatherForm()
    if form.validate_on_submit():
        result = get_weather(form.Place.data)
    else:
        result = 'Тык.'
    return render_template('test.html', form=form, result=result)
def get_weather(weatherplace):
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/find",
                     params={'q': weatherplace, 'type': 'like', 'units': 'metric', 'APPID': appid})
        data = res.json()
        cities = ["{} ({})".format(d['name'], d['sys']['country'])
                  for d in data['list']]
        print("city:", cities)
        city_id = data['list'][0]['id']
        print('city_id=', city_id)
    except Exception as e:
        print("Exception (find):", e)
        pass
        return "Нет информации :C"
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                     params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
        data = res.json()
        result = []
        result = "Погода для населенного пункта " + weatherplace + ": сейчас " + str(data['weather'][0]['description']) + ", температура " + str(data['main']['temp']) + " градусов по Цельсию, скорость ветра: " + str(data['wind']['speed']) + " м/с, максимальная температура на сегодня: " + str(data['main']['temp_max']) + ", минимальная: " + str(data['main']['temp_min'])
        print(data)
        print("temp:", data['main']['temp'])
        print("temp_min:", data['main']['temp_min'])
        print("temp_max:", data['main']['temp_max'])
        return result
    except Exception as e:
        print("Exception (weather):", e)
        pass
