import speech_recognition as s
import webbrowser
import pyttsx3
import datetime
import requests
from word2number import w2n
import requests
import json


recog = s.Recognizer()


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
         gemini_chat(c)
   
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
            print(f"City: {city}")
            print(f"Region: {region}")
            print(f"Country: {country}")
            print(f"Postal Code: {postal}")
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
                audio = recog.listen(source, timeout=100)
                command = recog.recognize_google(audio)
                print("Command received:", command)
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

def gemini_chat(user_input):
    API_KEY = "AIzaSyBpmbhirCwNPzFTaLmfgy0GMv0uhCxLP94"
    URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": API_KEY
    }
    payload = {
        "contents": [
            {"parts": [{"text": user_input}]}
        ]
    }

    try:
        response = requests.post(URL, headers=headers, json=payload)
        data = response.json()
        answer = data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception:
        answer = "Sorry, I could not process that."

    speak(answer)
    print("Gemini:", answer)


def voice_loop():
    speak("Hello! I am your assistant")
    print("Listening... Say 'stop' to exit.")

    while True:
        try:
            with s.Microphone() as source:
                recog.adjust_for_ambient_noise(source)
                print("Listening...")
                audio = recog.listen(source, timeout=10, phrase_time_limit=10)

            word = recog.recognize_google(audio).lower()
            print("You said:", word)

            if word == "stop":
                speak("Goodbye!")
                print("Exiting chat.")
                break
            # Call your Process function
            Process(word)

        except s.WaitTimeoutError:
            print("Listening timed out. Try again.")
        except s.UnknownValueError:
            print("Sorry, I did not catch that.")
        except s.RequestError as e:
            print("Could not request results; {0}".format(e))
        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":  


    voice_loop()

#   while True:
#     print("Say something...")
#     try:
#         with s.Microphone() as source:
#             print("listening...........")
#             audio = recog.listen(source, timeout=15, phrase_time_limit=1)
#         word = recog.recognize_google(audio)
#         print(word)
#         word = word.lower()
#         if (word == "welcome"):
#             speak("YES")
#             perfom =listen()
#             Process(perfom)
#         elif "stop" in word:
#             speak("Exiting... You said stop")
#             print("Exiting... You said end")
#             exit()
#     except Exception as e:
#         print("Error:", e)
   
    
    