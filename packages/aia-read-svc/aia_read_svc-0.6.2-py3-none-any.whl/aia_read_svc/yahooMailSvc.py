#!/usr/bin/env python
# -*- coding: utf-8 -*-
import imaplib, email  # Library to interact with IMPAP server
from email.header    import Header
from email.mime.text import MIMEText
from .repositories.aiaRepo import AIAMessageRepository
from email.header import decode_header
from datetime import datetime
import random
import time
import csv
import os
from .numbers_to_letters import leer_decenas
from dotenv import load_dotenv
load_dotenv()
#driver = webdriver.Firefox()
from aia_utils.Queue import QueueConsumer, QueueProducer

#https://es.ayuda.yahoo.com/kb/account/Genera-y-administra-contrase%C3%B1as-de-aplicaciones-de-externas-sln15241.html#:~:text=Inicia%20sesi%C3%B3n%20en%20la%20p%C3%A1gina,administrar%20contrase%C3%B1as%20de%20la%20aplicaci%C3%B3n.
class YahooMail:

    def __init__(self, topic_producer, topic_consumer, version):
        self.topic_producer = topic_producer
        self.queueProducer = QueueProducer(self.topic_producer, version, "aia-read-svc")
        self.topic_consumer = topic_consumer
        self.aiaMsgRepo = AIAMessageRepository(os.environ['MONGODB_URI'])
        self.version = version

    def mailDaemon(self):
        queueConsumer = QueueConsumer(self.topic_consumer)
        queueConsumer.listen(self.callback)

    def callback(self, msgDict):
        text = "Llegó un mensaje!"
        print(text)
        try:
            print(str(msgDict["body"]["cmd"]))
            self.getMails()
        except KeyError:
            print("[WARN] not body.cmd field in message")
            pass

    def obtain_header(self, msg):
        # decode the email subject
        subject, encoding = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes) and encoding != None:
            subject = subject.decode(encoding)
    
        # decode email sender
        From, encoding = decode_header(msg.get("From"))[0]
        if isinstance(From, bytes):
            From = From.decode(encoding)
    
        #print("Subject:", subject)
        #print("From:", From)
        return subject, From

    def sendMsg(self, sentences: list):

        dbObject = self.queueProducer.msgBuilder({
            "sentences": sentences,
            "classification": "YAHOO_MAIL"
        })
        id = self.aiaMsgRepo.insertAIAMessage(dbObject)
        print(id)
        sendObject = self.queueProducer.msgBuilder({
            "sentences": sentences,
            "classification": "YAHOO_MAIL"
        })
        sendObject['id'] = str(id)
        print(sendObject)
        #lo de abajo es una mejora que debo testear
        #data = json.dumps(sendObject)
        #data = data.replace("'", '\\"')
        #data = data.replace('"', '\\"')
        #self.queueProducer.send(data)
        self.queueProducer.send(sendObject)
        self.queueProducer.flush()        

    def prepareRemitenteMsg(self, txt):
        txt = txt.replace('"', "")
        txt = txt.replace("@", " arroba ")
        txt = txt.replace(".", " punto ")
        txt = txt.replace("yahoo", "llajú")
        txt = txt.replace("Yahoo", "llajú")
        return txt

    def getMails(self):
        IMAP_server = "imap.mail.yahoo.com"  # Yahoo IMAP server
        mail_id = "grineldosanchez@yahoo.com"
        imap = imaplib.IMAP4_SSL(IMAP_server)
        pwd = str(os.environ['YAHOO_PASSWORD3'])
        # login to the server
        try:
            status, summary = imap.login(mail_id, pwd)
            total_read = 5
            if status == "OK":
                print(imap.list()) # print various inboxes
                print(summary)                
                status, messages = imap.select("INBOX")
                numOfMessages = int(messages[0])  
                print(numOfMessages)
                self.sendMsg([{"msg": "Han llegado nuevos mensajes a la bandeja de entrada procederemos a leer los " 
                               +leer_decenas(total_read)+ " más nuevos.", "sound_in": "e-mail.wav"}])
                for i in range(numOfMessages, numOfMessages - total_read, -1):
                    res,msg = imap.fetch(str(i), "(RFC822)")  # fetches email using ID
                
                    for response in msg:
                        if isinstance(response, tuple):
                            msg = email.message_from_bytes(response[1])
                            subject, From = self.obtain_header(msg)                            
                            print("------------------------------------------------")
                            print(subject)
                            print(From)
                            strFrom = str(From)
                            strFom = self.prepareRemitenteMsg(strFrom)
                            print(From)
                            self.sendMsg([{"msg": "Remitente " + strFom}, 
                                          {"msg": str(subject).replace('"', "")}])
                            print("<"+From + "> " + str(subject))
                imap.close()
        except imaplib.IMAP4.error:
            print("Error logging into Mail")
            sys.exit(0)  # Successful termination


    def getMailsSelenium(self):
        print("selenium1")
        #driver = webdriver.Chrome('./chromedriver107')
        timeout = 5
        driver = webdriver.Chrome()
        #driver.get('https://login.yahoo.com/?.src=ym&lang=en-US&done=https%3A%2F%2Fmail.yahoo.com%2F%3Fguce_referrer%3DaHR0cHM6Ly93d3cuZ29vZ2xlLmNvbS8%26guce_referrer_sig%3DAQAAAIjjx8Mq4TeRJRK7LQmxwRtYKIC-7xuDmlMz7Ntqkx__noaVScl5QrztmdSvSWeypWPGL-jMG37SKn1WVG_2IQiOSSJ6eEw0m2sQVjeAtI2Yw1V8-wJbN2mM4E7yp81uwlbKWT8g5llvZEkCD7x2jSFrtDTJFYIpi7mYPrCLqmmF')
        print("selenium2")
        driver.get("https://mail.yahoo.com/d/folders/1?.src=fp")
        driver.maximize_window()
        print(driver.title)
        userNameElement = driver.find_element(By.NAME, "username")
        userNameElement.clear()
        userNameElement.send_keys(os.environ['YAHOO_USER'])
        userNameElement.send_keys(Keys.RETURN)
        try:
            element_present = EC.presence_of_element_located((By.NAME, 'password'))
            WebDriverWait(driver, timeout).until(element_present)
            passwordElement = driver.find_element(By.NAME, "password")
            passwordElement.clear()
            passwordElement.send_keys(os.environ['YAHOO_PASSWORD'])
            passwordElement.send_keys(Keys.RETURN)
        except TimeoutException:
            print("Timed out waiting for page to load")


        i = 0
        email_list = []

        emails = driver.find_elements(By.CLASS_NAME, "message-list-item")
        for email in emails:
            message = email.text.splitlines()
            print(len(message))
            print("{} | {} ... {}".format(message[0], message[1][:12], message[-1]))
            email_list.append({"title": message[0], "content": message[1], "date": message[-1], "type": "yahoo"})

        driver.close()
        return email_list