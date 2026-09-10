import datetime
import requests

def fetch_and_log():
    # Current date aur time nikalne ke liye
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Public API se random joke ya fact lene ke liye
    url = "https://api.chucknorris.io/jokes/random"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        joke = data.get("value")
        
        log_entry = f"[{now}] - {joke}\n"
        print(log_entry)
        
        # File mein data save karna
        try:
            with open("automation_log.txt", "a") as file:
                file.write(log_entry)
            print("Log successfully updated!")
        except Exception as e:
            print(f"Error writing file: {e}")
    else:
        print("Failed to fetch data from API")

if __name__ == "__main__":
    fetch_and_log()
