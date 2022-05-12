import os
import datetime
from dotenv import load_dotenv

import smtplib
import mimetypes
from email.message import EmailMessage



# path = os.path.abspath('')
# load_dotenv(os.path.join(path, '.env'))
load_dotenv('./Keys/.env')

MAIL_SECRET = os.getenv("MAIL_SECRET")
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")


class SendEmail:
    """
    Function: Send Email

    Input:
    -   List Of Emails
    -   Subject
    -   Body
    -   Attachment Files

    """ 
    # https://stackoverflow.com/questions/24719368/syntaxerror-non-default-argument-follows-default-argument
    def __init__(self, contacts:list, subject:str, body:str, files:list=None):
       self.CONTACTS = contacts
       self.SUBJECT = subject
       self.BODY = body
       self.FILES = files

    def checkFormat(self,):   
       assert isinstance(self.CONTACTS, list) and isinstance(self.SUBJECT, str) and isinstance(self.BODY, str)
  

    def createPayload(self,):

        self.checkFormat()

        msg = EmailMessage()
        msg['Subject'] = self.SUBJECT
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = self.CONTACTS
        # msg['To'] = ', '.join(self.CONTACTS)
        msg.set_content(self.BODY)

        if self.FILES:
            for file_path in self.FILES:
                file_name = os.path.basename(file_path)
                with open(file_path, 'rb') as f:
                    file_type_subtype, _ = mimetypes.guess_type(file_path)
                    file_type, file_subtype = file_type_subtype.split('/', 1)
            
                    msg.add_attachment(f.read(), maintype=file_type, subtype=file_subtype, filename=file_name)

        return msg

    def send(self, ):
        msg = self.createPayload()
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(EMAIL_ADDRESS, MAIL_SECRET)
                date = datetime.datetime.today().strftime('%Y-%m-%d')
                print('Date: {}'.format(date))
                print('Logged In Successfully...')

                smtp.send_message(msg, EMAIL_ADDRESS, self.CONTACTS)
                print('Email Sent...')
        except Exception as e:
            print('Error: {}'.format(e))




if __name__ == "__main__": 
    files = ['./../Attachments/HW2.pdf','./../Attachments/name.txt']
    textEmail = "Dear Umar,\n\nHope you are doing well!\n\nThank you!\nBest Regards,\nUmar"

    email = SendEmail(['umar.salman1997@gmail.com'], 'Text Email', textEmail, files)
    # email = SendEmail(['umar.salman1997@gmail.com', 'mahaagro48@gmail.com', 'asif.hanif@mbzuai.ac.ae'], 'Text Email', 'Hello from Alaska', files)
    email.send()