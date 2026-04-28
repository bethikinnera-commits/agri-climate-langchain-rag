import requests
from datetime import datetime, timedelta

API_KEY = "46511a39a7967e91af6bd9dc4452f9bb"


def get_3day_climate(city):

    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"

    res = requests.get(url)
    data = res.json()

    if data.get("cod") != "200":
        return f"Weather API Error: {data.get('message')}"

    rain_flag = False
    report = ""

    today = datetime.utcnow().date()

    for i in range(1, 4):
        day = today + timedelta(days=i)

        temps = []
        rains = []

        for item in data["list"]:
            dt = datetime.utcfromtimestamp(item["dt"]).date()

            if dt == day:
                temps.append(item["main"]["temp"])
                rains.append(item.get("rain", {}).get("3h", 0))

        if temps:
            total_rain = sum(rains)
            avg_temp = sum(temps) / len(temps)

            if total_rain > 0:
                rain_flag = True

            report += f"""
Date: {day}
Temp: {avg_temp:.1f}°C
Rain: {total_rain} mm
-------------------
"""

    # 🔥 FINAL DECISION LOGIC
    if rain_flag:
        return "❌ Not recommended to spray pesticides. Rain expected in next 3 days.\n\n" + report
    else:
        return "✔ Safe to spray pesticides. No rain expected.\n\n" + report