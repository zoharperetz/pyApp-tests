from flask import Flask, render_template, request, jsonify
from geopy.geocoders import Nominatim
import requests
import venv


app = Flask(__name__)

def get_data(values):
    lat = values[0]
    lon = values[1]
    
    data_obj = requests.get(f"http://api.weatherunlocked.com/api/forecast/{lat},{lon}?app_id={venv.app_id}&app_key={venv.app_key}")
    data_obj = data_obj.json()
    data_list = data_obj["Days"]
    days_list = []   #array of dictionaries data about all 7 days/ len = 7
    for item in data_list:
       days_list.append(item)
       
    for i in range(0, 7):
       print(f"day {i+1}: {days_list[i]['date']} {days_list[i]['temp_max_c']} {days_list[i]['temp_min_c']}")
    return days_list 


@app.route("/", methods=["POST","GET"])
def home():  
    res = ""
    if request.method == "POST":
        try:
           userInput = request.form["City"]
           loc = Nominatim(user_agent="GetLoc")
           get_loc = loc.geocode(userInput)
           lat = get_loc.latitude
           lon = get_loc.longitude
           print(get_loc)
           print(f"lat: {lat} lon: {lon}")
           res = get_data([lat, lon])
           return render_template("index.html", data=res, address=get_loc)
        except Exception: 
           message = "invalid input"
           return render_template("index.html", message=message)
    if request.method == "GET":
        return render_template("index.html")
      
  
   
if __name__ == "__main__":
   app.run(host='0.0.0.0', port=5000)

