import pyttsx3
import datetime
import requests
import pyjokes
import json
import speech_recognition as sr

engine = pyttsx3.init()

# Speak function
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Listen function for voice commands
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening...")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            command = recognizer.recognize_google(audio).lower()
            return command
        except sr.UnknownValueError:
            speak("Sorry, I didn't understand that.")
            return None
        except sr.RequestError:
            speak("Could not connect to the voice recognition service.")
            return None

# Function to get current date and time
def get_date_time():
    current_time = datetime.datetime.now().strftime("%I:%M %p")  # Time in 12-hour format
    current_date = datetime.datetime.now().strftime("%A, %d %B %Y")  # Date in readable format
    return f"Today is {current_date} and the current time is {current_time}."

# Greet the user
def greet_user():
    hour = datetime.datetime.now().hour
    if hour < 12:
        greeting = "Good Morning!"
    elif 12 <= hour < 18:
        greeting = "Good Afternoon!"
    else:
        greeting = "Good Evening!"
    
    date_time_message = get_date_time()
    combined_message = f"{greeting} {date_time_message}"
    speak(combined_message)
    print(combined_message)

# Fetch weather by city
def get_weather_by_city():
    speak("Which city do you want to know the weather for?")
    city = listen()
    if not city:
        return
    
    api_key = "d462bef4177dd676722d96c92b6776fa"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        message = f"The weather in {city} is {weather} with a temperature of {temp} degrees Celsius."
        speak(message)
        print(message)
    else:
        error_message = response.json().get('message', 'Unknown error')
        speak(f"Could not fetch weather details. Error: {error_message}")
        print(f"Error: {error_message}")

# Fetch jokes
def get_jokes():
    joke = pyjokes.get_joke()
    speak(joke)
    print(joke)

# Fetch news
def get_news():
    speak("What type of news are you interested in?")
    query = listen()
    if not query:
        return
    
    speak("Enter the language for news, for example, 'English' or 'Hindi'.")
    language = listen()
    if not language:
        return
    
    speak("Enter the country for news, for example, 'India' or 'United States'.")
    location = listen()
    if not location:
        return
    
    language_code = {"english": "en", "hindi": "hi"}.get(language.lower(), "en")
    country_code = {"india": "in", "united states": "us"}.get(location.lower(), "us")

    api_key = "pub_6104669217ac160b5ada47cdc8c472cb750e9"
    url = f"https://newsdata.io/api/1/news?apikey={api_key}&q={query}&language={language_code}&country={country_code}"
    r = requests.get(url)
    if r.status_code != 200:
        speak("Failed to fetch news. Please try again later.")
        print("Failed to fetch news.")
    else:
        news = r.json()
        if "results" in news and news["results"]:
            for article in news["results"][:5]:  # Limiting to 5 articles for brevity
                title = article.get('title', 'No title available')
                description = article.get('description', 'No description available')
                speak(f"Title: {title}")
                speak(f"Description: {description}")
                print(f"Title: {title}")
                print(f"Description: {description}")
                print("--------------------------------------")
        else:
            speak("No articles found for your query.")
            print("No articles found.")

# Main program
if __name__ == "__main__":
    greet_user()
    while True:
        speak("What would you like me to do? Options are weather, joke, news, or exit.")
        command = listen()
        if not command:
            continue

        if "weather" in command:
            get_weather_by_city()
        elif "joke" in command:
            get_jokes()
        elif "news" in command:
            get_news()
        elif "exit" in command:
            speak("Goodbye!")
            break
        else:
            speak("I didn't understand that. Please try again.")