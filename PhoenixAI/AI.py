import datetime
from PyQt5 import *
from posixpath import supports_unicode_filenames
import time
from requests.api import get
from win32com.client.makepy import main
import pyautogui
import os
import sys
import requests
from bs4 import BeautifulSoup
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QTime, QTimer, QDate, Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from aiui import Ui_aiui
from joke.jokes import *
from joke.quotes import *
from pprint import pprint
from pyjokes import jokes_de
from random import choice
from googletrans import Translator
import speech_recognition as sr
import pyttsx3
import wikipedia
import webbrowser
import pywhatkit
import pyjokes
import randfacts
from PyDictionary import PyDictionary as pd
from os import system


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

webbrowser.register('chrome',
	None,
	webbrowser.BackgroundBrowser("C://Program Files (x86)//Google//Chrome//Application//chrome.exe"))
chrome_incog = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s --incognito'

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour <12:
        speak("Good Morning!")

    elif hour >= 4 and hour <12:
        speak("Good Evening!")

    else:
        speak("Good Afternoon!")

    speak("I am your AI Sir, how may I help you")

class MainThread(QThread):
    def __init__(self):
        super().__init__()

    def run(self):
        self.TaskExecution()

    def takeCommand(self):
            
        r=sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            r.pause_threshold = 1
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)

            try:
                print("Recognising...")
                self.query = r.recognize_google(audio, language='en-in')
                print(f"User said: {self.query}\n")

            except Exception as e:

                print("Say it again please...")
                speak("Say it again please...")
                return "None"
            return self.query


    def TaskExecution(self):
            wishMe()
            while True:
                                
                self.query =  self.takeCommand().lower()
                                        
                if 'wikipedia' in self.query:
                    speak("Searching...")
                    self.query = self.query.replace('wikipedia', '')
                    results = wikipedia.summary(self.query, sentences = 2)
                    speak("According to Wikipedia")
                    print(results)
                    speak(results)

                elif 'open chrome' in self.query:
                    speak("Opening Chrome")
                    chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
                    webbrowser.get(chrome_path).open('chrome://newtab')
                        
                elif 'close chrome' in self.query:
                    browserExe = "chrome.exe"
                    speak("closing Chrome")
                    os. system("taskkill /f /im "+browserExe)

                elif 'open notepad' in self.query:
                    path = 'C:\\Windows\\system32\\notepad.exe'
                    speak("opening Notepad")
                    os.startfile(path)

                elif 'close notepad' in self.query:
                    speak("Closing Notepad")
                    os.system("TASKKILL /F /IM notepad.exe")
                        
                elif 'open paint' in self.query:
                    path = 'C:\\Windows\\system32\\mspaint.exe'
                    speak("Opening Paint")
                    os.startfile(path)

                elif 'close paint' in self.query:
                    speak("Closing paint")
                    os.system("TASKKILL /F /IM paint.exe")

                elif 'open cmd' in self.query:
                    speak("Opening cmd")
                    os.startfile("C:\\Windows\\system32\\cmd.exe")

                elif 'close cmd' in self.query:
                    speak("Closing cmd")
                    os.system("TASKKILL /F /IM cmd.exe")

                elif 'Pranjal Srivastava' in self.query:
                    speak("Pranjal Srivastava is my owner and creator.")
                            
                elif 'how' in self.query:
                    speak("Searching...")
                    self.query = self.query.replace('how', '')
                    results = wikipedia.summary(self.query, sentences = 2)
                    print(results)
                    speak(results) 

                elif 'what' in self.query:
                    speak("Searching...")
                    self.query = self.query.replace('what', '')
                    results = wikipedia.summary(self.query, sentences = 2)
                    print(results)
                    speak(results) 

                elif 'who' in self.query:
                    speak("Searching...")
                    self.query = self.query.replace('who', '')
                    results = wikipedia.summary(self.query, sentences = 2)
                    print(results)
                    speak(results)

                elif 'where' in self.query:
                    speak("Searching...")
                    self.query = self.query.replace('where', '')
                    results = wikipedia.summary(self.query, sentences = 2)
                    print(results)
                    speak(results)
                        
                elif 'when' in self.query:
                    speak("Searching...")
                    self.query = self.query.replace('when', '')
                    results = wikipedia.summary(self.query, sentences = 2)
                    print(results)
                    speak(results)
                                
                elif 'open youtube' in self.query:
                    self.query = self.query.replace('open', '')
                    speak('opening' + self.query)
                    webbrowser.get('chrome').open('https://youtube.com')

                elif 'close youtube' in self.query:
                    speak("Closing Youtube")
                    os.system("TASKKILL /F /IM chrome.exe")

                elif 'open whatsapp' in self.query:
                    self.query = self.query.replace('open', '')
                    speak('opening' + self.query)
                    webbrowser.get('chrome').open('https://web.whatsapp.com/')

                elif 'open zinedu' in self.query:
                    self.query = self.query.replace('open', '')
                    speak('opening' + self.query)
                    webbrowser.get('chrome').open('https://zinedu.com')    

                elif 'open insta' in self.query:
                    self.query = self.query.replace('open', '')
                    speak('opening instagram')
                    webbrowser.get('chrome').open('https://instagram.com')

                elif 'open fb' in self.query:
                    self.query = self.query.replace('open', '')
                    speak('opening facebook')
                    webbrowser.get('chrome').open('https://fb.com')

                elif 'open google' in self.query:
                    self.query = self.query.replace('open', '')
                    speak('opening' + self.query)
                    webbrowser.get('chrome').open('https://google.com')

                elif 'open amazon' in self.query:
                    self.query = self.query.replace('open', '')
                    speak('opening' + self.query)
                    webbrowser.get('chrome').open('https://amazon.in')

                elif 'incognito mode' in self.query:
                    self.query = self.query.replace('open', '')
                    speak('opening' + self.query)
                    system("\"C://Program Files (x86)//Google//Chrome//Application//chrome.exe\" -incognito ")

                elif 'google in incognito' in self.query:
                    speak('opening' + self.query)
                    system("\"C://Program Files (x86)//Google//Chrome//Application//chrome.exe\" -incognito google.com")

                elif 'youtube in incognito' in self.query:
                    speak('opening' + self.query)
                    system("\"C://Program Files (x86)//Google//Chrome//Application//chrome.exe\" -incognito youtube.com")

                elif 'time' in self.query:
                    time = datetime.datetime.now().strftime('%I:%M %p')
                    speak(time)
                    print(time)

                elif 'play' in self.query:
                    video = self.query.replace('play', '')
                    speak('playing' + video)
                    pywhatkit.playonyt(video)

                elif 'joke' in self.query:
                    if 'tech joke' in self.query:
                        speak(pyjokes.get_joke())
                        print(pyjokes.get_joke())
                    else:
                        c=choice([icanhazdad, icndb])()
                        speak(c)
                        print(c)
                        
                elif 'quote' in self.query:
                    quote=stormconsultancy()
                    print(quote)
                    speak(quote)
                            
                elif 'fact' in self.query:
                    fact=randfacts.getFact(False)
                    print(fact)
                    speak(fact)
                        
                elif 'search' in self.query:
                    search = self.query.replace('search', '')
                    speak("Searching"  + search)
                    pywhatkit.search(search)
                                    
                elif 'info' in self.query:
                    info = self.query.replace('info', '')
                    speak("Searching" + info)
                    pywhatkit.info(info)
                            
                elif 'meaning of' in self.query:
                    self.query = self.query.replace('meaning of', '')
                    result = pd.meaning(self.query)
                    speak(result)
                    print(result)

                elif 'temperature' in self.query:
                    search = 'temperature in agra'
                    url = f"http://www.google.com/search?q={search}"
                    r = requests.get(url)
                    data = BeautifulSoup(r.text, 'html.parser')
                    temp = data.find('div',class_= 'BNeawe').text
                    print(f"Current {search} is {temp}")      
                    speak(f"Current {search} is {temp}")  
                                
                elif 'news' in self.query:
                        speak('Sure Sir!! Here are some headlines')
                        def NewsFromBBC():
                                                            
                            self.query_params = {
                            "source": "bbc-news",
                            "sortBy": "top",
                            "apiKey": "b48aa42a1bcc43938c03079051272b19"
                            }
                            main_url = " https://newsapi.org/v1/articles"
                            
                            res = requests.get(main_url, params=self.query_params)
                            open_bbc_page = res.json()

                            article = open_bbc_page["articles"]
                            
                            results = []
                                
                            for ar in article:
                                results.append(ar["title"])
                                    
                            for i in range(len(results)):                                
                                print(i + 1, results[i])
                            
                            from win32com.client import Dispatch
                            speak = Dispatch("SAPI.Spvoice")
                            speak.Speak(results)                

                        if __name__ == '__main__':
                                
                            NewsFromBBC()

                elif 'switch window' in self.query:
                    pyautogui.keyDown('alt')
                    pyautogui.press('tab')
                    time.sleep(1)
                    pyautogui.keyUp('alt')

                elif 'take screenshot' in self.query:
                    speak('Sir, what should be the name of this screenshot ?')
                    name = self.takeCommand().lower()
                    speak("OK sir")
                    time.sleep(1)
                    img = pyautogui.screenshot()
                    img.save(f"(name).png")
                    speak("Screenshot is ready in the main folder, Sir")
                                    
                elif 'shut down' in self.query:
                    speak("Shutting Down System")
                    os.system('shutdown /s /t 5')
                        
                elif 'restart system' in self.query:
                    speak("Shutting Down System")
                    os.system('shutdown /r /t 5')

                elif 'sleep' in self.query or 'good bye' in self.query:
                    speak("OK sir. You can call me whenever you want!")
                    print("OK sir. You can call me whenever you want!")
                    break
 

startExecution = MainThread()

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_aiui()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.startTask)
        self.ui.pushButton_2.clicked.connect(self.close)

    def startTask(self):
        self.ui.movie = QtGui.QMovie("D://Projects//Coding//PhoenixAI//1.gif")
        self.ui.label.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("D://Projects//Coding//PhoenixAI//2.gif")
        self.ui.label_2.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("D://Projects//Coding//PhoenixAI//3.gif")
        self.ui.label_3.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("D://Projects//Coding//PhoenixAI//5.gif")
        self.ui.label_4.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("D://Projects//Coding//PhoenixAI//6.gif")
        self.ui.label_5.setMovie(self.ui.movie)
        self.ui.movie.start()
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        startExecution.start()
        

    def showTime(self):
        current_time = QTime.currentTime()
        current_date = QDate.currentDate()
        lable_time = current_time.toString('hh:mm:ss')
        lable_date = current_date.toString(Qt.ISODate)
        self.ui.textBrowser.setText(lable_date)
        self.ui.textBrowser_2.setText(lable_time)


app = QApplication(sys.argv)
aiui = Main()
aiui.show()
exit(app.exec_())