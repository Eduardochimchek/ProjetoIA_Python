from chatterbot.trainers import ListTrainer
from chatterbot import ChatBot
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
from pymongo import MongoClient
import gridfs
import os

client = MongoClient('mongodb://localhost:27017/')

banco = client.test_database

def ouvir_microfone():
    microfone = sr.Recognizer()
    with sr.Microphone() as source:
        #Chama a funcao de reducao de ruido disponivel na speech_recognition
        microfone.adjust_for_ambient_noise(source)
        print("Microfone...")
        audio = microfone.listen(source)
    try:
        #Passa o audio para o reconhecedor de padroes do speech_recognition
        frase = microfone.recognize_google(audio, language='pt-BR')
        print("Humano: ", frase)
    except sr.UnknownValueError:

        print('bot: Isso não funcionou')
    return frase


def cria_audio(audio):
    tts = gTTS(audio, lang="pt-BR")
    tts.save('bot.mp3')
    playsound('bot.mp3')
    os.remove('bot.mp3')



bot = ChatBot("ChatBot")

conversa = ['oi',
            'olá',
            'tudo bem?',
            'tudo ótimo',
            'qual seu nome?',
            'Meu nome é Lili']

trainer = ListTrainer(bot)
trainer.train(conversa)

while True:
    quest = ouvir_microfone()
    resposta = bot.get_response(quest)
    cria_audio(str(resposta))
    print('Lili:', resposta)

album = banco.test_collection
bot.mp3 = {
         "nome": "falas",

             }