import schedule
import time

# importing twilio
from twilio.rest import Client

# Your Account Sid and Auth Token from twilio.com / console
account_sid = 'AC37f1875e071ba09e925c8327cef77db4'
auth_token = 'ddbb324d42d78eda5b084496c6eab18a'

client = Client(account_sid, auth_token)

''' Change the value of 'from' with the number
received from Twilio and the value of 'to'
with the number in which you want to send message.'''



def processText():
    list = [9294101112]
    for  number in list:
        currentNumber = str(number)
        currentNumber = '+1' + currentNumber
        message = client.messages.create(
                                from_='+16178827645',
                                body ='body',
                                to =currentNumber
                            )
        print(message.sid)

schedule.every(10).seconds.do(processText)
schedule.every().day.at("09:00").do(processText)


while True:
    schedule.run_pending()
    time.sleep(1)