import schedule
import time
import os
from dotenv import load_dotenv
import psycopg
from psycopg.errors import ProgrammingError
from twilio.rest import Client

load_dotenv()

# Your Account Sid and Auth Token from twilio.com / console
ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
DATABASE_URL = os.getenv('DATABASE_URL')

client = Client(ACCOUNT_SID, AUTH_TOKEN)

''' Change the value of 'from' with the number
received from Twilio and the value of 'to'
with the number in which you want to send message.'''


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


def processText():
    list = [9294101112]
    for number in list:
        currentNumber = str(number)
        currentNumber = '+1' + currentNumber
        message = client.messages.create(
            from_='+16178827645',
            body='body',
            to=currentNumber
        )
        print(message.sid)


def main():
    # Connect to CockroachDB
    connection = psycopg.connect(DATABASE_URL)

    phone_nums = exec_statement(connection, "SELECT message FROM users")
    print(phone_nums)

    # Close communication with the database
    connection.close()


if __name__ == "__main__":
    main()
