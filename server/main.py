import csv
import os
import string
from datetime import date, timedelta
import psycopg
from dotenv import load_dotenv
from psycopg.errors import ProgrammingError
from twilio.rest import Client

load_dotenv()

# Your Account Sid and Auth Token from twilio.com / console
ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
DATABASE_URL = str(os.getenv('DATABASE_URL'))
TWILIO_NUMBER = os.getenv("TWILIO_NUMBER")

client = Client(ACCOUNT_SID, AUTH_TOKEN)
today = date.today()
tomorrow = today + timedelta(days=1)
today = today.strftime("%Y-%m-%d")
tomorrow = tomorrow.strftime("%Y-%m-%d")


def getEventList():
    PATH = "./server/data.csv"

    with open(PATH, 'r') as read_obj:
        csv_reader = csv.reader(read_obj)
        list_of_events = list(csv_reader)

    return list_of_events[1:]


def exec_statement(conn, stmt):
    res: list[str] = []
    try:
        with conn.cursor() as cur:
            cur.execute(stmt)
            rows = cur.fetchall()
            # get all phone numbers (2nd column)
            for r in rows:
                res.append(r[1])

    except ProgrammingError:
        return []

    return res


def newDayList(list1):
    newList = []
    for i in range(len(list1)):
        if list1[i][0] == today:
            newList.append(list1[i])
        else:
            continue

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


def processText(msg):
    # Connect to CockroachDB
    connection = psycopg.connect(DATABASE_URL)
    phone_nums = exec_statement(connection, "SELECT * FROM users")
    # phone_nums=["929-410-1112"]
    print(phone_nums)

    for number in phone_nums:
        currentNumber = "".join(number.split("-"))
        currentNumber = '+1' + currentNumber
        # twilioMsg = client.messages.create(
        #     from_=TWILIO_NUMBER,
        #     body=msg,
        #     to=currentNumber
        # )
        # print(twilioMsg.sid)

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
