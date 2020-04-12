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
        array_returned = get_weather(form.Place.data)
        result = array_returned[0]
        if(len(get_weather(form.Place.data)) > 1):
            result2 = array_returned[1]
    else:
        result = 'Тык.'
        result2 = ''
    return render_template('test.html', form = form, result = result , result2 = result2)



def generate_clothes_choice(temperature, weather):
    current_condition = weather['weather'][0]['main']
    thing_to_return = []
    if current_condition == "Thunderstorm":
        thing_to_return.append("На улице гроза. Советуем не выходить.")
    if current_condition == "Drizzle":
        thing_to_return.append("Советуем взять зонт или одежу с капюшоном.")
    if current_condition == "Rain":
        thing_to_return.append("Советуем взять зонт или одежу с капюшоном.")
    if current_condition == "Snow":
        thing_to_return.append("Советуем взять зонт или одежу с капюшоном.")
    if weather['clouds']['all'] < 20:
        thing_to_return.append("Советуем надеть солнечные очки или головной убор с козырьком.")
    if temperature > 20:
        thing_to_return.append("Советуем одеться по-легче.")
    elif temperature > 5:
        thing_to_return.append("Советуем одеться по-теплее.")
    elif temperature < 5:
        thing_to_return.append("Советуем одеться тепло.")    
    if weather['wind']['speed'] > 30:
        thing_to_return.append("Сильный ветер. Советуем надеть непродуваемую куртку.")
    elif weather['wind']['speed'] > 10:
        thing_to_return.append("Советуем надеть одежду с рукавами.")
    print(thing_to_return)
    return " ".join(thing_to_return)


def get_weather(weatherplace):
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/find",
                     params={'q': weatherplace, 'type': 'like', 'units': 'metric', 'APPID': appid})
        data = res.json()
        cities = ["{} ({})".format(d['name'], d['sys']['country'])
                  for d in data['list']]
        city_id = data['list'][0]['id']
    except Exception as e:
        print("Exception (find):", e)
        pass
        return "Нет информации :C"
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                     params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
        data = res.json()
        result = []
        result.append("Погода для населенного пункта " + weatherplace + ": сейчас " + str(data['weather'][0]['description']) + ", температура " + str(data['main']['temp']) + " градусов по Цельсию, скорость ветра: " + str(data['wind']['speed']) + " м/с, максимальная температура на сегодня: " + str(data['main']['temp_max']) + ", минимальная: " + str(data['main']['temp_min']))
        result.append(generate_clothes_choice(data['main']['temp'], data))
        return result
    except Exception as e:
        print("Exception (weather):", e)
        pass
