from dotenv import load_dotenv
from flask import Blueprint, render_template, request
import smtplib
import os

bp = Blueprint('contact', __name__)


@bp.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'GET':
        # return for GET
        return render_template('contact.html', msg_sent=False)
    else:
        # return for POST
        form_name = request.form['userName']
        form_email = request.form['userEmail']
        form_text = request.form['userText']
        # print(form_name, form_email, form_text)
        send_email(form_name, form_email, form_text)
        return render_template('contact.html', msg_sent=True)


# Send message using Gmail smtplib
def send_email(name, email, message):
    load_dotenv()
    OWN_EMAIL = os.environ.get('OWN_EMAIL')
    OWN_PASSWORD = os.environ.get('OWN_PASSWORD')
    email_message = f"Subject:New Message\n\nName: {name}\nEmail: {email}\nMessage: {message}"
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(OWN_EMAIL, OWN_PASSWORD)
        connection.sendmail(OWN_EMAIL, OWN_EMAIL, email_message)
