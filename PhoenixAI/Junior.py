from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import threading


bot = ChatBot("AI")

intent=open(r"D:\New folder (2)\New folder\intents.json","r")

trainer = ListTrainer(bot)

trainer.train(intent)



def ask_from_bot():
    query = textF.get()
    answer_from_bot = bot.get_response(query)
    msgs.insert(END, "you : " + query)
    print(type(answer_from_bot))
    msgs.insert(END, "bot : " + str(answer_from_bot))
    speak(answer_from_bot)
    textF.delete(0, END)
    msgs.yview(END)
