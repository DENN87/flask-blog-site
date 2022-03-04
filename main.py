from flask import Flask, render_template
import requests

app = Flask(__name__)


@app.route('/')
def home():
    api_url = 'https://api.npoint.io/38823c0454884cd19c9c'
    data_response = requests.get(api_url)
    blogs_data = data_response.json()
    print(blogs_data)
    return render_template('home.html', blogs=blogs_data)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


if __name__ == "__main__":
    app.run(debug=True)
