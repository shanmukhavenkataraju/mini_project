import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os

# Initialize the speech engine
try:
    engine = pyttsx3.init()
    print("Speech engine initialized.")
except Exception as e:
    print(f"Error initializing speech engine: {e}")
    exit()

# Set speech rate and volume (optional)
engine.setProperty('rate', 150)  # Speed of speech
engine.setProperty('volume', 1.0)  # Volume level (1.0 is max)

# Function to convert text to speech
def speak(text):
    try:
        print(f"Speaking: {text}")  # Debug print statement
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Error in speak function: {e}")

# Function to greet the user
def greet():
    try:
        hour = datetime.datetime.now().hour
        if 0 <= hour < 12:
            speak("Good Morning!")
        elif 12 <= hour < 18:
            speak("Good Afternoon!")
        else:
            speak("Good Evening!")
        speak("I am your voice assistant. How can I help you today?")
    except Exception as e:
        print(f"Error in greet function: {e}")

# Function to take a voice command from the user
def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        try:
            audio = r.listen(source)
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that. Could you repeat?")
            return "None"
        except sr.RequestError:
            print("Sorry, there seems to be a problem with the speech recognition service.")
            return "None"
        except Exception as e:
            print(f"Error in take_command function: {e}")
            return "None"
    
    return query.lower()

# Function to handle commands
def handle_query(query):
    try:
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "").strip()
            try:
                result = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                speak(result)
            except wikipedia.exceptions.DisambiguationError:
                speak("The search term was ambiguous. Please be more specific.")
            except wikipedia.exceptions.PageError:
                speak("Sorry, I couldn't find any results for that query.")
            except Exception:
                speak("Sorry, an error occurred while searching Wikipedia.")

        elif 'open youtube' in query:
            speak("Opening YouTube")
            webbrowser.open("https://www.youtube.com")

        elif 'open google' in query:
            speak("Opening Google")
            webbrowser.open("https://www.google.com")

        elif 'the time' in query:
            str_time = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {str_time}")

        elif 'play music' in query:
            music_dir = r'C:\Users\amrutha\Desktop\Music'  # Path to your music directory
            if os.path.exists(music_dir):
                songs = [song for song in os.listdir(music_dir) if song.endswith('.mp3')]
                if songs:
                    os.startfile(os.path.join(music_dir, songs[0]))
                else:
                    speak("No music files found.")
            else:
                speak("Music directory not found.")

        elif 'open code' in query:
            code_path = r"C:\Users\amrutha\Desktop\voice_recognition.py"  # Update this path as needed
            if os.path.exists(code_path):
                os.startfile(code_path)
            else:
                speak("Code file not found.")

        elif 'exit' in query or 'quit' in query:
            speak("Goodbye! Have a great day!")
            exit()
    except Exception as e:
        print(f"Error in handle_query function: {e}")

# Main Function
if __name__ == "__main__":
    # Your code here

    greet()
    while True:
        query = take_command()
        if query != "None":
            handle_query(query)
