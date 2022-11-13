import csv
import schedule
import time
import os
from dotenv import load_dotenv
# importing twilio
from twilio.rest import Client
from datetime import date
from datetime import timedelta

load_dotenv()


def getEventList():
    # replace path
    PATH = "./data.csv"

    with open(PATH, 'r') as read_obj:
        csv_reader = csv.reader(read_obj)
        list_of_events = list(csv_reader)

    return list_of_events[1:]


myID = os.getenv("ID")
myToken = os.getenv("TOKEN")
today = date.today()
tommorrow = today + timedelta(days=1)
today = today.strftime("%Y-%m-%d")
tommorrow = tommorrow.strftime("%Y-%m-%d")


client = Client(myID, myToken)


def newDayList(list1):
    newList = []
    for i in range(len(list1)):
        if list1[i][0] == today:
            newList.append(list1[i])
        else:
            break
    return newList


def format(data):
    eventNum = 1
    messageToDisplay = ""
    brokenUpMessage = []
    for i in range(len(data)):
        currentTitle = data[i][2]
        currentTime = data[i][4]
        currentOrg = data[i][5]
        
        currentMessage = (str(eventNum) + ") " + currentTitle +
                                 " at " + currentTime)
        if currentOrg:
            currentMessage += " hosted by " + currentOrg + "\n"
        else:
            currentMessage += "\n"
            
        if (len(messageToDisplay) + len(currentMessage)  < 1000):
            messageToDisplay += currentMessage
        else:
            brokenUpMessage.append(messageToDisplay)
            messageToDisplay = ""
            messageToDisplay += currentMessage
        eventNum += 1
    brokenUpMessage.append(messageToDisplay)
    return brokenUpMessage


def processText(str1):
    list = [9294101112]

    message = str1
    for number in list:
        currentNumber = str(number)
        currentNumber = '+1' + currentNumber
        message = client.messages.create(
            from_='+16178827645',
            body=message,
            to=currentNumber
        )
        print(message.sid)


def sendBrokenMessages():
    listOfMessages = format(newDayList(getEventList()))
    for i in range(len(listOfMessages)):
        processText(listOfMessages[i])

sendBrokenMessages()
# schedule.every().day.at("09:00").do(processText())


# while True:
#     schedule.run_pending()
#     time.sleep(1)
