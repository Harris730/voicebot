import speech_recognition as s
import webbrowser
import pyttsx3
import datetime
import requests
from pymongo import MongoClient
# Function to speak text
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def Process(c):
    if "time" in c or "date" in c:
        timing()
    elif "open google" in c.lower():
        webbrowser.open("https://www.google.co.uk/")
    elif "location" in c.lower():
        get_ip_location()
    elif "weather today" in c.lower():
        get_weather()   
    else:
        speak("I cant understand")
   
def timing():
    now = datetime.datetime.now()

    date = now.strftime("%A, %B %d, %Y")     # Example: Monday, July 01, 2025
    time = now.strftime("%I:%M %p")          # Example: 09:45 AM

    message = f"Today is {date}, and the time is {time}"
    print(message)
    speak(message)

def get_ip_location():
    try:
        response = requests.get("https://ipinfo.io/json")
        if response.status_code == 200:
            data = response.json()
            ip = data.get("ip")
            city = data.get("city")
            region = data.get("region")
            country = data.get("country")
            postal = data.get("postal")
            org = data.get("org")
            loc = data.get("loc")  # "lat,long"
            
            if loc:
                latitude, longitude = map(float, loc.split(','))
            else:
                latitude, longitude = None, None

           # print(f"IP Address: {ip}")
            speak(f"City: {city}")
            speak(f"Region: {region}")
            speak(f"Country: {country}")
           #3 speak(f"Postal Code: {postal}")
           # speak(f"Organization: {org}")
            print(f"City: {city}")
            print(f"Region: {region}")
            print(f"Country: {country}")
            print(f"Postal Code: {postal}")
          #  print(f"Organization: {org}")
            #print(f"Latitude: {latitude}, Longitude: {longitude}")
        else:
            print("Failed to get location data.")
    except Exception as e:
        print("Error:", e)
     
def get_weather():
    #city="London"
    city  = requests.get("http://api.ipify.org").text
    print(city)
    api_key = "56f406e1aabd4e69abb192259250207"  
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"

    try:
        response = requests.get(url)
        data = response.json()

        if "error" in data:
            speak("City not found. Please try again.")
            return

        location = data["location"]
        current = data["current"]

        city_name = location["name"]
        country = location["country"]
        local_time = location["localtime"]
        temp = current["temp_c"]
        feels_like = current["feelslike_c"]
        condition = current["condition"]["text"]
        humidity = current["humidity"]
        wind = current["wind_kph"]

       # message = (
        speak (f"Weather in {city_name}, {country} at {local_time.split(" ")[0]}:\n")
        speak (f"{condition}. Temperature is {temp}°C, feels like {feels_like}°C.\n")
        speak (f"Humidity is {humidity}%, and wind speed is {wind} kilometers per hour.")
       # )

      #  speak(message)

    except Exception as e:
        speak("There was an error fetching the weather.")

# Function to listen and return recognized text
def listen():
    recog = s.Recognizer()
    print("Say something...")
    try:
        with s.Microphone() as source:
            print("listening...........")
            audio = recog.listen(source, timeout=8, phrase_time_limit=1)

        word = recog.recognize_google(audio)
        print(word)
        word = word.lower()
        if (word == "welcome"):
            speak("YES")
            with s.Microphone() as source:
                speak("Listening for command...")
                audio = recog.listen(source)
                command = recog.recognize_google(audio)
                print("Command received:", command)
                Process(command)
                return command.lower()
        elif "stop" in word:
            speak("Exiting... You said stop")
            print("Exiting... You said end")
            exit()
        else:
            print("Say correct word")
            return word

    except Exception as e:
        print("Error:", e)
        return ""

if __name__ == "__main__":
  # Connect to MongoDB
 client = MongoClient("mongodb://localhost:27017/")
 db = client["my_records"]
 orders_collection = db["orders"]

# Documents to insert
 orders = [
    {"order_id": 1, "product": "Ps4", "c_id": 100400},
    {"order_id": 2, "product": "Xbox Series X", "c_id": 100401},
    {"order_id": 3, "product": "Nintendo Switch", "c_id": 100402},
    {"order_id": 4, "product": "Gaming PC", "c_id": 100403},
    {"order_id": 5, "product": "VR Headset", "c_id": 100404},
    {"order_id": 6, "product": "Gaming Laptop", "c_id": 100405}
 ]

# Insert into MongoDB
 result = orders_collection.insert_many(orders)

# ✅ Print actual inserted IDs
 print("Inserted IDs:", result.inserted_ids)
   # while True:
    #    text = listen()
        #if text and "stop" in text:
        #    break
    # get_weather()
    #get_ip_location()
#    ip = requests.get("http://api.ipify.org").text
#    print(ip)