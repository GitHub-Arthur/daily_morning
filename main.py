from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]

city_cjy = os.environ['CITY_CJY']
template_id_cjy = os.environ["TEMPLATE_ID_CJY"]
user_id_cjy = os.environ["USER_ID_CJY"]



def get_weather():
  url = "https://devapi.qweather.com/v7/weather/3d?location=101210601&key=2698ab9d271f4ae8bd7e3899e8bb4902"
  res = requests.get(url).json()
  weather = res['daily'][0]
  tomorrow = res['daily'][1]
  return weather['textDay'], \
         math.floor(weather['tempMin']),\
         math.floor(weather['tempMax']),\
         weather['windDirDay'], \
         weather['windScaleDay'], \
         tomorrow['sunrise']


def get_weather_cjy():
  url = "https://devapi.qweather.com/v7/weather/3d?location=101210101&key=2698ab9d271f4ae8bd7e3899e8bb4902"
  res = requests.get(url).json()
  weather = res['daily'][0]
  tomorrow = res['daily'][1]
  return weather['textDay'], \
         math.floor(weather['tempMin']),\
         math.floor(weather['tempMax']),\
         weather['windDirDay'], \
         weather['windScaleDay'], \
         tomorrow['sunrise']

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_words_pyq():
  words = requests.get("https://api.shadiao.pro/pyq")
  if words.status_code != 200:
    return get_words_pyq()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea,  low, high, wind, windScale, sunrise = get_weather()
data = {
        "weather": {"value":wea, "color":get_random_color()},  # 天气
        "low":{"value":low, "color":get_random_color()},  # 最低气温
        "high":{"value":high, "color":get_random_color()},  # 最高气温
        "wind": {"value": wind, "color": get_random_color()},  # 风力
        "windScale": {"value": windScale, "color": get_random_color()},  # 风力等级
        "sunrise": {"value": sunrise, "color": get_random_color()},  # 明日日出时间
        "love_days":{"value":get_count(), "color":get_random_color()},  # 恋爱纪念日
        "birthday_left":{"value":get_birthday(), "color":get_random_color()},  # 宝宝生日
        "words":{"value":get_words(), "color":get_random_color()},  # 彩虹屁
        "words_pyq": {"value": get_words_pyq(), "color": get_random_color()}  # 朋友圈文案
}
# res = wm.send_template(user_id, template_id, data)
# print(res)

wm = WeChatMessage(client)
wea,  low, high, wind, windScale, sunrise = get_weather_cjy()
data = {
        "weather": {"value":wea, "color":get_random_color()},  # 天气
        "low":{"value":low, "color":get_random_color()},  # 最低气温
        "high":{"value":high, "color":get_random_color()},  # 最高气温
        "wind": {"value": wind, "color": get_random_color()},  # 风力
        "windScale": {"value": windScale, "color": get_random_color()},  # 风力等级
        "sunrise": {"value": sunrise, "color": get_random_color()},  # 明日日出时间
        "love_days":{"value":get_count(), "color":get_random_color()},  # 恋爱纪念日
        "birthday_left":{"value":get_birthday(), "color":get_random_color()},  # 宝宝生日
        "words":{"value":get_words(), "color":get_random_color()},  # 彩虹屁
        "words_pyq": {"value": get_words_pyq(), "color": get_random_color()}  # 朋友圈文案
}
res = wm.send_template(user_id_cjy, template_id_cjy, data)
print(res)

###
