import datetime
import requests

def update_dashboard():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Open-Meteo free API (Bahawalpur coordinates)
    url = "https://api.open-meteo.com/v1/forecast?latitude=29.3956&longitude=71.6836&current_weather=true"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        current = data.get("current_weather", {})
        temp = current.get("temperature")
        windspeed = current.get("windspeed")
        
        log_entry = f"[{now}] - Temp: {temp}°C | Wind: {windspeed} km/h"
        print(log_entry)
        
        # 1. Read existing logs
        logs = []
        try:
            with open("automation_log.txt", "r") as file:
                logs = file.readlines()
        except FileNotFoundError:
            pass
        
        # Naya log sab se upar add karo
        logs.insert(0, log_entry + "\n")
        logs = logs[:20] # Sirf akhri 20 logs rakho taake list lambi na ho
        
        # Save back to text file
        with open("automation_log.txt", "w") as file:
            file.writelines(logs)
            
        # 2. Generate a Web Page (index.html) automatically
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Bahawalpur Live Weather Cloud Dashboard</title>
            <script src="https://cdn.tailwindcss.com"></script>
        </head>
        <body class="bg-slate-900 text-white font-sans p-6">
            <div class="max-w-xl mx-auto bg-slate-800 p-6 rounded-xl shadow-xl border border-slate-700">
                <h1 class="text-2xl font-bold mb-1 text-emerald-400">🌤️ Bahawalpur Cloud Weather</h1>
                <p class="text-slate-400 text-sm mb-6">Automated live dashboard running on GitHub Actions cloud.</p>
                
                <div class="bg-slate-900 p-4 rounded-lg border border-slate-700 mb-6">
                    <h2 class="text-xs uppercase tracking-wider text-slate-500 font-semibold mb-1">Latest Reading</h2>
                    <div class="text-2xl font-bold text-yellow-400">{temp}°C <span class="text-sm font-normal text-slate-300">| Wind: {windspeed} km/h</span></div>
                    <div class="text-xs text-slate-500 mt-1">Last updated: {now}</div>
                </div>

                <h2 class="text-lg font-semibold mb-3 text-slate-200">📜 History Logs</h2>
                <div class="bg-slate-900 p-4 rounded-lg font-mono text-xs text-slate-300 space-y-2 max-h-60 overflow-y-auto border border-slate-700">
        """
        
        for line in logs:
            html_content += f"<div class='border-b border-slate-800 pb-1'>{line.strip()}</div>\n"
            
        html_content += """
                </div>
            </div>
        </body>
        </html>
        """
        
        with open("index.html", "w") as f:
            f.write(html_content)
        print("Dashboard index.html generated successfully!")
        
    else:
        print("Failed to fetch weather data")

if __name__ == "__main__":
    update_dashboard()
