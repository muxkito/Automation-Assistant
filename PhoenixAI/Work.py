import random
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
import numpy as np
import json
import torch
import torch.nn as nn
from torch.utils.data import Dataset,DataLoader
import nltk
nltk.download('punkt')
from nltk.stem.porter import PorterStemmer

Stemmer = PorterStemmer()

def tokenize(sentence):
    return nltk.word_tokenize(sentence)

def stem(word):
    return Stemmer.stem(word.lower())

def bag_of_words(tokenized_sentence,words):
    sentence_word = [stem(word) for word in tokenized_sentence]
    bag = np.zeros(len(words),dtype=np.float32)

    for idx , w in enumerate(words):
        if w in sentence_word:
            bag[idx] = 1

    return bag


class NeuralNet(nn.Module):

    def __init__(self,input_size,hidden_size,num_classes):
        super(NeuralNet,self).__init__()
        self.l1 = nn.Linear(input_size,hidden_size)
        self.l2 = nn.Linear(hidden_size,hidden_size)
        self.l3 = nn.Linear(hidden_size,num_classes)
        self.relu = nn.ReLU()

    def forward(self,x):
        out = self.l1(x)
        out = self.relu(out)
        out = self.l2(out)
        out = self.relu(out)
        out = self.l3(out)
        return out


with open('intents.json','r') as f:
    intents = json.load(f)

all_words = []
tags = []
xy = []

for intent in intents['intents']:
    tag = intent['tag']
    tags.append(tag)

    for pattern in intent['patterns']:
        w = tokenize(pattern)
        all_words.extend(w)
        xy.append((w,tag))

ignore_words = [',','?','/','.','!']
all_words = [stem(w) for w in all_words if w not in ignore_words]
all_words = sorted(set(all_words))
tags = sorted(set(tags))

x_train = []
y_train = []

for (pattern_sentence,tag) in xy:
    bag = bag_of_words(pattern_sentence,all_words)
    x_train.append(bag)

    label = tags.index(tag)
    y_train.append(label)

x_train = np.array(x_train)
y_train = np.array(y_train)

num_epochs = 1000
batch_size = 8
learning_rate = 0.001
input_size = len(x_train[0])
hidden_size = 8
output_size = len(tags)

print("Training The Model..")

class ChatDataset(Dataset):

    def __init__(self):
        self.n_samples = len(x_train)
        self.x_data = x_train
        self.y_data = y_train

    def __getitem__(self,index):
        return self.x_data[index],self.y_data[index]

    def __len__(self):
        return self.n_samples
    
dataset = ChatDataset()

train_loader = DataLoader(dataset=dataset,
                            batch_size=batch_size,
                            shuffle=True,
                            num_workers=0)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = NeuralNet(input_size,hidden_size,output_size).to(device=device)
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(),lr=learning_rate)

for epoch in range(num_epochs):
    for (words,labels)  in train_loader:
        words = words.to(device)
        labels = labels.to(dtype=torch.long).to(device)
        outputs = model(words)
        loss = criterion(outputs,labels)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    if (epoch+1) % 100 ==0:
        print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')

print(f'Final Loss : {loss.item():.4f}')

data = {
"model_state":model.state_dict(),
"input_size":input_size,
"hidden_size":hidden_size,
"output_size":output_size,
"all_words":all_words,
"tags":tags
}

FILE = "TrainData.pth"
torch.save(data,FILE)

print(f"Training Complete, File Saved To {FILE}")

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
with open("intents.json",'r') as json_data:
    intents = json.load(json_data)

FILE = "TrainData.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data["all_words"]
tags = data["tags"]
model_state = data["model_state"]

model = NeuralNet(input_size,hidden_size,output_size).to(device)
model.load_state_dict(model_state)
model.eval()

class NeuralNet(nn.Module):

    def __init__(self,input_size,hidden_size,num_classes):
        super(NeuralNet,self).__init__()
        self.l1 = nn.Linear(input_size,hidden_size)
        self.l2 = nn.Linear(hidden_size,hidden_size)
        self.l3 = nn.Linear(hidden_size,num_classes)
        self.relu = nn.ReLU()

    def forward(self,x):
        out = self.l1(x)
        out = self.relu(out)
        out = self.l2(out)
        out = self.relu(out)
        out = self.l3(out)
        return out


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()



#--------------------------------------------------------

Name = "Jarvis"

from Listen import Listen
from Speak import Say
from Task import InputExecution
from Task import NonInputExecution

def New_Main(query):
       
    query = Listen()
    result = str(query)

    if query == "bye":
        exit()

    query = tokenize(query)
    X = bag_of_words(query,all_words)
    X = X.reshape(1,X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)

    _ , predicted = torch.max(output,dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output,dim=1)
    prob = probs[0][predicted.item()]

    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                reply = random.choice(intent["responses"])

                if "time" in reply:
                    NonInputExecution(reply)

                elif "date" in reply:
                    NonInputExecution(reply)

                elif "day" in reply:
                    NonInputExecution(reply)

                elif "wikipedia" in reply:
                    InputExecution(reply,result)

                elif "google" in reply:
                    InputExecution(reply,result)

                else:
                    Say(reply)

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour <12:
        speak("Good Morning!")

    elif hour >= 12 and hour <10:
        speak("Good Afternoon!")

    else:
        speak("Good Evening!")

    speak("I am your AI Sir, how may I help you")

def Time():
    time = datetime.datetime.now().strftime("%H:%M")
    Say(time)

def Date():
    date = datetime.date.today()
    Say(date)

def Day():
    day = datetime.datetime.now().strftime("%A")
    Say(day)


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

                elif "time" in self.query:
                    Time()

                elif "date" in self.query:
                    Date()

                elif "day" in self.query:
                    Day()

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
                            
                elif 'google' in self.query:
                    speak("Searching...")
                    self.query = self.query.replace('google', '')
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
                    speak('Sir, what should be the mane of this screenshot ?')
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
        self.ui.movie = QtGui.QMovie("D:\\New folder (3)\\1.gif")
        self.ui.label.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("D:\\New folder (3)\\2.gif")
        self.ui.label_2.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("D:\\New folder (3)\\3.gif")
        self.ui.label_3.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("D:\\New folder (3)\\5.gif")
        self.ui.label_4.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("D:\\New folder (3)\\6.gif")
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

