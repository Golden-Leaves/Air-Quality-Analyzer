import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Float,DateTime
import requests
from datetime import datetime,timezone,timedelta
import time
from db_models import db,AirData,Weather
import threading
import gunicorn
os.chdir(os.path.dirname(os.path.abspath(__file__)))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///air.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
with app.app_context():
    db.create_all()
    
def collect_data():
    while True:
        print("Fetching Data...")
        main()
        time.sleep(900)
        
@app.route("/")
def index():
    print("Hi hi hi I'm online.")
    return
        
        
def get_air_data(api_key,country,state,city) -> AirData:
        params = {"key":api_key,
              "country":country,
              "state":state,
              "city":city}
        response = requests.get("http://api.airvisual.com/v2/city",params=params)
        # response = requests.get("http://api.airvisual.com/v2/cities",params=params)
        response.raise_for_status()
        data = response.json()
        data = data["data"]
        pollution = data["current"]["pollution"]
        weather = data["current"]["weather"]
        coords = data["location"]["coordinates"]

        #Refactor timestamp
        ts = datetime.fromisoformat(pollution["ts"].replace("Z", "+00:00"))
        
        air_entry = AirData(
            city=data["city"],
            state=data["state"],
            country=data["country"],
            longitude=coords[0],
            latitude=coords[1],
            ts=ts,
            aqi_us=pollution["aqius"],
            main_pollutant_us=pollution["mainus"],
        )
        return air_entry
    
def get_weather_data(api_key,lon,lat,timestamp = None) -> Weather:
    #timestamp is IQAir's, so the two match 1:1
    params = {
    "lon": lon,
    "lat":lat,
    "dt": int(time.time()),
    "appid": api_key,
    "unit": "metric"
}
    response = requests.get("https://api.openweathermap.org/data/2.5/weather",params=params)
    response.raise_for_status()
    data = response.json()
    weather_meta = data["weather"][0]    
    main_metrics = data["main"]          
    sys_info = data["sys"]               #Sunrise, sunset
    wind_info = data["wind"]  
    if not timestamp:
        timestamp = datetime.fromtimestamp(data["dt"], tz=timezone.utc)         
    weather_entry = Weather(
        city_name =data["name"],
        country = sys_info["country"],
        latitude = data["coord"]["lat"],
        longitude = data["coord"]["lon"],

        weather_id=weather_meta["id"],
        weather_main=weather_meta["main"],
        weather_description=weather_meta["description"],
        icon_code = weather_meta["icon"],

        temp_c = main_metrics["temp"],
        feels_like_c = main_metrics["feels_like"],
        temp_min_c = main_metrics["temp_min"],
        temp_max_c = main_metrics["temp_max"],
        pressure_hpa = main_metrics["pressure"],
        humidity = main_metrics["humidity"],
        sea_level_hpa = main_metrics.get("sea_level"),
        ground_level_hpa= main_metrics.get("grnd_level"),

        visibility_m = data.get("visibility"),

        wind_speed_mps = wind_info["speed"],
        wind_deg = wind_info["deg"],
        wind_gust_mps = wind_info.get("gust"),

        cloud_pct = data["clouds"]["all"],

        sunrise = datetime.fromtimestamp(sys_info["sunrise"], tz=timezone.utc),
        sunset = datetime.fromtimestamp(sys_info["sunset"], tz=timezone.utc),

        ts=timestamp, #datetime.fromtimestamp(data["dt"], tz=timezone.utc)
        timezone_offset=data["timezone"],
        source_id=data["id"]
    )
    return weather_entry

def main():
    COUNTRY = "Vietnam"
    STATE = "Tinh Binh Duong"
    CITY = "Thu Dau Mot"
    current_directory = os.path.dirname(os.path.abspath(__file__))
    env_path = os.path.join(current_directory,".env")
    load_dotenv(env_path)
    iqair_api_key = os.getenv("IQAIR_API_KEY")
    openweather_api_key = os.getenv("OPENWEATHER_API_KEY")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
    }
    
    
    air_data = get_air_data(api_key=iqair_api_key,country=COUNTRY,state=STATE,city=CITY)
    weather_data = get_weather_data(api_key=openweather_api_key,lon=air_data.longitude,lat=air_data.latitude,timestamp=air_data.ts)

   
    with app.app_context():
        db.session.add_all([air_data,weather_data])
        db.session.commit()
if __name__ == "__main__":
    t = threading.Thread(target=collect_data)
    t.daemon = True
    t.start()