from website import create_app
from flask_apscheduler import APScheduler
from website.database import offLineSerach
#from website.email_config import mail  # Import the mail object from email.py
from flask_mail import Mail,Message

app = create_app()
shced= APScheduler()

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'kobihazut8@gmail.com'
app.config['MAIL_PASSWORD'] = ''
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail=Mail(app)  # Initialize the mail object with the app

def scheduled_job():
  msg = Message("Hey", sender='noreply@demo.com', recipients=['kobihazut8@gmail.com'])
  msg.body = "Hey how are you? Is everything okay?"
  mail.send(msg) 



if __name__ == '__main__':
    shced.add_job(id='job1',func=scheduled_job,trigger='interval',seconds=20)
    app.debug = True

    #shced.start()
    app.run()

    