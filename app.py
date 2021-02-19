from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/')
def index():
    return "ruynig puthpon flask - Univa NE, Profe: Guerra"

# @app.route('/home/<user_name>')
# def home(user_name):
#     # return "Welcome home "+user_name

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/hello/<user_name>')
def hello(user_name):
    return render_template('hello.html',user_name=user_name)


@app.route('/w3school')
def w3school():
    return redirect("https://www.w3schools.com/python/")


@app.route('/python')
def python():
    return redirect(url_for('w3school'))






if __name__=="__main__":
    app.run(port=3000, debug=True)