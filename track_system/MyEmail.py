from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from flask_mysqldb import MySQL
from _init_ import create_app
import os
import random
import string

class MyEmail:
    def __init__(self, receiver) -> None:
        self.receiver = receiver

    def email_generate(self):
        app = create_app()
        db = MySQL(app)

        cur = db.connection.cursor()
        query = "SELECT username FROM user WHERE email = %s"
        user_info = cur.execute(query, ([self.receiver]))

        if user_info > 0:
            random_password = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(10))
            
            update_pass = db.connection.cursor()
            query = "UPDATE user SET password = md5(%s) where email = %s"
            update_pass.execute(query, (random_password, [self.receiver]))
            update_pass.connection.commit()
            update_pass.close()

            generate = Mail(
            from_email= "aqilsmtp@gmail.com",
            to_emails= self.receiver,
            subject= "REQUEST NEW PASSWORD",
            html_content= "<p>This is your new password please log in using this password</p>"
                         +"<p>After log in you can change to new password or stay with the same password "
                         +"below please keep this password safe<br>"
                         +"</p><strong> New Password : " + random_password +"</strong>"
            )

            try:
                sg  = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
                response = sg.send(generate)
                print(response.status_code)
                print(response.body)
                print(response.headers)

            except Exception as e:
                print(e.args)

             
