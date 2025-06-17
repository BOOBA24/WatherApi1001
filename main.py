from fastapi import FastAPI
from datetime import datetime
from dotenv import load_dotenv
import requests
import pytz  # ✅ Ajout pour gérer les fuseaux horaires
import uvicorn
load_dotenv()

app = FastAPI()

CITY = "Toronto"
API_KEY = 'd2f188f5c57dd17f4bc59c73e0c0fffc'

def get_weather():
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
    
    try:
        response = requests.get(weather_url)
        data = response.json()
        
        weather = {
            'city': data['name'],
            'temperature': data['main']['temp'],
            'description': data['weather'][0]['description']
        }
    except Exception as e:
        print(e)
        weather = {
            'city': 'N/A',
            'temperature': 'N/A',
            'description': 'N/A'
        }
    return weather

@app.get("/info")
async def get_info():
    # ✅ Appliquer fuseau horaire local
    tz = pytz.timezone("America/Toronto")
    current_datetime = datetime.now(tz)

    formatted_date = current_datetime.strftime("%Y-%m-%d")
    formatted_time = current_datetime.strftime("%H:%M:%S")

    weather = get_weather()

    return {
        "date": formatted_date,
        "time": formatted_time,
        "weather": weather
    }
