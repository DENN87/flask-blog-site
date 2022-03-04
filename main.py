from flask import Flask, render_template, request
import requests
# for sending emails
import smtplib

app = Flask(__name__)

api_url = 'https://api.npoint.io/38823c0454884cd19c9c'
data_response = requests.get(api_url)
blogs_data = data_response.json()


@app.route('/')
def home():
    return render_template('home.html', blogs=blogs_data)


@app.route('/blog/<int:post_id>')
def get_blog(post_id):
    return render_template('blog.html', blog=blogs_data[post_id-1])


@app.route('/compose')
def compose_post():
    return render_template('compose.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact', methods=['GET', 'POST'])
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
        return render_template('contact.html', msg_sent=True)


if __name__ == "__main__":
    app.run(debug=True)
