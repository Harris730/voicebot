import speech_recognition as s
import webbrowser
import pyttsx3
import datetime
import requests
from pymongo import MongoClient
from word2number import w2n

recog = s.Recognizer()
client = MongoClient("mongodb://localhost:27017/")


def add_records():
 db = client["my_records"]
 orders_collection = db["orders"]
 while True:  
        speak("Tell number of records")
        n = extract_all_numbers(listen())
        if n:
            speak(f"Records to be entered are:{n[0]}")
            break
        else:
            speak("invalid number")

 orders = []
 for i in range(n[0]):
    print(f"\nEnter details for order #{i+1}:")
    while True:
     try:
        while True:
          speak("Tell order Id")
          order_id = extract_all_numbers(listen())
          if order_id:
                print(order_id[0])
                break
          speak("invalid id")
        while True:
          speak("Tell product name")
          product = listen()
          if product:
                print(product)
                break
          speak("invalid product")
        while True:
          speak("Tell customer id")
          c_id=extract_all_numbers(listen())
          if c_id:
                print(c_id[0])
                break
          speak("invalid customer id")
        url = "http://localhost:5000/add-order"
        payload = {
                "order_id": order_id[0],
                "product": product,
                "c_id": c_id[0]
            }
        response = requests.post(url, json=payload)
        if response.status_code == 201:
            print("Order added successfully!")
            print(response.json())
            break
        elif response.status_code == 409:
            print("Order ID already exists. Please re-enter the order.")
            speak("Order already exists. Please say a different order ID.")
            continue 
        else:
            print(" Failed to add order.")
            print(response.status_code, response.json())
            break
     except ValueError:
        print("Invalid input. Skipping this entry.")
        continue 

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
    elif "add data" or "add records" in c.lower(): 
       add_records()
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
    city  = requests.get("http://api.ipify.org").text
    #print(city)
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

def listen():
    print("Say something...")
    try:
        with s.Microphone() as source:
                speak("Listening for command...")
                audio = recog.listen(source)
                command = recog.recognize_google(audio)
                print("Command received:", command)
               # Process(command)
                if "stop" in command.lower():
                    speak("Exiting... You said stop")
                    print("Exiting... You said end")
                    exit()
                return command.lower()
    except Exception as e:
        print("Error:", e)
        return ""

def extract_all_numbers(text):
    words = text.lower().split()
    numbers = []
    i = 0
    while i < len(words):
        for j in range(len(words), i, -1):
            chunk = ' '.join(words[i:j])
            try:
                num = w2n.word_to_num(chunk)
                numbers.append(num)
                i = j - 1 
                break
            except ValueError:
                continue
        i += 1
    return numbers

def update_order():
     db = client["my_records"]
     orders_collection = db["orders"]
     try:
         while True:
                speak("Tell order id")
                order_id = extract_all_numbers(listen())
                existing_order = orders_collection.find_one({"order_id": order_id[0]})
                if not existing_order:
                    print(f"No order found with order_id {order_id}. Please try again.")
                    continue
                else:
                  #  print(f" Found order: {existing_order}")
                    break
         while True:
            speak("Tell product name")
            product = listen()
            if product:
                    break
            speak("invalid product")
         while True:
            speak("Tell customer id")
            c_id_input = extract_all_numbers(listen())
            if c_id_input:
                break
            speak("invalid Customer id")
         update_data = {}
         if product:
                 update_data["product"] = product
         if c_id_input:
                 update_data["c_id"] = c_id_input[0]

         if not update_data:
                print("No fields to update. Exiting.")
                return
         try:
            url =f"http://127.0.0.1:5000/update-order/{order_id[0]}"
            response = requests.put(url, json=update_data)
            print(response.json())
         except Exception as e:
            print(" Error while connecting to the server:", e)

     except ValueError:
              print(" Invalid input.")

def get_orders():
     db = client["my_records"]
     orders_collection = db["orders"]
     url = "http://127.0.0.1:5000/get-items"
     response= requests.get(url)
     if response.status_code== 200:
         orders= response.json()
         for i, order in enumerate(orders):
             speak (f"For order{1+i}")
             speak (f"Order_id :{order['order_id']} ")
             speak (f"Product :{order['product']} ")
             speak (f"Customer ID :{order['c_id']} ")
             print(i+1)
     else:
         print("unable to get response")     
         
            
if __name__ == "__main__":  
    get_orders()
   
#   while True:
#     print("Say something...")
#     try:
#         with s.Microphone() as source:
#             print("listening...........")
#             audio = recog.listen(source, timeout=8, phrase_time_limit=1)
#         word = recog.recognize_google(audio)
#         print(word)
#         word = word.lower()
#         if (word == "welcome"):
#             speak("YES")
#             perfom =listen()
#             Process(perfom)
#             #add_records()
#         elif "stop" in word:
#             speak("Exiting... You said stop")
#             print("Exiting... You said end")
#             exit()
#     except Exception as e:
#         print("Error:", e)
