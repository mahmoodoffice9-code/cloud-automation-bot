import datetime
import requests

def fetch_weather():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Open-Meteo free API jo baghair kisi key ke weather deti hai (Bahawalpur coordinates: 29.3956, 71.6836)
    url = "https://api.open-meteo.com/v1/forecast?latitude=29.3956&longitude=71.6836&current_weather=true"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        current = data.get("current_weather", {})
        temp = current.get("temperature")
        windspeed = current.get("windspeed")
        
        log_entry = f"[{now}] - Bahawalpur Weather: Temp: {temp}°C, Wind: {windspeed} km/h\n"
        print(log_entry)
        
        # File mein save karna
        try:
            with open("automation_log.txt", "a") as file:
                file.write(log_entry)
            print("Weather log successfully updated!")
        except Exception as e:
            print(f"Error writing file: {e}")
    else:
        print("Failed to fetch weather data")

if __name__ == "__main__":
    fetch_weather()
