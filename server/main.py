import csv
import schedule
import time
import os
from dotenv import load_dotenv
# importing twilio
from twilio.rest import Client
from datetime import date
from datetime import timedelta
from psycopg.errors import ProgrammingError
import psycopg

load_dotenv()

# Your Account Sid and Auth Token from twilio.com / console
ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
DATABASE_URL = os.getenv('DATABASE_URL')
today = date.today()
tommorrow = today + timedelta(days=1)
today = today.strftime("%Y-%m-%d")
tommorrow = tommorrow.strftime("%Y-%m-%d")


client = Client(ACCOUNT_SID, AUTH_TOKEN)


def getEventList():
    # replace path
    PATH = "./server/data.csv"

    with open(PATH, 'r') as read_obj:
        csv_reader = csv.reader(read_obj)
        list_of_events = list(csv_reader)

    return list_of_events[1:]


def exec_statement(conn, stmt):
    res = []
    try:
        with conn.cursor() as cur:
            cur.execute(stmt)
            rows = cur.fetchall()
            for r in rows:
                res.append(r[0])

    except ProgrammingError:
        return

    return res


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

        if (len(messageToDisplay) + len(currentMessage) < 1000):
            messageToDisplay += currentMessage
        else:
            brokenUpMessage.append(messageToDisplay)
            messageToDisplay = ""
            messageToDisplay += currentMessage
        eventNum += 1
    brokenUpMessage.append(messageToDisplay)
    return brokenUpMessage


def processText(str1):
    # Connect to CockroachDB
    connection = psycopg.connect(DATABASE_URL)
    phone_nums = exec_statement(connection, "SELECT message FROM users")

    message = str1
    for number in phone_nums:
        currentNumber = "".join(number.split("-"))
        currentNumber = '+1' + currentNumber
        message = client.messages.create(
            from_='+16178827645',
            body=message,
            to=currentNumber
        )
        print(message.sid)

    # Close communication with the database
    connection.close()


def sendBrokenMessages():
    listOfMessages = format(newDayList(getEventList()))
    for i in range(len(listOfMessages)):
        processText(listOfMessages[i])


# schedule.every().day.at("09:00").do(processText())


# while True:
#     schedule.run_pending()
#     time.sleep(1)


def main():
    sendBrokenMessages()


if __name__ == "__main__":
    main()
