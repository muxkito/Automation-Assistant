import pyttsx3
from torch import *
import speech_recognition as sr
import torch.nn as nn
import numpy as np
import nltk
from nltk.stem.porter import PorterStemmer
import json
from torch.utils.data import Dataset,DataLoader
from NeuralNetwork import bag_of_words , tokenize , stem
from Brain import NeuralNet
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
import wikipedia
import webbrowser
import pywhatkit
import pyjokes
import randfacts
from PyDictionary import PyDictionary as pd
from os import system

webbrowser.register('chrome',
	None,
	webbrowser.BackgroundBrowser("C://Program Files (x86)//Google//Chrome//Application//chrome.exe"))
chrome_incog = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s --incognito'

def Say(Text):
    engine = pyttsx3.init("sapi5")
    voices = engine.getProperty('voices')
    engine.setProperty('voices',voices[0].id)
    engine.setProperty('rate',170)
    print("    ")
    print(f"A.I : {Text}")
    engine.say(text=Text)
    engine.runAndWait()
    print("    ")

def Listen():

    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing..")
        query = r.recognize_google(audio,language="en-in")
        print(f"You Said : {query}")

    except:
        return ""

    query = str(query)
    return query.lower()



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

#Function
import datetime
from Speak import Say
#2 Types

#1 - Non Input
#eg: Time , Date , Speedtest

def Time():
    time = datetime.datetime.now().strftime("%H:%M")
    Say(time)

def Date():
    date = datetime.date.today()
    Say(date)

def Day():
    day = datetime.datetime.now().strftime("%A")
    Say(day)
