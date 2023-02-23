from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# Create your views here.
class EmailSend(APIView):

    @staticmethod
    def post(request, *args, **kwargs):
        receiver_email = request.data.get("send_to", None)
        subject = request.data.get("subject", None)
        body  = request.data.get("body", None)
        if receiver_email == None or subject == None or body == None or receiver_email == "" or subject == "" or body == "":
            payload = { 
                "status" : 400,
                "massage" : "Bad Request: Invalid request payload",
                "detial" : "The request payload must include 'send_to', 'subject', 'body'.",
            }
            return Response(payload,status=status.HTTP_400_BAD_REQUEST)

        sender_email = "nuttapat.test@gmail.com"

        # create message object instance
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject

        # attach the message body
        msg.attach(MIMEText(body, 'plain'))

        # create SMTP session
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_username = 'nuttapat.test@gmail.com'
        smtp_password = 'uqmpueppfkbnhajy'
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        try:
            server.login(smtp_username, smtp_password)
        except Exception as e:
            payload = { 
                "status" : 500,
                "massage" : "INTERNAL_SERVER_ERROR",
                "detial" : str(e),
            }
            return Response(payload,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # send the email
        text = msg.as_string()
        try:
            server.sendmail(sender_email, receiver_email, text)
        except Exception as e:
            payload = { 
                "status" : 500,
                "massage" : "INTERNAL_SERVER_ERROR",
                "detial" : str(e),
            }
            return Response(payload,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            server.quit()
        payload = { 
                "status" : 200,
                "massage" : "email sended successfully",
                "detial" : {"From":sender_email,"To":receiver_email,
                            "subject":subject, "body":body },
            }
        return Response(payload,status=status.HTTP_200_OK)
